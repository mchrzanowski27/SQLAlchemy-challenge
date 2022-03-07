#Import dependencies
import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# Database Setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Station = Base.classes.station
Measurement = Base.classes.measurement

# Flask Setup
app = Flask(__name__)

#Flask routes
#Home
@app.route("/")
def home():
    return (
        "Welcome!<br/>"
        "Available routes:<br/>"
        f"Precipitation by date: /api/v1.0/precipitation<br/>"
        f"List of stations: /api/v1.0/stations<br/>"
        f"Temperatures for the last year: /api/v1.0/tobs<br/>"
        f"Temperature data from start date*: /api/v1.0/<start_date><br/>"
        f"Temperature data between start and end dates*: /api/v1.0/<start_date>/<end_date><br/>"
        f"*Dates should be entered in YYYY-MM-DD format"
    )

#Precipitation
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of date and precipitation data"""
    # Query date and precipitation
    results = session.query(Measurement.date, Measurement.prcp).all()

    #Close session
    session.close()

    # Create a dictionary from the row data and append to a list
    precipitation = []
    for date, prcp in results:
        precipitation_dict = {}
        precipitation_dict[date] = prcp
        precipitation.append(precipitation_dict)

    return jsonify(precipitation)

#Stations
@app.route("/api/v1.0/stations")
def stations():
    # Create our session from Python to the DB
    session = Session(engine)

    """Return a list of all stations"""
    # Query stations
    results = session.query(Station.station).all()

    #Close session
    session.close()

    # Convert list of tuples into normal list
    all_stations = list(np.ravel(results))

    return jsonify(all_stations)

#Temperature
@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session from Python to the DB
    session = Session(engine)

    """Return a list of dates and tobs for the most active station for the last year of data"""
    most_active_station = 'USC00519281' 
    most_recent_year = '2016-08-23'    

    #Query
    results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.station == most_active_station).\
        filter(Measurement.date >= most_recent_year).all()

    #Close session
    session.close()

    # Create a dictionary from the row data and append to a list
    temp = []
    for date, tobs in results:
        tobs_dict = {}
        tobs_dict["Date"] = date
        tobs_dict["Temperature"] = tobs
        temp.append(tobs_dict)

    return jsonify(temp)

#Start date
@app.route("/api/v1.0/<start_date>")
def startdate(start_date):
    # Create our session from Python to the DB
    session = Session(engine)

    """Return a list of the minimum temperature, the average temperature, and the max temperature for a given start date"""
    #Query
    results = session.query(func.max(Measurement.tobs), func.min(Measurement.tobs), func.avg(Measurement.tobs)).\
        filter(Measurement.date >= start_date).all()
    
    #Close session
    session.close()

        # Create a dictionary from the data and append to a list
    temp_calc = []
    for max, min, avg in results:
        temp_calc_dict = {}
        temp_calc_dict["Maximum Temperature"] = max
        temp_calc_dict["Minimum Temperature"] = min
        temp_calc_dict["Average Temperature"] = avg
        temp_calc.append(temp_calc_dict)

    return jsonify(temp_calc)


#Start and end dates
@app.route("/api/v1.0/<start_date>/<end_date>")
def start_end(start_date, end_date):
    # Create our session from Python to the DB
    session = Session(engine)

    """Return a list of the minimum temperature, the average temperature, and the max temperature for a given date period"""
    #Query
    results = session.query(func.max(Measurement.tobs), func.min(Measurement.tobs), func.avg(Measurement.tobs)).\
        filter(Measurement.date >= start_date).\
        filter(Measurement.date <= end_date).all()

    #Close session
    session.close()

    # Create a dictionary from the data and append to a list
    temp_calc = []
    for max, min, avg in results:
        temp_calc_dict = {}
        temp_calc_dict["Maximum Temperature"] = max
        temp_calc_dict["Minimum Temperature"] = min
        temp_calc_dict["Average Temperature"] = avg
        temp_calc.append(temp_calc_dict)

    return jsonify(temp_calc)



if __name__ == '__main__':
    app.run(debug=True)
