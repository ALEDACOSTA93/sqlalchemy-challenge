import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# Database Setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

#Flask Setup
app = Flask(__name__)

#Flask Routes
@app.route("/")
def welcome():
    return(
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation"
        f"/api/v1.0/stations"
        f"/api/v1.0/tobs"
        f"/api/v1.0/temp/<start>"
        f"/api/v1.0/temp/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    results = session.query(Measurement.date, Measurement.prcp).all()
    session.close()

    all_prcp = list(np.ravel(results))
    return jsonify(all_prcp)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    results = session.query(Station.station)
    session.close()

    all_stations = list(np.ravel(results))
    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def temperature():
    session = Session(engine)
    previous_yr_date = session.query(dt.datetime(2017, 8, 23)-dt.timedelta(days=365))
    results = session.query(Measurement.station, Measurement.date, Measurement.tobs).\
    filter(Measurement.station == 'USC00519281').filter(Measurement.date >= previous_yr_date).all()

    active_station_tobs = list(np.ravel(results))
    return jsonify(active_station_tobs)

@app.route("/api/v1.0/<start>")
def start():
    session = Session(engine)
    Start_Date = dt.datetime.strptime(start,"%Y-%m-%d")

    results_max = session.query(Measurement.station, func.max(Measurement.tobs)).\
    group_by(Measurement.station).filter(Measurement.date >= Start_Date).all()
    results_min = session.query(Measurement.station, func.min(Measurement.tobs)).\
    group_by(Measurement.station).filter(Measurement.date >= Start_Date).all()
    results_avg = session.query(Measurement.station, func.avg(Measurement.tobs)).\
    group_by(Measurement.station).filter(Measurement.date >= Start_Date).all()
    session.close()

    temps_start = []
    for results in results:
        temp_dict = {}
        temp_max["max temp"] = results_max
        temp_min["min temp"] = results_min
        temp_avg["avg temp"] = results_avg
        temps_start.append(temp_dict)

    return jsonify(temps_start)

@app.route("/api/v1.0/<start>/<end>")
def start_end():
    session = Session(engine)
    Start_Date = dt.datetime.strptime(start,"%Y-%m-%d")
    End_Date = dt.datetime.strptime(end,"%Y-%m-%d")

    results_max = session.query(Measurement.station, func.max(Measurement.tobs)).\
    group_by(Measurement.station).filter(Measurement.date >= Start_Date).all()
    results_min = session.query(Measurement.station, func.min(Measurement.tobs)).\
    group_by(Measurement.station).filter(Measurement.date >= Start_Date).all()
    results_avg = session.query(Measurement.station, func.avg(Measurement.tobs)).\
    group_by(Measurement.station).filter(Measurement.date >= Start_Date AND Measurement.date =< End_Date).all()
    session.close()

    temps_start_end = []
    for results in results:
        temp_dict = {}
        temp_max["max temp"] = results_max
        temp_min["min temp"] = results_min
        temp_avg["avg temp"] = results_avg
        temps_start_end.append(temp_dict)

    return jsonify(temps_start_end)



if __name__ == '__main__':
    app.run(debug=True)