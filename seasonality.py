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


intraday = 1
intraweek = 1

exch = [5]

for exc in exch:
    exc_name, time_listM, pricesM, volumesM = di.get_list(exc)
    exc_name = exc_name[0:-3]
    if intraday == 1:
        # HOURS ----------------------------------------------------------------------------------------------------
        print("------ INTRADAY FOR", exc_name.upper(), "------")

        time_listH, returnsH, spreadH, volumesH, log_volumesH, illiqH, log_illiqH, rvolH, log_rvolH= \
            dis.clean_series_hour(time_listM, pricesM, volumesM, exc=exc, convert_time_zones=1)

        print(len(time_listH), len(spreadH), len(rvolH), len(log_rvolH), len(log_illiqH))

        # Finding average for every hour of the day
        hour_of_day, avg_returns_hour, low_returns_hour, upper_returns_hour = dis.cyclical_average(time_listH, returnsH, frequency="h")
        hour_of_day, avg_volumes_hour, low_volumes_hour, upper_volumes_hour = dis.cyclical_average(time_listH, log_volumesH, frequency="h")
        hour_of_day, avg_spread_hour, low_spread_hour, upper_spread_hour = dis.cyclical_average(time_listH, spreadH, frequency="h")
        hour_of_day, avg_rvol_hour, low_rvol_hour, upper_rvol_hour = dis.cyclical_average(time_listH, rvolH, frequency="h")
        #hour_of_day, avg_log_rvol_hour, low_log_rvol_hour, upper_log_rvol_hour = dis.cyclical_average(time_listH, log_rvol_hours, frequency="h")
        hour_of_day, avg_illiq_hour, low_illiq_hour, upper_illiq_hour = dis.cyclical_average(time_listH, illiqH, frequency="h")
        #hour_of_day, avg_log_illiq_hour, low_log_illiq_hour, upper_log_illiq_hour = dis.cyclical_average(illiq_timeH, log_illiq_hours, frequency="h")

        plot.intraday(avg_returns_hour, low_returns_hour, upper_returns_hour, title="Return_" + exc_name, perc=1, ndigits=2, yzero=1)
        plot.intraday(avg_volumes_hour, low_volumes_hour, upper_volumes_hour, title="Log_Volume_" + exc_name, perc=0)
        plot.intraday(avg_spread_hour, low_spread_hour, upper_spread_hour, title="Spread_" + exc_name, perc=1)
        plot.intraday(avg_rvol_hour, low_rvol_hour, upper_rvol_hour, title="RVol_" + exc_name, perc=1, logy=0, ndigits=0)
        plot.intraday(avg_illiq_hour, low_illiq_hour, upper_illiq_hour, title="ILLIQ_" + exc_name, perc=1, ndigits=2)
        #plot.intraday(avg_log_rvol_hour, low_log_rvol_hour, upper_log_rvol_hour, title="Log_RVol" + exc_name, perc=1, logy=1, ndigits=0)
        #plot.intraday(avg_log_illiq_hour, low_log_illiq_hour, upper_log_illiq_hour, title="Log_ILLIQ" + exc_name, perc=0, ndigits=3, logy=0)  # Skulle helst brukt vanlig illiq med log-skala i stedet

    if intraweek == 1:
        print("------ INTRAWEEK", exc_name.upper(), "------")
        # DAYS ----------------------------------------------------------------------------------------------------
        # Converting to daily data
        returns_minutes = jake_supp.logreturn(pricesM)
        time_listD, returnsD, volumesD, log_volumesD, spreadD, illiqD, log_illiqD, rvolD, log_rvolD = dis.clean_series_days(time_listM, pricesM, volumesM, exc=exc, print_days_excluded=0, convert_time_zones=1)

        day_of_week, avg_returns_day, low_returns_day, upper_returns_day = dis.cyclical_average(time_listD, returnsD, frequency="d")
        day_of_week, avg_spread_day, low_spread_day, upper_spread_day = dis.cyclical_average(time_listD, spreadD, frequency="d")
        day_of_week, avg_illiq_day_clean, low_illiq_day_clean, upper_illiq_day_clean = dis.cyclical_average(time_listD, illiqD, frequency="d")
        day_of_week, avg_rvol_day, low_rvol_day, upper_rvol_day = dis.cyclical_average(time_listD, rvolD, frequency="d")
        plot.intraweek(avg_returns_day, low_returns_day, upper_returns_day, title="Return_" + exc_name, perc=1, ndigits=1)
        plot.intraweek(avg_spread_day, low_spread_day, upper_spread_day, title="Spread_" + exc_name, perc=1, ndigits=3)
        plot.intraweek(avg_illiq_day_clean, low_illiq_day_clean, upper_illiq_day_clean, title="ILLIQ_" + exc_name, perc=1,   logy=0, ndigits=3)
        plot.intraweek(avg_rvol_day, low_rvol_day, upper_rvol_day, title="RVol_" + exc_name, perc=1,   logy=0, ndigits=3)

        # Finding average for transformed
        day_of_week, avg_log_volume_day, low_log_volume_day, upper_log_volume_day = dis.cyclical_average(time_listD, log_volumesD, frequency="d")
        #day_of_week, avg_log_rvol_day, low_log_rvol_day, upper_log_rvol_day = dis.cyclical_average(time_listD, log_rvolD, frequency="d")
        #day_of_week, avg_log_illiq_day, low_log_illiq_day, upper_log_illiq_day = dis.cyclical_average(time_listD, log_illiqD, frequency="d")

        #plot.intraweek(avg_log_rvol_day, low_log_rvol_day, upper_log_rvol_day, title="Log_RVol" + exc_name, perc=0,   logy=0, ndigits=0)
        #plot.intraweek(avg_log_illiq_day, low_log_illiq_day, upper_log_illiq_day, title="Log_ILLIQ" + exc_name, perc=0,   logy=0, ndigits=3)
        plot.intraweek(avg_log_volume_day, low_log_volume_day, upper_log_volume_day, title="Log_Volume_" + exc_name, perc=0,weekends=1)  # Hva faen gjør vi med y-aksen på denne?
