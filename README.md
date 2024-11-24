# Climate Data Analysis

# Overview

This project involves analyzing climate data for Honolulu, Hawaii, using SQLAlchemy and Flask. 

The project is divided into two main parts:

Climate Data Analysis: Using SQLAlchemy to query and analyze climate data, including precipitation and station statistics.

Flask API: Building an API to get details on the climate analysis data through various endpoints.

# Files Description:

hawaii.sqlite: SQLite database file containing 2 tables namely Measurement and Station. 

The Measurement table has information on Station, Date, Precipitation and Temperature observations. 

The Station table has information on Station Name, Latitude, Longitude and Elevation.

climate_starter.ipynb: Jupyter notebook for performing the climate analysis.

app.py: Flask app file containing API routes that expose the climate data through HTTP endpoints.

# Prerequisites:

Python 3.x

Flask

SQLAlchemy

Pandas

Jupyter Notebook

Matplotlib


# climate_starter.ipynb notebook:

The notebook is linked to the hawaii.sqlite database and provides analysis on precipitation and station analysis

# app.py (Flask API):

The app.py provides endpoints for the climate data analysis. Here’s a summary of the API routes:

/api/v1.0/precipitation

GET: Returns the precipitation data for the last 12 months in JSON format.

/api/v1.0/stations

GET: Returns list of stations in the dataset in JSON format.

/api/v1.0/stations_with_tobs

GET: Returns list of stations along with max temperature observations for the respective stations in JSON format.

/api/v1.0/tobs

GET: Returns the temperature observations (TOBS) for the most active station in the last 12 months in JSON format.

/api/v1.0/<start_date>

GET: Returns the minimum, average, and maximum temperatures from the given start_date to the present.
Example: /api/v1.0/2017-07-07

/api/v1.0/<start_date>/<end_date>

GET: Returns the minimum, average, and maximum temperatures between the given start_date and end_date.
Example: /api/v1.0/2017-07-07/2017-07-31
