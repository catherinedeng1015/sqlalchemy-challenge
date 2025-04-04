# Import the dependencies.
from flask import Flask, jsonify
from sqlalchemy import create_engine, func
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
import datetime as dt
import numpy as np



#################################################
# Database Setup
#################################################


# reflect an existing database into a new model

# reflect the tables
engine = create_engine("sqlite:///../Resources/hawaii.sqlite")
Base = automap_base()
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
@app.route("/")
def welcome():
    """List all available API routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/2015-08-23<br/>"
        f"/api/v1.0/2015-08-23/2017-08-23<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return precipitation data for the last 12 months."""
    most_recent_date = session.query(func.max(Measurement.date)).scalar()
    end_date = dt.datetime.strptime(most_recent_date, '%Y-%m-%d')
    start_date = end_date - dt.timedelta(days=365)

    precipitation_data = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= start_date.strftime('%Y-%m-%d')).all()

    precipitation_dict = {date: prcp for date, prcp in precipitation_data}
    return jsonify(precipitation_dict)

@app.route("/api/v1.0/stations")
def stations():
    """Return a JSON list of stations from the dataset."""
    stations_data = session.query(Station.station, Station.name).all()
    all_stations = [{ "station": station, "name": name } for station, name in stations_data]
    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    """Return temperature observations for the most active station in the past year."""
    most_active_station_id = 'USC00519281'  
    most_recent_date = session.query(func.max(Measurement.date)).scalar()
    end_date = dt.datetime.strptime(most_recent_date, '%Y-%m-%d')
    start_date = end_date - dt.timedelta(days=365)

    temperature_data = session.query(Measurement.tobs).\
        filter(Measurement.station == most_active_station_id).\
        filter(Measurement.date >= start_date.strftime('%Y-%m-%d')).all()

    temp_list = [tobs for (tobs,) in temperature_data]
    return jsonify(temp_list)

@app.route("/api/v1.0/<start>")
def start_route(start):
    """Return TMIN, TAVG, and TMAX for the specified start date."""
    start = start.strip()
    results = session.query(func.min(Measurement.tobs),
                            func.avg(Measurement.tobs),
                            func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()
    temp_stats = results[0]
    return jsonify({
        "TMIN": temp_stats[0],
        "TAVG": temp_stats[1],
        "TMAX": temp_stats[2]
    })

@app.route("/api/v1.0/<start>/<end>")
def start_end_route(start, end):
    """Return TMIN, TAVG, and TMAX for the specified start-end range."""
    start = start.strip()
    end = end.strip()
    results = session.query(func.min(Measurement.tobs),
                            func.avg(Measurement.tobs),
                            func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temp_stats = results[0]
    return jsonify({
        "TMIN": temp_stats[0],
        "TAVG": temp_stats[1],
        "TMAX": temp_stats[2]
    })

@app.route("/api/v1.0/<start>/<end>")
def start_end_route(start, end):
    """Return TMIN, TAVG, and TMAX for the specified start-end range."""
    start = start.strip()
    end = end.strip()

    results = session.query(func.min(Measurement.tobs),
                            func.avg(Measurement.tobs),
                            func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()

    temp_stats = results[0]
    return jsonify({
        "TMIN": temp_stats[0],
        "TAVG": temp_stats[1],
        "TMAX": temp_stats[2]
    })

if __name__ == "__main__":
    app.run(debug=True)