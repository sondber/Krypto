import numpy as np
import data_import as di
import plot
from Jacob import jacob_support as jake_supp
from Sondre import sondre_support_formulas as supp
from matplotlib import pyplot as plt
import data_import_support as dis
import os
import rolls
import scipy.stats as st
import global_volume_index as gvi
import ILLIQ
import realized_volatility
import math


intraday = 1
figure_formats = "narrow"
intraweek = 0
global_volume_index = 0
global_time = 0
exch = ["bitstamp", "coinbase", "btcn", "korbit"]

for exc in exch:
    if intraday == 1:
        for local_time in [0, 1]:
            # HOURS ----------------------------------------------------------------------------------------------------

            if local_time == 1:
                folder = figure_formats + "/local_time/"
            else:
                folder = figure_formats + "/global_time/"

            exc_name, time_listH, returnsH, spreadH, volumesH, log_volumesH, illiqH, log_illiqH, rvolH, log_rvolH = di.get_list(exc=exc, freq="h", local_time=local_time)
            print("------ INTRADAY FOR", exc_name.upper(), "------")

            # Finding average for every hour of the day
            hour_of_day, avg_returns_hour, low_returns_hour, upper_returns_hour = dis.cyclical_average(time_listH, returnsH, frequency="h")
            hour_of_day, avg_volumes_hour, low_volumes_hour, upper_volumes_hour = dis.cyclical_average(time_listH, log_volumesH, frequency="h")
            hour_of_day, avg_spread_hour, low_spread_hour, upper_spread_hour = dis.cyclical_average(time_listH, spreadH, frequency="h")
            hour_of_day, avg_rvol_hour, low_rvol_hour, upper_rvol_hour = dis.cyclical_average(time_listH, rvolH, frequency="h")
            hour_of_day, avg_illiq_hour, low_illiq_hour, upper_illiq_hour = dis.cyclical_average(time_listH, illiqH, frequency="h")

            title = folder + "Return_" + exc_name
            plot.intraday(avg_returns_hour, low_returns_hour, upper_returns_hour, title=title, perc=1, ndigits=2, yzero=1, fig_format=figure_formats)
            title = folder + "Log_Volumes_" + exc_name
            plot.intraday(avg_volumes_hour, low_volumes_hour, upper_volumes_hour, title=title, perc=0, fig_format=figure_formats)
            title = folder + "Spread_" + exc_name
            plot.intraday(avg_spread_hour, low_spread_hour, upper_spread_hour, title=title, perc=1, fig_format=figure_formats)
            title = folder + "RVol_" + exc_name
            plot.intraday(avg_rvol_hour, low_rvol_hour, upper_rvol_hour, title=title, perc=1, logy=0, ndigits=0, fig_format=figure_formats)
            title = folder + "illiq_" + exc_name
            plot.intraday(avg_illiq_hour, low_illiq_hour, upper_illiq_hour, title=title, perc=1, ndigits=2, fig_format=figure_formats)

    if intraweek == 1:

        # DAYS ----------------------------------------------------------------------------------------------------
        # Converting to daily data
        exc_name, time_listD, returnsD, volumesD, log_volumesD, spreadD, illiqD, log_illiqD, rvolD, log_rvolD = di.get_list(exc=exc, freq="d")
        print("------ INTRAWEEK", exc_name.upper(), "------")

        day_of_week, avg_returns_day, low_returns_day, upper_returns_day = dis.cyclical_average(time_listD, returnsD, frequency="d")
        day_of_week, avg_spread_day, low_spread_day, upper_spread_day = dis.cyclical_average(time_listD, spreadD, frequency="d")
        day_of_week, avg_illiq_day_clean, low_illiq_day_clean, upper_illiq_day_clean = dis.cyclical_average(time_listD, illiqD, frequency="d")
        day_of_week, avg_rvol_day, low_rvol_day, upper_rvol_day = dis.cyclical_average(time_listD, rvolD, frequency="d")
        plot.intraweek(avg_returns_day, low_returns_day, upper_returns_day, title="Return_" + exc_name, perc=1, ndigits=1, fig_format=figure_formats)
        plot.intraweek(avg_spread_day, low_spread_day, upper_spread_day, title="Spread_" + exc_name, perc=1, ndigits=3, fig_format=figure_formats)
        plot.intraweek(avg_illiq_day_clean, low_illiq_day_clean, upper_illiq_day_clean, title="ILLIQ_" + exc_name, perc=1,   logy=0, ndigits=3, fig_format=figure_formats)
        plot.intraweek(avg_rvol_day, low_rvol_day, upper_rvol_day, title="RVol_" + exc_name, perc=1,   logy=0, ndigits=3, fig_format=figure_formats)

        # Finding average for transformed
        day_of_week, avg_log_volume_day, low_log_volume_day, upper_log_volume_day = dis.cyclical_average(time_listD, log_volumesD, frequency="d")
        plot.intraweek(avg_log_volume_day, low_log_volume_day, upper_log_volume_day, title="Log_Volume_" + exc_name, perc=0,weekends=1, fig_format=figure_formats)  # Hva faen gjør vi med y-aksen på denne?

