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

hours = 1
days = 1
# daily
full_week = 1
weekdays = 1

exc = 0  #  0=bitstamp, 1=coincheck

if full_week== 1 or hours==1:
    exchanges, time_list_minutes, prices_minutes, volumes_minutes = di.get_lists(opening_hours="n", make_totals="n")
    exc_name = "_" + exchanges[exc]

    returns_minutes = jake_supp.logreturn(prices_minutes[0, :])
    # Converting to hourly data
    time_list_hours, prices_hours, volumes_hours = dis.convert_to_hour(time_list_minutes, prices_minutes, volumes_minutes)
    volumes_hours = volumes_hours[exc, :]
    time_list_days, prices_days, volumes_days = dis.convert_to_day(time_list_minutes, prices_minutes, volumes_minutes)

if hours == 1:
    # HOURS ----------------------------------------------------------------------------------------------------
    returns_hours = jake_supp.logreturn(prices_hours[exc, :])
    spread_hours = rolls.rolls(prices_minutes[exc, :], time_list_minutes, calc_basis=0, kill_output=0)[1]  # Rolls
    illiq_hours_time, illiq_hours = ILLIQ.illiq(time_list_minutes, returns_minutes, volumes_minutes[exc, :], day_or_hour=0)

    if exc == 0:
        cutoff_hour = 8784  # 2012
        illiq_cutoff = cutoff_hour
    elif exc == 1:
        cutoff_hour = 26304 # 2012-2015
        illiq_cutoff = 539
    else:
        print("Choose an exchange!")

    total_hours = len(time_list_hours)-1
    time_list_hours = time_list_hours[cutoff_hour:total_hours]
    returns_hours = returns_hours[cutoff_hour:total_hours]
    volumes_hours = volumes_hours[cutoff_hour:total_hours]
    spread_hours = spread_hours[cutoff_hour:total_hours]
    illiq_hours = illiq_hours[illiq_cutoff:len(illiq_hours)-1]
    illiq_hours_time = illiq_hours_time[illiq_cutoff:len(illiq_hours)-1]

    if exc == 0:
        hours_to_remove = [2393, 2410, 17228, 26712, 30468, 33819]
    else:
        hours_to_remove = [318, 1503, 1504, 7389, 12674, 12890, 17649, 17653, 21022, 21052, 21053,  25726]

    time_list_hours = np.delete(time_list_hours, hours_to_remove)
    returns_hours = np.delete(returns_hours, hours_to_remove)
    volumes_hours = np.delete(volumes_hours, hours_to_remove)
    spread_hours = np.delete(spread_hours, hours_to_remove)
    illiq_hours = np.delete(illiq_hours, hours_to_remove)
    illiq_hours_time = np.delete(illiq_hours_time, hours_to_remove)


    # Finding average for every hour of the day
    hour_of_day, avg_returns_hour, low_returns_hour, upper_returns_hour = dis.cyclical_average(time_list_hours, returns_hours, frequency="h")
    hour_of_day, avg_volumes_hour, low_volumes_hour, upper_volumes_hour = dis.cyclical_average(time_list_hours, volumes_hours,frequency="h")
    hour_of_day, avg_spread_hour, low_spread_hour, upper_spread_hour = dis.cyclical_average(time_list_hours, spread_hours, frequency="h")
    hour_of_day, avg_illiq_hour, low_illiq_hour, upper_illiq_hour = dis.cyclical_average(illiq_hours_time, illiq_hours, frequency="h")

    plot.plot_for_day(avg_returns_hour, low_returns_hour, upper_returns_hour, title="Return"+exc_name, perc=1, ndigits=2, yzero=1)
    plot.plot_for_day(avg_volumes_hour, low_volumes_hour, upper_volumes_hour, title="Volume"+exc_name, perc=0)
    plot.plot_for_day(avg_spread_hour, low_spread_hour, upper_spread_hour, title="Spread"+exc_name, perc=1)
    plot.plot_for_day(avg_illiq_hour, low_illiq_hour, upper_illiq_hour, title="ILLIQ"+exc_name, perc=1, ndigits=3)

