  
import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
measurement = Base.classes.measurement
station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def home():
    return (f"Available routes:<br/>"
            f"-------------------------------<br/>"
            f"/api/v1.0/precipitation<br/>"
            f"/api/v1.0/stations<br/>"
            f"/api/v1.0/tobs<br/>"
            f"/api/v1.0/start<br/>"
            f"/api/v1.0/start/end<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    precipitation = [measurement.prcp, measurement.date]
    yeardate = dt.datetime(2016,8,23)
    precip_query = session.query(*precipitation).\
        filter(measurement.date >= yeardate).all()

    precip_list = []
    for x in precip_query:
        precip_list.append(precip_query)

    session.close()
    
    return jsonify(precip_list)



@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    station_query = session.query(measurement.station, func.count(measurement.station)).\
        group_by(measurement.station).\
        order_by(func.count(measurement.station).desc()).all()


    station_list = []
    for x in station_query:
        precip_list.append(station_query)

    session.close()
    
    return jsonify(station_query)


    
@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    yeardate = dt.datetime(2016,8,23)
    histo_list=[]

    for x in session.query(measurement).filter(measurement.station=="USC00519281").filter(measurement.date>yeardate):
        histo_list.append(measure.tobs)
    
  
    session.close()
    
    return jsonify(histo_list)
    
@app.route("/api/v1.0/<start>")
def start(start):
    print(start)
    newer_list=[]
    for measure in session.query(measurement).filter(measurement.station=="USC00519281").filter(measurement.date=start):
        newer_list.append(measure.tobs)

    mean = np.mean(newer_list)
    high = np.max(newer_list)
    low = np.min(newer_list)



@app.route("/api/v1.0/<start>/<end>")
def startend(start,end):
    startend_list=[]
    for measure in session.query(measurement).filter(measurement.station=="USC00519281").filter(measurement.date>=start).filter(measurement.date=<end):
        startend_list.append(measure.tobs)

   
if __name__ == "__main__":
    app.run(debug=True)