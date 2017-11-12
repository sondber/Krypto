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


def hour_of_day_ticks():
    labels = ["00:00\n20:00\n09:00", "06:00\n02:00\n15:00", "12:00\n08:00\n21:00", "18:00\n14:00\n03:00",
              "23:59\n19:59\n08:59"]
    plt.xticks(np.arange(0, 1441, 6 * 60), labels)
    plt.title("Average return per minute over the course of a day")
    plt.ylabel("Minute logreturn")
    plt.figtext(0.01, 0.068, "London")
    plt.figtext(0.01, 0.036, "New York")
    plt.figtext(0.01, 0.005, "Tokyo")


os.chdir("/Users/sondre/Documents/GitHub/krypto")

exchanges, time_list_minutes, prices_minutes, volumes_minutes = di.get_lists(opening_hours="y", make_totals="n")
time_list_days_clean, time_list_removed, returns_days_clean, volumes_days_clean, log_volumes_days_clean, spread_days_clean, \
illiq_days_clean, log_illiq_days_clean, volatility_days_clean, log_volatility_days_clean = dis.clean_trans_2013(
    time_list_minutes, prices_minutes,
    volumes_minutes)

spread_hour = rolls.rolls(prices_minutes[0, :], time_list_minutes, calc_basis=0, kill_output=1)[1]  # Rolls


hours = 1
days = 0
figcount = 1  # Making sure all graphs are in unique figures

if hours == 1:
    # HOURS ----------------------------------------------------------------------------------------------------
    # Converting to hourly data
    time_list_hour, prices_hour, volumes_hour = dis.convert_to_hour(time_list_minutes, prices_minutes, volumes_minutes)
    returns_hour = jake_supp.logreturn(prices_hour[0, :])

    # Finding average for every hour of the day
    hour_of_day, avg_returns_hour, low_returns_hour, upper_returns_hour = dis.average_over_day(time_list_hour, returns_hour, frequency="h")
    hour_of_day, avg_volumes_hour, low_volumes_hour, upper_volumes_hour = dis.average_over_day(time_list_hour, volumes_hour[0, :], frequency="h")
    hour_of_day, avg_spread_hour, low_spread_hour, upper_spread_hour = dis.average_over_day(time_list_hour, spread_hour, frequency="h")

    avg_returns_hour = avg_returns_hour * 100  # Converting to percentage
    low_returns_hour = low_returns_hour * 100  # Converting to percentage
    upper_returns_hour = upper_returns_hour * 100  # Converting to percentage

    avg_spread_hour = avg_spread_hour * 100  # Converting to percentage
    low_spread_hour = low_spread_hour * 100  # Converting to percentage
    upper_spread_hour = upper_spread_hour * 100  # Converting to percentage

    stdev = np.std(returns_hour) * 100  # Converting to percentage
    plt.ylim([-stdev, stdev])
    plt.plot(avg_returns_hour, label="Logreturns -  Hour")
    plt.plot(low_returns_hour, label="95% confidence interval", color="blue", linestyle='--', linewidth=0.5)
    plt.plot(upper_returns_hour, color="blue", linestyle='--', linewidth=0.5)

    labels = ["00:00\n20:00\n09:00", "06:00\n02:00\n15:00", "12:00\n08:00\n21:00", "18:00\n14:00\n03:00",
              "23:59\n19:59\n08:59"]
    plt.xticks(np.arange(0, 25, 6), labels)
    plt.title("Average return per hour over the course of a day")
    plt.ylabel("Hourly logreturn (%)")
    plt.figtext(0.01, 0.068, "London")
    plt.figtext(0.01, 0.036, "New York")
    plt.figtext(0.01, 0.005, "Tokyo")
    plt.legend()

    figcount += 1
    plt.figure(figcount)

    # Volumes
    plt.plot(avg_volumes_hour, label="Volume")
    plt.plot(low_volumes_hour, label="95% confidence interval", color="blue", linestyle='--', linewidth=0.5)
    plt.plot(upper_volumes_hour, color="blue", linestyle='--', linewidth=0.5)
    plt.xticks(np.arange(0, 25, 6), labels)
    plt.title("Average volume per hour over the course of a day")
    plt.ylabel("Hourly volume [BTC]")
    plt.figtext(0.01, 0.068, "London")
    plt.figtext(0.01, 0.036, "New York")
    plt.figtext(0.01, 0.005, "Tokyo")
    stdev = np.std(volumes_hour[0, :])
    mean = np.mean(volumes_hour[0, :])
    plt.ylim([mean-stdev, mean+stdev])
    plt.legend()

    figcount += 1
    plt.figure(figcount)


    # Rolls
    plt.plot(avg_spread_hour, label="Bid/ask (relative)")
    plt.plot(low_spread_hour, label="95% confidence interval", color="blue", linestyle='--', linewidth=0.5)
    plt.plot(upper_spread_hour, color="blue", linestyle='--', linewidth=0.5)

    plt.title("Roll's estimator for bid/ask spread (relative) - Hourly")
    plt.ylabel("Bid/ask spread (%)")
    plt.xticks(np.arange(0, 25, 6), labels)
    plt.figtext(0.01, 0.068, "London")
    plt.figtext(0.01, 0.036, "New York")
    plt.figtext(0.01, 0.005, "Tokyo")
    stdev = np.std(spread_hour) * 100  # Converting to percentage
    mean = np.mean(spread_hour) * 100  # Converting to percentage
    plt.ylim([mean-stdev, mean+stdev])
    plt.legend()

    figcount += 1
    plt.figure(figcount)

