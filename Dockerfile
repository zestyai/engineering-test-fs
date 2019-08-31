FROM python:2.7

# Copy files (TODO: only copy required files, not all)
ADD . /code
WORKDIR /code

# Update pip and install dependencies
RUN pip install --upgrade pip
RUN pip install web.py psycopg2 Pillow geojson shapely

# Start development web server
CMD ["python", "server.py", "1235"]
