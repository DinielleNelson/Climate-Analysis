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



if __name__ == "__main__":
    app.run(debug=True)