if days == 1:
    # DAYS ----------------------------------------------------------------------------------------------------
    # Converting to daily data

    time_list_day, prices_day, volumes_day = dis.convert_to_day(time_list_minutes, prices_minutes, volumes_minutes)
    returns_day = jake_supp.logreturn(prices_day[0, :])

    # Finding average for every day of the week
    day_of_week, avg_returns_day, low_returns_day, upper_returns_day = dis.average_over_day(time_list_day, returns_day, frequency="d")
    day_of_week, avg_volumes_day, low_volumes_day, upper_volumes_day = dis.average_over_day(time_list_day, volumes_day[0, :], frequency="d")
    day_of_week, avg_spread_day, low_spread_day, upper_spread_day = dis.average_over_day(time_list_day, spread_day, frequency="d")

    avg_returns_day = avg_returns_day * 100  # Converting to percentage
    low_returns_day = low_returns_day * 100  # Converting to percentage
    upper_returns_day = upper_returns_day * 100  # Converting to percentage

    avg_spread_day = avg_spread_day * 100  # Converting to percentage
    low_spread_day = low_spread_day * 100  # Converting to percentage
    upper_spread_day = upper_spread_day * 100  # Converting to percentage

    plt.plot(avg_returns_day, label="Logreturns - Day")
    plt.plot(low_returns_day, label="95% confidence interval", color="blue", linestyle='--', linewidth=0.5)
    plt.plot(upper_returns_day, color="blue", linestyle='--', linewidth=0.5)

    stdev = np.std(returns_day) * 100  # Converting to percentage
    plt.ylim([-stdev, stdev])

    labels = ["Mon", "Tue", "Wed", "Thur", "Fri", "Sat", "Sun"]
    plt.xticks(np.arange(0, 7, 1), labels)
    plt.title("Average return per day over the course of a week")
    plt.ylabel("Daily logreturn (%)")
    plt.legend()

    # Volume
    figcount += 1
    plt.figure(figcount)
    plt.xticks(np.arange(0, 7, 1), labels)
    plt.ylabel("Daily volume [BTC]")
    plt.plot(avg_volumes_day, label="Volumes")
    plt.plot(low_volumes_day, label="95% confidence interval", color="blue", linestyle='--', linewidth=0.5)
    plt.plot(upper_volumes_day, color="blue", linestyle='--', linewidth=0.5)

    plt.title("Average volume per day over the course of a week")
    stdev = np.std(volumes_day[0, :])
    mean = np.mean(volumes_day[0, :])
    plt.ylim([mean-stdev, mean+stdev])
    plt.legend()
    figcount += 1


    # Rolls
    plt.figure(figcount)
    plt.xticks(np.arange(0, 7, 1), labels)
    plt.title("Roll's estimator for bid/ask spread (relative) - Daily")
    plt.ylabel("Bid/ask spread (%)")
    plt.plot(avg_spread_day, label="Bid/ask (relative)")
    plt.plot(low_spread_day, label="95% confidence interval", color="blue", linestyle='--', linewidth=0.5)
    plt.plot(upper_spread_day, color="blue", linestyle='--', linewidth=0.5)
    stdev = np.std(spread_day) * 100  # Converting to percentage
    mean = np.mean(spread_day) * 100  # Converting to percentage
    plt.ylim([mean-stdev, mean+stdev])
    plt.legend()


plt.show()