if global_volume_index == 1:
    time_H, volume_indexH = gvi.get_global_hourly_volume_index(transformed=1)
    hour_of_day, avg_volumes_hour, low_volumes_hour, upper_volumes_hour = dis.cyclical_average(time_H, volume_indexH, frequency="h")
    title = "Log_Volumes_Global_index"
    plot.intraday(avg_volumes_hour, low_volumes_hour, upper_volumes_hour, title=title, perc=0, fig_format="wide")



exch = [0, 1, 3, 4, 5]
if global_time == 1:
    for exc in exch:
        exc_name, time_listH, returnsH, spreadH, volumesH, log_volumesH, illiqH, log_illiqH, rvolH, log_rvolH = di.get_list(
            exc=exc, freq=1, local_time=0)

        hour_of_day, avg_volumes_hour, low_volumes_hour, upper_volumes_hour = dis.cyclical_average(time_listH, volumesH, frequency="h")
        hour_of_day, avg_spread_hour, low_spread_hour, upper_spread_hour = dis.cyclical_average(time_listH, spreadH, frequency="h")

        spread_std = (avg_spread_hour - np.mean(avg_spread_hour))/(max(avg_spread_hour)-min(avg_spread_hour))
        volumes_std = (avg_volumes_hour - np.mean(avg_volumes_hour))/(max(avg_volumes_hour)-min(avg_volumes_hour))
        spread = avg_spread_hour
        volumes = avg_volumes_hour

        if exc == 0:
            marker = "s"
            color = "black"
        elif exc == 1:
            marker = "x"
            color = "blue"
        elif exc == 2:
            marker = "o"
            color = "blue"
        elif exc == 3:
            marker = "v"
            color = "black"
        elif exc == 4:
            marker = "+"
            color = "blue"
        elif exc == 5:
            marker = "p"
            color = "black"

        plt.figure(1, figsize=[16, 4], dpi=300)
        plt.plot(spread_std, label=exc_name, color=color, marker=marker)
        plt.figure(2, figsize=[16, 4], dpi=300)
        plt.plot(spread, label=exc_name, color=color, marker=marker)
        plt.figure(3, figsize=[16, 4], dpi=300)
        plt.plot(volumes_std, label=exc_name, color=color, marker=marker)
        plt.figure(4, figsize=[16, 4], dpi=300)
        plt.plot(volumes, label=exc_name, color=color, marker=marker)

    title1 = "intraday_spread_std"
    title2 = "intraday_spread"
    title3 = "intraday_volumes_std"
    title4 = "intraday_volumes"

    location1 = "figures/seasonality/global/" + title1 + ".png"
    location2 = "figures/seasonality/global/" + title2 + ".png"
    location3 = "figures/seasonality/global/" + title3 + ".png"
    location4 = "figures/seasonality/global/" + title4 + ".png"


    plt.figure(1, figsize=[16, 4], dpi=300)
    plt.legend()
    plt.xlim([0, 23])
    plt.savefig(location1)

    plt.figure(2, figsize=[16, 4], dpi=300)
    plt.legend()
    plt.xlim([0, 23])
    plt.savefig(location2)

    plt.figure(3, figsize=[16, 4], dpi=300)
    plt.legend()
    plt.xlim([0, 23])
    plt.savefig(location3)

    plt.figure(4, figsize=[16, 4], dpi=300)
    plt.legend()
    plt.xlim([0, 23])
    plt.savefig(location4)
