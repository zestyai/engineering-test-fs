import io
import json
import os
import urllib2

import geojson
import psycopg2
import web
from PIL import Image, ImageDraw
from shapely import wkb

# Setup API routes
urls = (
    '/statistics/(.*)', 'Statistics',
    '/display/(.*)', 'Display',
    '/find', 'Find'
)

# Database connection and cursor (initialized later)
conn = None
cur = None

# Get the absolute path name
script_dir = os.path.dirname(__file__)


class Display:
    def __init__(self):
        pass

    def GET(self, id):
        # Read query parameters
        data = web.input()

        # Since this endpoint returns image/jpeg, let's set the right header
        web.header('Content-Type', 'image/jpeg')
        web.header('Access-Control-Allow-Origin', '*')
        web.header('Access-Control-Allow-Methods', 'GET')

        # Fetch image from DB or cache, if exists
        image = fetch_image(id)
        if image is not False:
            # Do we want to overlay the parcel and building polygons?
            if 'overlay' in data and data['overlay'] == 'yes':
                # Fetch geometries and image boundaries
                query_db("SELECT parcel_geo, building_geo, image_bounds FROM properties WHERE id = %s", [id])
                # Assumes ID exists, if image exists
                row = cur.fetchone()

                # Set default colors, but also accepts custom colors from query parameters
                parcel_color = 'orange'
                building_color = 'green'
                if 'parcel' in data:
                    parcel_color = data['parcel']
                if 'building' in data:
                    building_color = data['building']

                # Plot polygons on image (use shapely to parse wkb)
                geom = wkb.loads(row[0], hex=True)
                image_plotted = geom_plotter(image, row[2], geom, parcel_color)
                geom = wkb.loads(row[1], hex=True)
                image_plotted = geom_plotter(image_plotted, row[2], geom, building_color)

                # Return final image
                return image_plotted.getvalue()

            # Return image without polygon overlays if overlay was not requested
            return image

        # If ID not found then return a 404 image (TODO: do as redirect instead)
        return not_found_image()


class Find:
    def __init__(self):
        pass

    def POST(self):
        # Read POST body as JSON (TODO: validate Content-Type is correct first)
        data = geojson.loads(web.data())

        # Since this endpoint returns application/json, let's set the right header
        web.header('Content-Type', 'application/json')
        web.header('Access-Control-Allow-Origin', '*')
        web.header('Access-Control-Allow-Methods', 'POST')

        # Fetch all properties within distance specified from point specified
        query_db("""
            SELECT id, ST_X(geocode_geo::geometry) AS longitude, ST_Y(geocode_geo::geometry) AS latitude
            FROM properties
            WHERE ST_Distance_Sphere(geocode_geo::geometry, ST_MakePoint(%s, %s)) <= %s
            """,
                 [data.geometry.coordinates[0], data.geometry.coordinates[1], data["x-distance"]])

        return json.dumps([{'propertyId': row[0], 'coordinates': [row[1], row[2]]} for row in cur.fetchall()])


class Statistics:
    def __init__(self):
        pass

    def GET(self, id):
        # Read query parameters
        data = web.input()

        web.header('Content-Type', 'application/json')
        web.header('Access-Control-Allow-Origin', '*')
        web.header('Access-Control-Allow-Methods', 'GET')

        distance = 0
        if 'distance' in data and int(data['distance']) > 0:
            distance = data['distance']

        # Fetch total parcel area
        query_db("""
            SELECT SUM(
              ST_Area(
                ST_Intersection(
                  parcel_geo, ST_Buffer(
                        (SELECT geocode_geo FROM properties WHERE id = %s), %s
                  )
                )
              )
            ) FROM properties;
            """,
                 [id, distance])

        parcel_area = cur.fetchone()[0]

        # Fetch building areas
        query_db("""
            SELECT 
              ST_Area(
                ST_Intersection(
                  building_geo, ST_Buffer(
                        (SELECT geocode_geo FROM properties WHERE id = %s), %s
                  )
                )
              )
            FROM properties;
            """,
                 [id, distance])

        building_areas = [row[0] for row in cur.fetchall()]

        # Fetch building distances to center
        query_db("""
            SELECT 
              ST_Distance(building_geo, (SELECT geocode_geo FROM properties WHERE id = %s))
            FROM properties;
            """,
                 [id])

        building_distances = [row[0] for row in cur.fetchall()]

        query_db("""
            WITH x AS (SELECT geocode_geo FROM properties WHERE id = %s)
            SELECT (SUM(
              ST_Area(
                ST_Intersection(
                  building_geo, ST_Buffer((SELECT geocode_geo FROM x), %s
                  )
                )
              ) / ST_Area(ST_Buffer((SELECT geocode_geo FROM x), %s))) * 100
            ) FROM properties;
            """,
                 [id, distance, distance])

        zone_density = [row[0] for row in cur.fetchall()]

        # Build and return final structure
        return json.dumps({
            'parcel_area_sqm': parcel_area,
            'building_area_sqm': building_areas,
            'building_distances_m': building_distances,
            'zone_density': zone_density
        })


