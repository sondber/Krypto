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
import math

os.chdir("/Users/sondre/Documents/GitHub/krypto")

intraday = 1
intraweek = 0

exch = [0, 1]  # 0=bitstamp, 1=coincheck

exchanges, time_list_minutes, prices_minutes, volumes_minutes = di.get_lists(opening_hours="n", make_totals="n")


for exc in exch:
    exc_name = "_" + exchanges[exc]
    print()
    print("SEASONALITY FOR", exchanges[exc].upper())
    print()

    if intraday == 1:
        # HOURS ----------------------------------------------------------------------------------------------------

        time_list_hours_clean, returns_hours_clean, spread_hours_clean, log_volumes_hours_clean, illiq_hours_clean, \
        illiq_hours_time, log_illiq_hours_clean, rvol_hours_clean, log_rvol_hours_clean = \
            dis.clean_trans_hours(time_list_minutes, prices_minutes, volumes_minutes, exc=exc, convert_time_zones=1)

        n_hours = 0
        # Finding average for every hour of the day
        hour_of_day, avg_returns_hour, low_returns_hour, upper_returns_hour = dis.cyclical_average(time_list_hours_clean, returns_hours_clean, frequency="h", time_zone_conversion=n_hours)
        hour_of_day, avg_volumes_hour, low_volumes_hour, upper_volumes_hour = dis.cyclical_average(time_list_hours_clean, log_volumes_hours_clean,frequency="h", time_zone_conversion=n_hours)
        hour_of_day, avg_spread_hour, low_spread_hour, upper_spread_hour = dis.cyclical_average(time_list_hours_clean, spread_hours_clean, frequency="h", time_zone_conversion=n_hours)
        hour_of_day, avg_rvol_hour, low_rvol_hour, upper_rvol_hour = dis.cyclical_average(time_list_hours_clean, rvol_hours_clean, frequency="h", time_zone_conversion=n_hours)
        hour_of_day, avg_illiq_hour, low_illiq_hour, upper_illiq_hour = dis.cyclical_average(illiq_hours_time, log_illiq_hours_clean, frequency="h", time_zone_conversion=n_hours)

        plot.plot_for_day(avg_returns_hour, low_returns_hour, upper_returns_hour, title="Return"+exc_name, perc=1, ndigits=2, yzero=1)
        plot.plot_for_day(avg_volumes_hour, low_volumes_hour, upper_volumes_hour, title="Log_Volume"+exc_name, perc=0)
        plot.plot_for_day(avg_spread_hour, low_spread_hour, upper_spread_hour, title="Spread"+exc_name, perc=1)
        plot.plot_for_day(avg_rvol_hour, low_rvol_hour, upper_rvol_hour, title="Log_RVol"+exc_name, perc=1, logy=1, ndigits=0)
        plot.plot_for_day(avg_illiq_hour, low_illiq_hour, upper_illiq_hour, title="Log_ILLIQ"+exc_name, perc=0, ndigits=3, logy=0)  # Skulle helst brukt vanlig illiq med log-skala i stedet

    if intraweek == 1:
        # DAYS ----------------------------------------------------------------------------------------------------
        # Converting to daily data
        time_list_days, prices_days, volumes_days = dis.convert_to_day(time_list_minutes, prices_minutes, volumes_minutes)
        returns_minutes = jake_supp.logreturn(prices_minutes[exc, :])
        time_list_days_clean, time_list_removed, returns_days_clean, volumes_days_clean, log_volumes_days_clean, spread_days_clean, \
        illiq_days_clean, log_illiq_days_clean, volatility_days_clean, log_volatility_days_clean = dis.clean_trans_days(
            time_list_minutes, prices_minutes,
            volumes_minutes, full_week=1, exc=exc)

        spread_days_raw = rolls.rolls(prices_minutes[exc, :], time_list_minutes, calc_basis=1, kill_output=1)[1]  # Rolls
        returns_days_raw = jake_supp.logreturn(prices_days[exc, :])
        illiq_days_time, illiq_days_raw = ILLIQ.illiq(time_list_minutes, returns_minutes, volumes_minutes[exc, :], hourly_or_daily=1)


        # Finding average for raw variables
        #day_of_week, avg_returns_day_raw, low_returns_day_raw, upper_returns_day_raw = dis.cyclical_average(time_list_days, returns_days_raw, frequency="d", time_zone_conversion=n_hours)
        #day_of_week, avg_volumes_day_raw, low_volumes_day_raw, upper_volumes_day_raw = dis.cyclical_average(time_list_days, volumes_days[exc,:], frequency="d", time_zone_conversion=n_hours)
        #day_of_week, avg_spread_day_raw, low_spread_day_raw, upper_spread_day_raw = dis.cyclical_average(time_list_days, spread_days_raw, frequency="d", time_zone_conversion=n_hours)
        #day_of_week, avg_illiq_day_raw, low_illiq_day_raw, upper_illiq_day_raw = dis.cyclical_average(illiq_days_time, illiq_days_raw,frequency="d", time_zone_conversion=n_hours)

        #plot.plot_for_week(avg_returns_day_raw, low_returns_day_raw, upper_returns_day_raw, title="Return_raw"+exc_name, perc=1, ndigits=1)
        #plot.plot_for_week(avg_volumes_day_raw, low_volumes_day_raw, upper_volumes_day_raw, title="Volume_raw"+exc_name, perc=0)
        #plot.plot_for_week(avg_spread_day_raw, low_spread_day_raw, upper_spread_day_raw, title="Spread_raw"+exc_name, perc=1)
        #plot.plot_for_week(avg_illiq_day_raw, low_illiq_day_raw, upper_illiq_day_raw, title="ILLIQ_raw"+exc_name, perc=1, ndigits=3)


        # Finding average for clean variables
        day_of_week, avg_returns_day, low_returns_day, upper_returns_day = dis.cyclical_average(time_list_days_clean,
                                                                                                returns_days_clean,
                                                                                                frequency="d", time_zone_conversion=n_hours)
        #day_of_week, avg_volumes_day, low_volumes_day, upper_volumes_day = dis.cyclical_average(time_list_days_clean,
        #                                                                                        volumes_days_clean,
        #                                                                                        frequency="d", time_zone_conversion=n_hours)
        day_of_week, avg_spread_day, low_spread_day, upper_spread_day = dis.cyclical_average(time_list_days_clean, spread_days_clean,
                                                                                             frequency="d", time_zone_conversion=n_hours)
        #day_of_week, avg_illiq_day, low_illiq_day, upper_illiq_day = dis.cyclical_average(time_list_days_clean, illiq_days_clean,
        #                                                                                  frequency="d", time_zone_conversion=n_hours)
        #day_of_week, avg_volatility_day, low_volatility_day, upper_volatility_day = dis.cyclical_average(time_list_days_clean, volatility_days_clean,
        #                                                                                     frequency="d", time_zone_conversion=n_hours)

        plot.plot_for_week(avg_returns_day, low_returns_day, upper_returns_day, title="Return_clean"+exc_name, perc=1, ndigits=1)
        #plot.plot_for_week(avg_volumes_day, low_volumes_day, upper_volumes_day, title="Volume_clean"+exc_name, perc=0)
        plot.plot_for_week(avg_spread_day, low_spread_day, upper_spread_day, title="Spread_clean"+exc_name, perc=1)
        #plot.plot_for_week(avg_volatility_day, low_volatility_day, upper_volatility_day, title="Volatility_clean"+exc_name, perc=1, ndigits=0, logy=0)
        #plot.plot_for_week(avg_illiq_day, low_illiq_day, upper_illiq_day, title="ILLIQ_clean"+exc_name, perc=1, ndigits=3, logy=0)

        #Finding average for transformed
        day_of_week, avg_log_volume_day, low_log_volume_day, upper_log_volume_day = dis.cyclical_average(
            time_list_days_clean, log_volumes_days_clean, frequency="d", time_zone_conversion=n_hours)
        day_of_week, avg_volatility_day_clean, low_volatility_day_clean, upper_volatility_day_clean = dis.cyclical_average(
            time_list_days_clean, volatility_days_clean, frequency="d", time_zone_conversion=n_hours)
        day_of_week, avg_illiq_day_clean, low_illiq_day_clean, upper_illiq_day_clean = dis.cyclical_average(
            time_list_days_clean, illiq_days_clean, frequency="d", time_zone_conversion=n_hours)
        day_of_week, avg_spread_day_clean, low_spread_day_clean, upper_spread_day_clean = dis.cyclical_average(
            time_list_days_clean, spread_days_clean, frequency="d", time_zone_conversion=n_hours)

        plot.plot_for_week(avg_volatility_day_clean, low_volatility_day_clean, upper_volatility_day_clean,
                           title="Log_Volatility"+exc_name, perc=1, weekends=1, logy=1, ndigits=0)
        plot.plot_for_week(avg_illiq_day_clean, low_illiq_day_clean, upper_illiq_day_clean, title="Log_ILLIQ"+exc_name, perc=1,
                           weekends=1, logy=1, ndigits=3)
        plot.plot_for_week(avg_log_volume_day, low_log_volume_day, upper_log_volume_day, title="Log_Volume"+exc_name, perc=0,
                           weekends=1)  # Hva faen gjør vi med y-aksen på denne?
        plot.plot_for_week(avg_spread_day_clean, low_spread_day_clean, upper_spread_day_clean, title="Spread_clean"+exc_name,
                           perc=1, weekends=1)


