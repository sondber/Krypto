import numpy as np
import data_import as di
import plot
from Jacob import jacob_support as jake_supp
from Sondre import sondre_support_formulas as supp
import data_import_support as dis
import os
import rolls
from matplotlib import pyplot as plt
import scipy.stats as st


os.chdir("/Users/sondre/Documents/GitHub/krypto")

exchanges = ["bitstampusd", "btceusd", "coinbaseusd", "krakenusd"]

# Importing data for all minutes of the day
exchanges, time_list_min, prices_min, volumes_min = di.get_lists(opening_hours="n", make_totals="n")
spread_hour = rolls.rolls(prices_min[0, :], time_list_min, calc_basis=0, kill_output=1)[1]  # Rolls
spread_day = rolls.rolls(prices_min[0, :], time_list_min, calc_basis=1, kill_output=1)[1]  # Rolls


time_min = time_list_min
prices_min = prices_min  # BitstampUSD
volumes_min = volumes_min  # BitstampUSD

# MINUTES ----------------------------------------------------------------------------------------------------
returns_min = jake_supp.logreturn(prices_min[0, :])
min_of_day, avg_returns_minute, lower_minute, upper_minute = dis.average_over_day(time_list_min, returns_min, frequency="m")

"""
min_of_day, avg_volume_minute = dis.average_over_day(time_list_min, volumes_min[0, :], frequency="m")

figcount = 1  # Making sure all graphs are in unique figures
plt.figure(figcount)
plt.plot(avg_returns_minute, label="Logreturns - Minute", color="blue")

mov_ave = np.zeros(1440)  # Creating a moving average
for i in range(30, 1440):
    mov_ave[i] = np.average(avg_returns_minute[i - 15:i + 15])
plt.plot(mov_ave, label="Logreturns - 30 minute moving average", color="black")

stdev = np.std(returns_min)
plt.ylim([-stdev, stdev])

# Generating x-ticks
labels = ["00:00\n20:00\n09:00", "06:00\n02:00\n15:00", "12:00\n08:00\n21:00", "18:00\n14:00\n03:00",
          "23:59\n19:59\n08:59"]
plt.xticks(np.arange(0, 1441, 6 * 60), labels)
plt.title("Average return per minute over the course of a day")
plt.ylabel("Minute logreturn")
plt.figtext(0.01, 0.068, "London")
plt.figtext(0.01, 0.036, "New York")
plt.figtext(0.01, 0.005, "Tokyo")

plt.legend()
figcount += 1
plt.figure(figcount)

# Volume
plt.plot(avg_volume_minute, label="Volume per minute", color="blue")
plt.xticks(np.arange(0, 1441, 6 * 60), labels)
plt.title("Average volume per minute over the course of a day")
plt.ylabel("Minute volume [BTC]")
plt.figtext(0.01, 0.068, "London")
plt.figtext(0.01, 0.036, "New York")
plt.figtext(0.01, 0.005, "Tokyo")

stdev = np.std(volumes_min[0, :])
mean = np.mean(volumes_min[0, :])
mean_test = np.mean(avg_volume_minute)
plt.ylim([mean-stdev, mean+stdev])

figcount += 1
plt.figure(figcount)

# HOURS ----------------------------------------------------------------------------------------------------
# Converting to hourly data
time_list_hour, prices_hour, volumes_hour = dis.convert_to_hour(time_list_min, prices_min, volumes_min)
returns_hour = jake_supp.logreturn(prices_hour[0, :])

# Finding average for every hour of the day
hour_of_day, avg_returns_hour = dis.average_over_day(time_list_hour, returns_hour, frequency="h")
hour_of_day, avg_volumes_hour = dis.average_over_day(time_list_hour, volumes_hour[0, :], frequency="h")
hour_of_day, avg_spread_hour = dis.average_over_day(time_list_hour, spread_hour, frequency="h")

stdev = np.std(returns_hour)
plt.ylim([-stdev, stdev])
plt.plot(avg_returns_hour, label="Logreturns -  Hour")

labels = ["00:00\n20:00\n09:00", "06:00\n02:00\n15:00", "12:00\n08:00\n21:00", "18:00\n14:00\n03:00",
          "23:59\n19:59\n08:59"]
plt.xticks(np.arange(0, 25, 6), labels)
plt.title("Average return per hour over the course of a day")
plt.ylabel("Hourly logreturn")
plt.figtext(0.01, 0.068, "London")
plt.figtext(0.01, 0.036, "New York")
plt.figtext(0.01, 0.005, "Tokyo")
figcount += 1
plt.figure(figcount)

# Volumes
plt.plot(avg_volumes_hour, label="Volume")
plt.xticks(np.arange(0, 25, 6), labels)
plt.title("Average volume per hour over the course of a day")
plt.ylabel("Hourly volume [BTC]")
plt.figtext(0.01, 0.068, "London")
plt.figtext(0.01, 0.036, "New York")
plt.figtext(0.01, 0.005, "Tokyo")
stdev = np.std(volumes_hour[0, :])
mean = np.mean(volumes_hour[0, :])
plt.ylim([mean-stdev, mean+stdev])
figcount += 1
plt.figure(figcount)


# Rolls
plt.plot(avg_spread_hour, label="Bid/ask (relative)")
plt.title("Roll's estimator for bid/ask spread (relative) - Hourly")
plt.ylabel("Bid/ask spread")
plt.xticks(np.arange(0, 25, 6), labels)
plt.figtext(0.01, 0.068, "London")
plt.figtext(0.01, 0.036, "New York")
plt.figtext(0.01, 0.005, "Tokyo")
stdev = np.std(spread_hour)
mean = np.mean(spread_hour)
plt.ylim([mean-stdev, mean+stdev])
figcount += 1
plt.figure(figcount)


# DAYS ----------------------------------------------------------------------------------------------------
# Converting to daily data

time_list_day, prices_day, volumes_day = dis.convert_to_day(time_min, prices_min, volumes_min)
returns_day = jake_supp.logreturn(prices_day[0, :])

# Finding average for every day of the week
day_of_week, avg_returns_day = dis.average_over_day(time_list_day, returns_day, frequency="d")
day_of_week, avg_volumes_day = dis.average_over_day(time_list_day, volumes_day[0, :], frequency="d")
day_of_week, avg_spread_day = dis.average_over_day(time_list_day, spread_day, frequency="d")

plt.plot(avg_returns_day, label="Returns")

stdev = np.std(returns_day)
plt.ylim([-stdev, stdev])

labels = ["Mon", "Tue", "Wed", "Thur", "Fri", "Sat", "Sun"]
plt.xticks(np.arange(0, 7, 1), labels)
plt.title("Average return per day over the course of a week")
plt.ylabel("Logreturn - Day")

# Volume
figcount += 1
plt.figure(figcount)
plt.xticks(np.arange(0, 7, 1), labels)
plt.ylabel("Daily volume [BTC]")
plt.plot(avg_volumes_day, label="Volumes")
plt.title("Average volume per day over the course of a week")
stdev = np.std(volumes_day[0, :])
mean = np.mean(volumes_day[0, :])
plt.ylim([mean-stdev, mean+stdev])
figcount += 1


# Rolls
plt.figure(figcount)
plt.xticks(np.arange(0, 7, 1), labels)
plt.title("Roll's estimator for bid/ask spread (relative) - Daily")
plt.ylabel("Bid/ask spread")
plt.plot(avg_spread_day, label="Bid/ask (relative)")
stdev = np.std(spread_day)
mean = np.mean(spread_day)
plt.ylim([mean-stdev, mean+stdev])

plt.show()
"""