# Plots a geometry's coordinates on top of an image given it's coordinate boundaries and with the provided color
def geom_plotter(image, image_bounds, geom, color):
    # Open image as Image
    img = Image.open(image)

    # Generate image pixels to coordinate bounds ratios
    mul_x = img.size[0] / (image_bounds[2] - image_bounds[0])
    mul_y = img.size[1] / (image_bounds[3] - image_bounds[1])

    # Convert coordinates to pixels
    x = []
    for val_x in geom.exterior.xy[0]:
        x.append((val_x - image_bounds[0]) * mul_x)
    y = []
    for val_y in geom.exterior.xy[1]:
        y.append((image_bounds[3] - val_y) * mul_y)

    # ???
    img2 = img.copy()
    draw = ImageDraw.Draw(img2)

    # Draw polygon
    draw.polygon(zip(x, y), fill=color)

    # Merge images
    img3 = Image.blend(img, img2, 0.5)

    # Convert Image to bytes
    img3_bytes = io.BytesIO()
    img3.save(img3_bytes, format='JPEG')

    return img3_bytes


# Retrieves and caches image from remote
def fetch_image(id):
    # Fetch image_url using provided ID from database
    query_db("""SELECT image_url FROM properties WHERE id = %s""", [id])
    image_url = cur.fetchone()

    # If there's are row found
    if image_url is not None:
        # First check if image is cached locally in the filesystem and return it
        rel_path = 'storage/cache/images/' + id
        abs_file_path = os.path.join(script_dir, rel_path)
        if os.path.exists(abs_file_path):
            image_cache = open(abs_file_path, "r")
            return image_cache

        # If image not cached then fetch it from the remote
        image_url = image_url[0]
        image_resp = urllib2.urlopen(image_url)
        # If image found in remote
        if image_resp.getcode() == 200:
            # Read tiff file and convert it to jpeg
            image_bin = image_resp.read()
            image_tiff = io.BytesIO(image_bin)
            image_jpg = io.BytesIO()
            pil_image = Image.open(image_tiff)
            pil_image.save(image_jpg, format='JPEG')

            # Cache jpeg file in case it's requested again
            rel_path = 'storage/cache/images/' + id
            abs_file_path = os.path.join(script_dir, rel_path)
            image_cache = open(abs_file_path, "w")
            image_cache.write(image_jpg.getvalue())
            image_cache.close()

            image_cache = open(abs_file_path, "r")
            return image_cache

    # If ID not found in database table, or remote url not found, then return false
    return False


# Helper method for running queries (TODO: add exception handling)
def query_db(sql, args):
    cur = cursor_db()

    cur.execute(sql, args)


# Lazy load database connection
def cursor_db():
    global cur, conn
    if not cur:
        # Establish database connection (TODO: read from environment, so that it can be set by docker-compose)
        conn = psycopg2.connect(host="postgresql", port="5432", database="zesty", user="postgres",
                                password="engineTest888")
        conn.autocommit = True

        cur = conn.cursor()

    return cur


def close_db():
    global conn, cur
    if cur:
        cur = None
    if conn:
        conn.rollback()
        conn.close()
        conn = None


# Retrieves and returns the 404 image from filesystem (TODO: do as redirect instead)
def not_found_image():
    rel_path = 'storage/not-found.jpg'
    abs_file_path = os.path.join(script_dir, rel_path)
    fp = open(abs_file_path, 'r+')
    return fp


# Run the API
if __name__ == '__main__':
    app = web.application(urls, globals())
    app.add_processor(web.loadhook(cursor_db))
    app.add_processor(web.unloadhook(close_db))
    app.run()
