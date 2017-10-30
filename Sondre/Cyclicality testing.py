import numpy as np
import data_import as di
import plot
from Jacob import jacob_support as jake_supp
from Sondre import sondre_support_formulas as supp
import descriptive_stats as desc
import data_import_support as dis
import os
from matplotlib import pyplot as plt
from scipy import math

os.chdir("/Users/sondre/Documents/GitHub/krypto")

exchanges = ["bitstampusd", "btceusd", "coinbaseusd", "krakenusd"]


# Importing data for all minutes of the day
exchanges, time_list, prices, volumes = di.get_lists(opening_hours="n", make_totals="n")

prices_min = prices
time_min = time_list
volumes_min = volumes
# MINUTES ----------------------------------------------------------------------------------------------------
full_returns = jake_supp.logreturn(prices_min[0, :])
full_day_time, full_day_avg_returns = dis.average_over_day(time_list, full_returns, frequency="m")
full_day_time, full_day_avg_volume = dis.average_over_day(time_list, volumes[0, :], frequency="m")

figcount = 1
plt.figure(figcount)
plt.plot(full_day_avg_returns, label="Returns per minute", color="blue")

mov_ave = np.zeros(1440)
for i in range(30, 1440):
    mov_ave[i] = np.average(full_day_avg_returns[i-15:i+15])

plt.plot(mov_ave, label="30 minute moving average", color="black")

stdev = np.std(full_returns)
plt.ylim([-stdev, stdev])

plt.title("Minute returns")

labels = ["00:00\n20:00\n09:00", "06:00\n02:00\n15:00", "12:00\n08:00\n21:00", "18:00\n14:00\n03:00",
          "23:59\n19:59\n08:59"]
plt.xticks(np.arange(0, 1441, 6*60), labels)
plt.title("Average return over the course of a day")
plt.ylabel("Hourly logreturn")
plt.figtext(0.01, 0.068, "London")
plt.figtext(0.01, 0.036, "New York")
plt.figtext(0.01, 0.005, "Tokyo")

plt.legend()
figcount += 1
plt.figure(figcount)

# Volume
plt.plot(full_day_avg_volume, label="Volume per minute", color="blue")
plt.xticks(np.arange(0, 1441, 6*60), labels)
plt.title("Average volume over the course of a day")
plt.ylabel("Hourly volume")
plt.figtext(0.01, 0.068, "London")
plt.figtext(0.01, 0.036, "New York")
plt.figtext(0.01, 0.005, "Tokyo")

plt.legend()
figcount += 1
plt.figure(figcount)


# HOURS ----------------------------------------------------------------------------------------------------
# Converting to hourly data
time_list, prices, volumes = dis.convert_to_hour(time_list, prices, volumes)
full_returns = jake_supp.logreturn(prices[0, :])

# Finding average for every hour of the day
full_day_time, full_day_avg_returns = dis.average_over_day(time_list, full_returns, frequency="h")
full_day_time, full_day_avg_volumes = dis.average_over_day(time_list, volumes[0, :], frequency="h")

stdev = np.std(full_returns)
plt.ylim([-stdev, stdev])
plt.plot(full_day_avg_returns, label="Returns per hour")

labels = ["00:00\n20:00\n09:00", "06:00\n02:00\n15:00", "12:00\n08:00\n21:00", "18:00\n14:00\n03:00",
          "23:59\n19:59\n08:59"]
plt.xticks(np.arange(0, 25, 6), labels)
plt.title("Average return over the course of a day")
plt.ylabel("Hourly logreturn")
plt.figtext(0.01, 0.068, "London")
plt.figtext(0.01, 0.036, "New York")
plt.figtext(0.01, 0.005, "Tokyo")
plt.legend()
figcount += 1
plt.figure(figcount)


# Volumes
plt.plot(full_day_avg_volumes, label="Volume")
plt.xticks(np.arange(0, 25, 6), labels)
plt.title("Average volume over the course of a day")
plt.ylabel("Hourly volume")
plt.figtext(0.01, 0.068, "London")
plt.figtext(0.01, 0.036, "New York")
plt.figtext(0.01, 0.005, "Tokyo")
plt.legend()
figcount += 1
plt.figure(figcount)


# DAYS ----------------------------------------------------------------------------------------------------
# Converting to daily data

time_list, prices, volumes = dis.convert_to_day(time_min, prices_min, volumes_min)
full_returns = jake_supp.logreturn(prices[0, :])

# Finding average for every day of the week
full_day_time, full_day_avg_returns = dis.average_over_day(time_list, full_returns, frequency="d")
full_day_time, full_day_avg_volumes = dis.average_over_day(time_list, volumes[0,:], frequency="d")

plt.plot(full_day_avg_returns, label="Returns per hour")

stdev = np.std(full_returns)
plt.ylim([-stdev, stdev])

labels = ["Mon", "Tue", "Wed", "Thur", "Fri", "Sat", "Sun"]
plt.xticks(np.arange(0, 7, 1), labels)
plt.title("Average return over the course of a week")
plt.ylabel("Daily logreturn")
plt.legend()

# Volume
figcount += 1
plt.figure(figcount)
plt.xticks(np.arange(0, 7, 1), labels)
plt.ylabel("Daily volume [BTC]")
plt.plot(full_day_avg_volumes, label="Volumes")
plt.legend()
plt.title("Volumes")


plt.show()
