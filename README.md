# Zesty.ai engineering test (full-stack)

## Background

Full-stack engineers at Zesty.ai develop our web applications end-to-end, working with modern front-end frameworks, APIs (ours and third parties'), and many kinds of data and imagery.

This test is an opportunity for you to demonstrate your comfort with developing a UI that utilizes existing back-end services, similar to a day-to-day project you might encounter working on our team.

## Assignment

Your goal is to create a web application to integrate with an API that allows developers to search for and retrieve information about real estate properties.

There are several different options for features you can implement in the application.  You can pick whichever ones you think you can do best.  The goal is to do as many as you can complete in **4 hours**. 

Note that some features are more difficult than others, and you will be evaluated on more than just the number of features completed.  Quality is preferred over quantity.  Design, organize, and comment your code as you would a typical production project.  Be prepared to explain any decisions you made.

## Setup
### Development environment requirements

You will need to install [Docker](https://www.docker.com/products/docker-desktop) and [`docker-compose`](https://docs.docker.com/compose/install/) to run the provided API service.

### API and database startup
From the root folder of this repo, run `docker-compose up -d` to start the API service and PostgreSQL database needed for this example.  The API service will be exposed on port **5080**.  The database server will be exposed on port **5555**.  If this port is not available on your computer, feel free to change the port in the `docker-compose.yml` file.

In case you are curious, the test database includes a single table called `properties` (with 5 sample rows), each row representing a property or address.  There are three geography* fields and one field with an image URL pointing to an image on [Google Cloud Storage](https://cloud.google.com/storage/).


### API

The API you will be integrating with for this project consists of three endpoints:

* `/find?geojson={geojson}&distance={distance}`
Finds properties within a radius *distance* in meters

* `/statistics?propertyId={propertyId}&distance={distance}`
Finds statistics such as parcel area, buildings area, and buildings distances to center

* `/display/{propertyId}[?overlay=[false|true]]`
Displays the image of property *propertyId*, optionally overlaying parcel and building footprints

### Feature list
(Note: Not all of these must be implemented - select the ones you think you can do in **4 hours**)

* **Search:** Prompt the user for a longitude, latitude, and search radius (default 10000 meters) and display, in a tabular format, the results of the search, including the image of the property and its geographic location (longitude and latitude)
* **Detail Page:** Show detailed information about a given property, including its image, geographic location, and statistics.
* **Visual Search:** Using [Google Maps](https://developers.google.com/maps/documentation/), display a map based on the user's current location (or an address they enter), and display markers on the map for any property located on that map<sup>*</sup>.  Clicking on the marker should reveal an [Info Window](https://developers.google.com/maps/documentation/javascript/examples/infowindow-simple) with key property information.
* **Save for Later:** Allow users to save properties from the Search, Detail, or Visual Search pages and visit their list of saved properties.
* **Freestyle:** If you can think of any other useful features to develop, feel free to implement them.

<sup>*</sup>By default, you may want to load the map with a very low zoom level, since our test database only has a few properties.

## Submission instructions

Send us your completed app, along with instructions for how to run it.  Consider sharing your completed app as a Docker image that runs alongside the API service provided.

Please include a list of what features you implemented, or if you did the freestyle, describe the features you came up with.  Add any comments or things you want the reviewer to consider when looking at your submission.  You don't need to be too detailed, as there will likely be a review done with you where you can explain what you've done.