if days == 1:
    # DAYS ----------------------------------------------------------------------------------------------------
    # Converting to daily data
    time_list_days_clean, time_list_removed, returns_days_clean, volumes_days_clean, log_volumes_days_clean, spread_days_clean, \
    illiq_days_clean, log_illiq_days_clean, volatility_days_clean, log_volatility_days_clean = dis.clean_trans_days(
        time_list_minutes, prices_minutes,
        volumes_minutes, full_week=1, exchange=exc)

    spread_days_raw = rolls.rolls(prices_minutes[exc, :], time_list_minutes, calc_basis=1, kill_output=1)[1]  # Rolls
    returns_days_raw = jake_supp.logreturn(prices_days[exc, :])
    illiq_days_time, illiq_days_raw = ILLIQ.illiq(time_list_minutes, returns_minutes, volumes_minutes[exc, :], day_or_hour=1)


    # Finding average for raw variables
    #day_of_week, avg_returns_day_raw, low_returns_day_raw, upper_returns_day_raw = dis.cyclical_average(time_list_days, returns_days_raw, frequency="d")
    #day_of_week, avg_volumes_day_raw, low_volumes_day_raw, upper_volumes_day_raw = dis.cyclical_average(time_list_days, volumes_days[exc,:], frequency="d")
    #day_of_week, avg_spread_day_raw, low_spread_day_raw, upper_spread_day_raw = dis.cyclical_average(time_list_days, spread_days_raw, frequency="d")
    #day_of_week, avg_illiq_day_raw, low_illiq_day_raw, upper_illiq_day_raw = dis.cyclical_average(illiq_days_time, illiq_days_raw,frequency="d")

    #plot.plot_for_week(avg_returns_day_raw, low_returns_day_raw, upper_returns_day_raw, title="Return_raw"+exc_name, perc=1, ndigits=1)
    #plot.plot_for_week(avg_volumes_day_raw, low_volumes_day_raw, upper_volumes_day_raw, title="Volume_raw"+exc_name, perc=0)
    #plot.plot_for_week(avg_spread_day_raw, low_spread_day_raw, upper_spread_day_raw, title="Spread_raw"+exc_name, perc=1)
    #plot.plot_for_week(avg_illiq_day_raw, low_illiq_day_raw, upper_illiq_day_raw, title="ILLIQ_raw"+exc_name, perc=1, ndigits=3)


    # Finding average for clean variables
    day_of_week, avg_returns_day, low_returns_day, upper_returns_day = dis.cyclical_average(time_list_days_clean,
                                                                                            returns_days_clean,
                                                                                            frequency="d")
    #day_of_week, avg_volumes_day, low_volumes_day, upper_volumes_day = dis.cyclical_average(time_list_days_clean,
    #                                                                                        volumes_days_clean,
    #                                                                                        frequency="d")
    day_of_week, avg_spread_day, low_spread_day, upper_spread_day = dis.cyclical_average(time_list_days_clean, spread_days_clean,
                                                                                         frequency="d")
    #day_of_week, avg_illiq_day, low_illiq_day, upper_illiq_day = dis.cyclical_average(time_list_days_clean, illiq_days_clean,
    #                                                                                  frequency="d")
    #day_of_week, avg_volatility_day, low_volatility_day, upper_volatility_day = dis.cyclical_average(time_list_days_clean, volatility_days_clean,
    #                                                                                     frequency="d")

    plot.plot_for_week(avg_returns_day, low_returns_day, upper_returns_day, title="Return_clean"+exc_name, perc=1, ndigits=1)
    #plot.plot_for_week(avg_volumes_day, low_volumes_day, upper_volumes_day, title="Volume_clean"+exc_name, perc=0)
    plot.plot_for_week(avg_spread_day, low_spread_day, upper_spread_day, title="Spread_clean"+exc_name, perc=1)
    #plot.plot_for_week(avg_volatility_day, low_volatility_day, upper_volatility_day, title="Volatility_clean"+exc_name, perc=1, ndigits=0, logy=0)
    #plot.plot_for_week(avg_illiq_day, low_illiq_day, upper_illiq_day, title="ILLIQ_clean"+exc_name, perc=1, ndigits=3, logy=0)

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
                       title="Log_Volatility"+exc_name, perc=1, weekends=1, logy=1, ndigits=0)
    plot.plot_for_week(avg_illiq_day_clean, low_illiq_day_clean, upper_illiq_day_clean, title="Log_ILLIQ"+exc_name, perc=1,
                       weekends=1, logy=1, ndigits=3)
    plot.plot_for_week(avg_log_volume_day, low_log_volume_day, upper_log_volume_day, title="Log_Volume"+exc_name, perc=0,
                       weekends=1)  # Hva faen gjør vi med y-aksen på denne?
    plot.plot_for_week(avg_spread_day_clean, low_spread_day_clean, upper_spread_day_clean, title="Spread_clean"+exc_name,
                       perc=1, weekends=1)


