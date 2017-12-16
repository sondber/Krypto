import numpy as np
import data_import as di
import plot
from Jacob import jacob_support as jake_supp
from Sondre import sondre_support_formulas as supp
import data_import_support as dis
import os
import rolls
import scipy.stats as st
import ILLIQ
import realized_volatility

os.chdir("/Users/sondre/Documents/GitHub/krypto")

hours = 0
days = 1
# daily
full_week = 1
weekdays = 1

if full_week== 1 or hours==1:
    exchanges, time_list_minutes, prices_minutes, volumes_minutes = di.get_lists(opening_hours="n", make_totals="n")

    returns_minutes = jake_supp.logreturn(prices_minutes[0, :])
    # Converting to hourly data
    time_list_hours, prices_hours, volumes_hours = dis.convert_to_hour(time_list_minutes, prices_minutes, volumes_minutes)



if hours == 1:
    # HOURS ----------------------------------------------------------------------------------------------------
    returns_hours = jake_supp.logreturn(prices_hours[0, :])
    spread_hours = rolls.rolls(prices_minutes[0, :], time_list_minutes, calc_basis=0, kill_output=1)[1]  # Rolls
    illiq_hours_time, illiq_hours = ILLIQ.illiq(time_list_minutes, returns_minutes, volumes_minutes[0, :], day_or_hour=0)

    # Finding average for every hour of the day
    hour_of_day, avg_returns_hour, low_returns_hour, upper_returns_hour = dis.cyclical_average(time_list_hours, returns_hours, frequency="h")
    hour_of_day, avg_volumes_hour, low_volumes_hour, upper_volumes_hour = dis.cyclical_average(time_list_hours, volumes_hours[0, :],frequency="h")
    hour_of_day, avg_spread_hour, low_spread_hour, upper_spread_hour = dis.cyclical_average(time_list_hours, spread_hours, frequency="h")
    hour_of_day, avg_illiq_hour, low_illiq_hour, upper_illiq_hour = dis.cyclical_average(illiq_hours_time, illiq_hours, frequency="h")

    plot.plot_for_day(avg_returns_hour, low_returns_hour, upper_returns_hour, title="Return", perc=1, ndigits=1, yzero=1)
    plot.plot_for_day(avg_volumes_hour, low_volumes_hour, upper_volumes_hour, title="Volume", perc=0)
    plot.plot_for_day(avg_spread_hour, low_spread_hour, upper_spread_hour, title="Spread", perc=1)
    plot.plot_for_day(avg_illiq_hour, low_illiq_hour, upper_illiq_hour, title="ILLIQ", perc=1, ndigits=3)

if days == 1:
    # DAYS ----------------------------------------------------------------------------------------------------
    # Converting to daily data
    time_list_days_clean, time_list_removed, returns_days_clean, volumes_days_clean, log_volumes_days_clean, spread_days_clean, \
    illiq_days_clean, log_illiq_days_clean, volatility_days_clean, log_volatility_days_clean = dis.clean_trans_2013(
        time_list_minutes, prices_minutes,
        volumes_minutes, full_week=1)

    """
    # Finding average for every day of the week
    day_of_week, avg_returns_day, low_returns_day, upper_returns_day = dis.cyclical_average(time_list_days_clean,
                                                                                            returns_days_clean,
                                                                                            frequency="d")
    day_of_week, avg_volumes_day, low_volumes_day, upper_volumes_day = dis.cyclical_average(time_list_days_clean,
                                                                                            volumes_days_clean,
                                                                                            frequency="d")
    day_of_week, avg_spread_day, low_spread_day, upper_spread_day = dis.cyclical_average(time_list_days_clean, spread_days_clean,
                                                                                         frequency="d")
    day_of_week, avg_illiq_day, low_illiq_day, upper_illiq_day = dis.cyclical_average(time_list_days_clean, illiq_days_clean,
                                                                                      frequency="d")
    day_of_week, avg_volatility_day, low_volatility_day, upper_volatility_day = dis.cyclical_average(time_list_days_clean, volatility_days_clean,
                                                                                         frequency="d")


    plot.plot_for_week(avg_returns_day, low_returns_day, upper_returns_day, title="Return", perc=1, ndigits=1)
    plot.plot_for_week(avg_volumes_day, low_volumes_day, upper_volumes_day, title="Volume", perc=0)
    plot.plot_for_week(avg_spread_day, low_spread_day, upper_spread_day, title="Spread", perc=1)
    plot.plot_for_week(avg_volatility_day, low_volatility_day, upper_volatility_day, title="Volatility", perc=1, ndigits=0, logy=1)
    plot.plot_for_week(avg_illiq_day, low_illiq_day, upper_illiq_day, title="ILLIQ", perc=1, ndigits=3, logy=1)
    """

    #Finding average for transformed
    day_of_week, avg_log_volume_day, low_log_volume_day, upper_log_volume_day = dis.cyclical_average(
        time_list_days_clean, log_volumes_days_clean, frequency="d")
    day_of_week, avg_volatility_day_clean, low_volatility_day_clean, upper_volatility_day_clean = dis.cyclical_average(
        time_list_days_clean, volatility_days_clean, frequency="d")
    day_of_week, avg_illiq_day_clean, low_illiq_day_clean, upper_illiq_day_clean = dis.cyclical_average(
        time_list_days_clean, illiq_days_clean, frequency="d")
    day_of_week, avg_spread_day_clean, low_spread_day_clean, upper_spread_day_clean = dis.cyclical_average(
        time_list_days_clean, spread_days_clean, frequency="d")


    plot.plot_for_week(avg_volatility_day_clean, low_volatility_day_clean, upper_volatility_day_clean,
                       title="Log_Volatility", perc=1, weekends=1, logy=1, ndigits=1)
    plot.plot_for_week(avg_illiq_day_clean, low_illiq_day_clean, upper_illiq_day_clean, title="Log_ILLIQ", perc=1,
                       weekends=1, logy=1, ndigits=3)
    plot.plot_for_week(avg_log_volume_day, low_log_volume_day, upper_log_volume_day, title="Log_Volume", perc=0,
                       weekends=1)  # Hva faen gjør vi med y-aksen på denne?
    plot.plot_for_week(avg_spread_day_clean, low_spread_day_clean, upper_spread_day_clean, title="Spread_clean",
                       perc=1, weekends=1)
