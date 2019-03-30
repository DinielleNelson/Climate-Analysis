
from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt

import numpy as np
import pandas as pd

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
Station = Base.classes.station

session = Session(engine)
stations = session.query(Station.station, Station.name).all()

session = Session(engine)
last_date = max(session.query(Measurement.date))
last_date2 = str(last_date[0])

dateObj = dtdt.strptime(last_date2,'%Y-%m-%d')
year_date = dateObj - dt.timedelta(days=365)

precip_l12 = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= year_date).all()
precip_df = pd.DataFrame(precip_l12).set_index('date').sort_values('date', ascending=True)

session = Session(engine)
station_activity = session.query(Measurement.station,func.count(Measurement.id)).group_by(Measurement.station).order_by(func.count(Measurement.id).desc()).all()

session = Session(engine)
top_station = station_activity[0][0]
top_station_temps = session.query(Measurement.tobs).filter(Measurement.station == top_station)
low_temp = min(top_station_temps)
high_temp = max(top_station_temps)
avg_temp = session.query(func.avg(Measurement.tobs)).filter(Measurement.station == top_station).all()

def calc_temps(start_date, end_date):
    return session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()

year_date2 = str(year_date.date())
calc_temp2 = calc_temps(year_date2, last_date2)

total_rain_query = engine.execute('SELECT station, sum(prcp), station.name, station.latitude, station.longitude, station.elevation \
                            FROM measurement JOIN station USING (station) \
                             GROUP BY station ORDER BY sum(prcp) desc').fetchall()

