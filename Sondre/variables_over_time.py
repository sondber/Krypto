import data_import as di
import data_import_support as dis
import plot
import numpy as np
import os
import rolls
import ILLIQ
from Jacob import jacob_support as jake_supp

os.chdir("/Users/sondre/Documents/GitHub/krypto")
exchanges, time_list_minutes, prices_minutes, volumes_minutes = di.get_lists(opening_hours="y", make_totals="n")


unedited = 1
minute = 1
day = 1
transformed = 1


# Transformation
time_list_days_clean, time_list_removed, returns_days_clean, volumes_days_clean, log_volumes_days_clean, spread_days_clean, \
illiq_days_clean, log_illiq_days_clean, volatility_days_clean, log_volatility_days_clean = dis.clean_trans_2013(
    time_list_minutes, prices_minutes,
    volumes_minutes)

fig_count = 0

if unedited == 1:
    time_list_days, prices_days, volumes_days = dis.convert_to_day(time_list_minutes, prices_minutes, volumes_minutes)
    time_list_hours, prices_hours, volumes_hours = dis.convert_to_hour(time_list_minutes, prices_minutes,
                                                                       volumes_minutes)
    returns_minutes = jake_supp.logreturn(prices_minutes[0, :])
    returns_days = jake_supp.logreturn(prices_days[0, :])
    spread_days = rolls.rolls(prices_minutes[0, :], time_list_minutes, calc_basis=1, kill_output=1)[1]
    illiq_days = ILLIQ.ILLIQ_nyse_day(prices_hours[0, :], volumes_hours[0, :])
    volatility_days = np.multiply(ILLIQ.daily_Rv(time_list_minutes, prices_minutes[0, :]), 252 ** 0.5)

    if minute == 1:
        fig_count += 1
        plot.plt.figure(fig_count)
        plot.time_series_single(time_list_minutes, prices_minutes[0, :], "Price")
        fig_count += 1
        plot.plt.figure(fig_count)
        plot.time_series_single(time_list_minutes, volumes_minutes[0, :], "Volume")
        fig_count += 1
        plot.plt.figure(fig_count)
        plot.time_series_single(time_list_minutes, returns_minutes, "Return", perc=1)
    if day == 1:
        fig_count += 1
        plot.plt.figure(fig_count)
        plot.time_series_single(time_list_days, prices_days[0, :], "Price")
        fig_count += 1
        plot.plt.figure(fig_count)
        plot.time_series_single(time_list_days, volumes_days[0, :], "Volume")
        fig_count += 1
        plot.plt.figure(fig_count)
        plot.time_series_single(time_list_days, returns_days, "Returns", perc=1)
        fig_count += 1
        plot.plt.figure(fig_count)
        plot.time_series_single(time_list_days, volatility_days, "Realized Volatility", perc=1)
        fig_count += 1
        plot.plt.figure(fig_count)
        plot.time_series_single(time_list_days, spread_days, "Spread", perc=1)
        fig_count += 1
        plot.plt.figure(fig_count)
        plot.time_series_single(time_list_days, illiq_days, "ILLIQ", perc=1)

if transformed == 1:
    fig_count += 1
    plot.plt.figure(fig_count)
    plot.time_series_single(time_list_days_clean, illiq_days_clean, "Log ILLIQ", logy=1, perc=1)
    fig_count += 1
    plot.plt.figure(fig_count)
    plot.time_series_single(time_list_days_clean, volatility_days_clean, "Log volatility", logy=1, perc=1)


plot.plt.show()