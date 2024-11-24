# Import the dependencies.
import numpy as np
import sqlalchemy
from sqlalchemy import create_engine, func
from sqlalchemy.orm import Session
from sqlalchemy import column, String, Integer, Float
from sqlalchemy.ext.automap import automap_base

from flask import Flask, jsonify

from dateutil.relativedelta import relativedelta
import datetime as dt

import pandas as pd
#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///C:/Gayatri/UnivOfTexas_Bootcamp/classes/Assignment/Assignment_Module10/Starter_Code/Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################
@app.route('/')
def homepage():
    """List of all available API routes"""
    return (
        f"Available routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/stations_with_tobs<br/>"
        f"/api/v1.0/tobs<br/>"
        f"<b>/api/v1.0/start_date</b>  <i>Example: 2017-07-07 (format: yyyy-mm-dd)</i><br/>"
        f"<b>/api/v1.0/start_date/end_date</b>  <i>Example: 2017-07-07/2017-07-14 (format: yyyy-mm-dd)</i><br/>"
    )
    

@app.route('/api/v1.0/precipitation')
def prcp():
    recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
    if isinstance(recent_date, str):
        recent_date = dt.datetime.strptime(recent_date, "%Y-%m-%d").date()
    twelve_months_ago = recent_date - relativedelta(months=12)
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= twelve_months_ago).order_by(Measurement.date.desc()).all()
    session.close()

    prcp_list=[]
    for date, prcp in results:
        prcp_dict={}
        prcp_dict["Date"] = date
        prcp_dict["Precipitation"] = prcp
        prcp_list.append(prcp_dict)

    return jsonify(prcp_list)

@app.route('/api/v1.0/stations')
def stations():
    results = session.query(Station.station, Station.name).all()
    session.close()
    station_list=[]
    for station, name in results:
        station_dict={}
        station_dict["Station"] = station
        station_dict["Station_Name"] = name
        station_list.append(station_dict)
    return jsonify(station_list)

"""Additional Route using JOIN in the query"""
@app.route('/api/v1.0/stations_with_tobs')
def stations_with_tobs():
    results = session.query(Station.station, Station.name, func.max(Measurement.tobs))\
        .join(Measurement, Measurement.station == Station.station)\
            .group_by(Station.station).all()
    session.close()
    station_tobs_list=[]
    for station, name, max_tobs in results:
        station_tobs_dict={}
        station_tobs_dict["Station"] = station
        station_tobs_dict["Station_Name"] = name
        station_tobs_dict["Max_Tobs"] = max_tobs
        station_tobs_list.append(station_tobs_dict)
    return jsonify(station_tobs_list)

@app.route('/api/v1.0/tobs')
def tobs():
    recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
    if isinstance(recent_date, str):
        recent_date = dt.datetime.strptime(recent_date, "%Y-%m-%d").date()
    twelve_months_ago = recent_date - relativedelta(months=12)

    active_station,_ = session.query(Measurement.station, func.count(Measurement.station)).group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).first()
    session.close()
    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station == active_station).filter(Measurement.date >= twelve_months_ago).order_by(Measurement.date.desc()).all()
    tobs_list=[{"Date": tobs[0], "Temperature": tobs[1]} for tobs in results]        
    return jsonify(tobs_list)

@app.route('/api/v1.0/<start_date>')
def start_date_only(start_date):
    start_date= dt.datetime.strptime(start_date, '%Y-%m-%d')
    results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date >= start_date).all()
    session.close()
    start_date_only_results = [{"Min Temp": results[0][0], "Max Temp": results[0][1], "Avg Temp": results[0][2]}]
    return jsonify(start_date_only_results)

@app.route('/api/v1.0/<start_date>/<end_date>')
def start_end_date(start_date, end_date):
    start_date= dt.datetime.strptime(start_date, '%Y-%m-%d')
    end_date= dt.datetime.strptime(end_date, '%Y-%m-%d')
    results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
    session.close()
    start_end_date_results = [{"Min Temp": results[0][0], "Max Temp": results[0][1], "Avg Temp": results[0][2]}]
    return jsonify(start_end_date_results)

if __name__ == '__main__':
    app.run(debug=True)