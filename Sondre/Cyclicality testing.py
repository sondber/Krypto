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
import ILLIQ


os.chdir("/Users/sondre/Documents/GitHub/krypto")
exchanges, time_list_minutes, prices_minutes, volumes_minutes = di.get_lists(opening_hours="n", make_totals="n")

hours = 1
days = 1
# daily
non_transformed = 1
transformed = 1
figcount = 0  # Making sure all graphs are in unique figures

# Converting to hourly data
time_list_hour, prices_hour, volumes_hour = dis.convert_to_hour(time_list_minutes, prices_minutes, volumes_minutes)

if hours == 1:
    # HOURS ----------------------------------------------------------------------------------------------------
    returns_hour = jake_supp.logreturn(prices_hour[0, :])
    spread_hour = rolls.rolls(prices_minutes[0, :], time_list_minutes, calc_basis=0, kill_output=1)[1]  # Rolls

    # Finding average for every hour of the day
    hour_of_day, avg_returns_hour, low_returns_hour, upper_returns_hour = dis.cyclical_average(time_list_hour, returns_hour, frequency="h")
    hour_of_day, avg_volumes_hour, low_volumes_hour, upper_volumes_hour = dis.cyclical_average(time_list_hour, volumes_hour[0, :], frequency="h")
    hour_of_day, avg_spread_hour, low_spread_hour, upper_spread_hour = dis.cyclical_average(time_list_hour, spread_hour, frequency="h")

    # Returns
    figcount += 1
    plt.figure(figcount)
    plot.plot_for_day(avg_returns_hour, low_returns_hour, upper_returns_hour, "Returns", perc=1)
    plot.plot_y_zero([0, 24])

    # Volumes
    figcount += 1
    plt.figure(figcount)
    plot.plot_for_day(avg_volumes_hour, low_volumes_hour, upper_volumes_hour, "Volume", perc=0)

    # Rolls
    figcount += 1
    plt.figure(figcount)
    plot.plot_for_day(avg_spread_hour, low_spread_hour, upper_spread_hour, "Spread", perc=1)

if days == 1:
    # DAYS ----------------------------------------------------------------------------------------------------
    # Converting to daily data

    time_list_day, prices_day, volumes_day = dis.convert_to_day(time_list_minutes, prices_minutes, volumes_minutes)
    returns_day = jake_supp.logreturn(prices_day[0, :])
    spread_day = rolls.rolls(prices_minutes[0, :], time_list_minutes, calc_basis=1, kill_output=1)[1]  # Rolls

    if non_transformed == 1:
        # Finding average for every day of the week
        day_of_week, avg_returns_day, low_returns_day, upper_returns_day = dis.cyclical_average(time_list_day, returns_day, frequency="d")
        day_of_week, avg_volumes_day, low_volumes_day, upper_volumes_day = dis.cyclical_average(time_list_day, volumes_day[0, :], frequency="d")
        day_of_week, avg_spread_day, low_spread_day, upper_spread_day = dis.cyclical_average(time_list_day, spread_day, frequency="d")

        # Returns
        figcount += 1
        plt.figure(figcount)
        plot.plot_for_week(avg_returns_day, low_returns_day, upper_returns_day, name="Returns", perc=1)

        # Volumes
        figcount += 1
        plt.figure(figcount)
        plot.plot_for_week(avg_volumes_day, low_volumes_day, upper_volumes_day, name="Volumes", perc=0)

        # Spread
        figcount += 1
        plt.figure(figcount)
        plot.plot_for_week(avg_spread_day, low_spread_day, upper_spread_day, name="Spread", perc=1)

    if transformed == 1:
        # opening hours only
        exchanges, time_list_minutes_open, prices_minutes_open, volumes_minutes_open = di.get_lists(opening_hours="y", make_totals="n")
        # importing transformed variables
        time_list_days_clean, time_list_removed, returns_days_clean, volumes_days_clean, log_volumes_days_clean, spread_days_clean, \
        illiq_days_clean, log_illiq_days_clean, volatility_days_clean, log_volatility_days_clean = dis.clean_trans_2013(
            time_list_minutes_open, prices_minutes_open,
            volumes_minutes_open)

        # Finding average for mon-fri
        day_of_week, avg_log_volume_day, low_log_volume_day, upper_log_volume_day = dis.cyclical_average(time_list_days_clean, log_volumes_days_clean, frequency="d")
        day_of_week, avg_volatility_day_clean, low_volatility_day_clean, upper_volatility_day_clean = dis.cyclical_average(time_list_days_clean, volatility_days_clean, frequency="d")
        day_of_week, avg_illiq_day_clean, low_illiq_day_clean, upper_illiq_day_clean = dis.cyclical_average(time_list_days_clean, illiq_days_clean, frequency="d")
        day_of_week, avg_spread_day_clean, low_spread_day_clean, upper_spread_day_clean = dis.cyclical_average(time_list_days_clean, spread_days_clean, frequency="d")

        # Log-Volatility
        figcount += 1
        plt.figure(figcount)
        plot.plot_for_week(avg_volatility_day_clean, low_volatility_day_clean, upper_volatility_day_clean, name="Volatility", perc=1, weekends=0, logy=1)
        # Log-ILLIQ
        figcount += 1
        plt.figure(figcount)
        plot.plot_for_week(avg_illiq_day_clean, low_illiq_day_clean, upper_illiq_day_clean, name="ILLIQ", perc=1, weekends=0, logy=1)
        # Log-Volumes
        figcount += 1
        plt.figure(figcount)
        plot.plot_for_week(avg_log_volume_day, low_log_volume_day, upper_log_volume_day, name="Volumes (hva gjør vi med denne?)", perc=0, weekends=0)  # Hva faen gjør vi med denne?
        # Spread
        figcount += 1
        plt.figure(figcount)
        plot.plot_for_week(avg_spread_day_clean, low_spread_day_clean, upper_spread_day_clean, name="Spread", perc=1, weekends=0)


plt.show()
