# Import the dependencies.
from flask import Flask, jsonify
from datetime import datetime, timedelta
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func



#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)
session = Session(engine)

# reflect the tables
Station = Base.classes.station
Measurement = Base.classes.measurement

# Create Flask app
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

# Define route for home page
@app.route("/")
def welcome():
    return (
        f"Welcome to the Climate App!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/&lt;start&gt;<br/>"
        f"/api/v1.0/&lt;start&gt;/&lt;end&gt;"
    )

# Define route for precipitation data
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Calculate the date one year ago from the most recent date
    one_year_ago = datetime.now() - timedelta(days=365)
    
    # Query precipitation data for the last 12 months
    precipitation_data = session.query(Measurement.date, Measurement.prcp)\
        .filter(Measurement.date >= one_year_ago).all()
    
    # Convert the query results to a dictionary
    precipitation_dict = {date: prcp for date, prcp in precipitation_data}
    
    return jsonify(precipitation_dict)

# Define route for stations
@app.route("/api/v1.0/stations")
def stations():
    # Query all stations
    stations = session.query(Station.station).all()
    
    # Convert the query results to a list
    station_list = [station for station, in stations]
    
    return jsonify(station_list)

# Define route for temperature observations
@app.route("/api/v1.0/tobs")
def tobs():
    # Calculate the date one year ago from the most recent date
    one_year_ago = datetime.now() - timedelta(days=365)
    
    # Query temperature observations for the last 12 months for the most active station
    temperature_data = session.query(Measurement.tobs)\
        .filter(Measurement.date >= one_year_ago).all()
    
    # Convert the query results to a list
    temperature_list = [temp for temp, in temperature_data]
    
    return jsonify(temperature_list)

# Define route for temperature statistics from a given start date
@app.route("/api/v1.0/<start>")
def temperature_start(start):
    # Query temperature statistics from the given start date
    temperature_stats = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs))\
        .filter(Measurement.date >= start).all()
    
    # Convert the query results to a dictionary
    temp_stats_dict = {
        "Minimum Temperature": temperature_stats[0][0],
        "Average Temperature": temperature_stats[0][1],
        "Maximum Temperature": temperature_stats[0][2]
    }
    
    return jsonify(temp_stats_dict)

# Define route for temperature statistics between a given start and end date
@app.route("/api/v1.0/<start>/<end>")
def temperature_range(start, end):
    # Query temperature statistics between the given start and end date
    temperature_stats = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs))\
        .filter(Measurement.date >= start)\
        .filter(Measurement.date <= end).all()
    
    # Convert the query results to a dictionary
    temp_stats_dict = {
        "Minimum Temperature": temperature_stats[0][0],
        "Average Temperature": temperature_stats[0][1],
        "Maximum Temperature": temperature_stats[0][2]
    }
    
    return jsonify(temp_stats_dict)

if __name__ == '__main__':
    app.run(debug=True)
