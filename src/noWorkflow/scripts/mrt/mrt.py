# HARVARD FOREST MET STATION: PROCESS REAL-TIME DATA

# Process real-time data from Fisher Met Station to create graphs as jpeg files.

# ERB rev. 4-Jun-2017

#----------------------- IMPORTS -------------------------#

from urllib.request import urlopen
import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#---------------------- INITIALIZE ------------------------#

days_to_plot = 30
rows_to_plot = days_to_plot * 96

#---------------------- FUNCTIONS ------------------------#

def outliers(x, min, max):
	if (x >= min and x <= max):
		return x
	else:
		return np.nan

#------------------ SPLIT LOGGER FILE ---------------------#

metsta_url = "http://harvardforest.fas.harvard.edu/sites/harvardforest.fas.harvard.edu/files/weather/metsta.dat"

m101 = open("m101.csv", "w")
m102 = open("m102.csv", "w")

with urlopen(metsta_url) as response:
    for line in response:
        line = line.decode("utf-8")
        if line[0:3] == "101":
            m101.write(line)
        else:
            m102.write(line)

m101.close()
m102.close()

#--------------------- READ FILES ------------------------#

# 15-minute data

cols = ["table", "year", "jd", "time", "airt", "rh", "dewp", "prec", "slrr", "parr", "netr", "bar", "wspd", "wres", "wdir", "wdev", "gspd", "s10t"]
qq_all = pd.read_csv("m101.csv", names = cols)
qq_all_rows = len(qq_all.index)

# daily data

cols = ["table", "year", "jd", "time", "airt", "airtmax", "airtmin", "rh", "rhmax", "rhmin", "dewp", "dewpmax", "dewpmin", "prec", "slrt", "part", "netr", "bar", "wspd", "wres", "wdir", "wdev", "gspd", "s10t", "s10tmax", "s10tmin", "bat", "prog"]
dd_all = pd.read_csv("m102.csv", names = cols)
dd_all_rows = len(dd_all.index)

#------------------------ SUBSET ---------------------------#

# remove unnecessary data
qq = qq_all[(qq_all_rows - rows_to_plot) : qq_all_rows]
dd = dd_all[(dd_all_rows - days_to_plot) : dd_all_rows]

#--------------------- GET DATETIME ------------------------#

# 15-minute data
qq_datetime = pd.to_datetime(qq.year, format='%Y') + pd.to_timedelta(qq.jd - 1, unit='d') + pd.to_timedelta(qq.time // 100, unit='h') + pd.to_timedelta(qq.time % 100, unit='m')

# daily data
dd_date = pd.to_datetime(dd.year, format='%Y') + pd.to_timedelta(dd.jd - 1, unit='d')

#--------------------- CHECK RANGES ------------------------#

# 15-minute data

qq_airt = qq['airt'].apply(lambda x: outliers(x, -50, 50))
qq_dewp = qq['dewp'].apply(lambda x: outliers(x, -50, 50))
qq_s10t = qq['s10t'].apply(lambda x: outliers(x, -50, 50))
qq_slrr = qq['slrr'].apply(lambda x: outliers(x, 0, 1500))
qq_netr = qq['netr'].apply(lambda x: outliers(x, -100, 1000))
qq_wspd = qq['wspd'].apply(lambda x: outliers(x, 0, 100))
qq_gspd = qq['gspd'].apply(lambda x: outliers(x, 0, 100))
qq_prec = qq['prec'].apply(lambda x: outliers(x, 0, 1000))

# daily data

dd_prec = dd['prec'].apply(lambda x: outliers(x, 0, 1000))

#----------------- PLOT 15-MINUTE DATA -------------------#

# AIR TEMPERATURE, SOIL TEMPERATURE, DEW POINT
plt.plot(qq_datetime, qq_airt, color="blue")
plt.plot(qq_datetime, qq_s10t, color="purple")
plt.plot(qq_datetime, qq_dewp, color="gray")
plt.title("Temperature & Humidity")
plt.ylabel("Temperature (deg C)")
plt.savefig('air_temperature.png')
plt.clf()

# SOLAR RADIATION, NET RADIATION
plt.plot(qq_datetime, qq_slrr, color="blue")
plt.plot(qq_datetime, qq_netr, color="gray")
plt.title("Radiation")
plt.ylabel("Radiation (W/m2)")
plt.savefig('solar_radiation.png')
plt.clf()

# WIND SPEED, GUST SPEED

plt.plot(qq_datetime, qq_wspd, color="blue")
plt.plot(qq_datetime, qq_gspd, color="gray")
plt.title("Wind Speed")
plt.ylabel("Speed (m/sec)")
plt.savefig('wind_speed.png')
plt.clf()

# PRECIPITATION

plt.plot(qq_datetime, qq_prec, color="gray")
plt.title("Precipitation")
plt.ylabel("Precipitation (mm)")
plt.savefig('daily_precipitation.png')
plt.clf()
