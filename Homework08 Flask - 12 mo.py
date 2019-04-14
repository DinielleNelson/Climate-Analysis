from flask import Flask
from flask import jsonify
import climate_starter

app = Flask(__name__)

@app.route("/")
def home():
    return (
        f"Available routes:<br/>"
        f"  / (home)<br/>"
        f"  /api/v1.0/precipitation")

@app.route("/api/v1.0/precipitation")
def precip():
    return jsonify(climate_starter.precip_l12)

# referencing external python file
@app.route("/api/v1.0/stations")
def stations():
    return jsonify(climate_starter.stations)

# creating entire query within def 
@app.route("/api/v1.0/stations_2")
def stations_2():
        import sqlalchemy
        from sqlalchemy.ext.automap import automap_base
        from sqlalchemy.orm import Session
        from sqlalchemy import create_engine, func

        engine = create_engine("sqlite:///Resources/hawaii.sqlite")
        Base = automap_base()
        Base.prepare(engine, reflect=True)
        Station = Base.classes.station
        session = Session(engine)
        stations = session.query(Station.station, Station.name).all()
        return jsonify(stations)

@app.route("/api/v1.0/tobs")
def temp_obs():
        import datetime as dt
        from datetime import datetime as dtdt

        import sqlalchemy
        from sqlalchemy.ext.automap import automap_base
        from sqlalchemy.orm import Session
        from sqlalchemy import create_engine, func

        engine = create_engine("sqlite:///Resources/hawaii.sqlite")

        Base = automap_base()
        Base.prepare(engine, reflect=True)
        Measurement = Base.classes.measurement

        session = Session(engine)
        last_date = max(session.query(Measurement.date))
        last_date2 = str(last_date[0])

        dateObj = dtdt.strptime(last_date2,'%Y-%m-%d')
        year_date = dateObj - dt.timedelta(days=365)

        precip_l12 = session.query(Measurement.date, Measurement.tobs,Measurement.station).filter(Measurement.date >= year_date).all()
        return jsonify(precip_l12)

@app.route("/api/v1.0/<start>")
def temp_start(start):
        import datetime as dt
        from datetime import datetime as dtdt

        import sqlalchemy
        from sqlalchemy.ext.automap import automap_base
        from sqlalchemy.orm import Session
        from sqlalchemy import create_engine, func

        engine = create_engine("sqlite:///Resources/hawaii.sqlite")

        Base = automap_base()
        Base.prepare(engine, reflect=True)
        Measurement = Base.classes.measurement

        session = Session(engine)
        tobs_start =session.query(func.min(Measurement.tobs), funcmon.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).all()
        
        return jsonify(tobs_start)
        
@app.route("/api/v1.0/<start>/<end>")
def temp_startend(start,end):
        import datetime as dt
        from datetime import datetime as dtdt

        import sqlalchemy
        from sqlalchemy.ext.automap import automap_base
        from sqlalchemy.orm import Session
        from sqlalchemy import create_engine, func

        engine = create_engine("sqlite:///Resources/hawaii.sqlite")

        Base = automap_base()
        Base.prepare(engine, reflect=True)
        Measurement = Base.classes.measurement

        session = Session(engine)
        tobs_startend =session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs))\
                .filter(Measurement.date >= start).filter(Measurement.date <= end).all()
        
        return jsonify(tobs_startend)

if __name__ == "__main__":
    app.run(debug=True)
