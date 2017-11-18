import data_import as di
import data_import_support as dis
import plot
import numpy as np
import os

import realized_volatility
import rolls
import ILLIQ_old
from Jacob import jacob_support as jake_supp

os.chdir("/Users/sondre/Documents/GitHub/krypto")
exchanges, time_list_minutes, prices_minutes, volumes_minutes = di.get_lists(opening_hours="y", make_totals="n")


unedited = 1
minute = 0
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
    illiq_days = ILLIQ_old.ILLIQ_nyse_day(prices_hours[0, :], volumes_hours[0, :])
    volatility_days = np.multiply(realized_volatility.daily_Rvol(time_list_minutes, prices_minutes[0, :]), 252 ** 0.5)

    if minute == 1:
        plot.time_series_single(time_list_minutes, prices_minutes[0, :], "Price")
        plot.time_series_single(time_list_minutes, volumes_minutes[0, :], "Volume")
        plot.time_series_single(time_list_minutes, returns_minutes, "Return", perc=1)
    if day == 1:
        plot.time_series_single(time_list_days, prices_days[0, :], "Price")
        plot.time_series_single(time_list_days, volumes_days[0, :], "Volume")
        plot.time_series_single(time_list_days, returns_days, "Return", perc=1)
        plot.time_series_single(time_list_days, volatility_days, "Realized_Volatility", perc=1)
        plot.time_series_single(time_list_days, spread_days, "Spread", perc=1)
        plot.time_series_single(time_list_days, illiq_days, "ILLIQ", perc=1)

if transformed == 1:
    plot.time_series_single(time_list_days_clean, illiq_days_clean, "Log_ILLIQ", logy=1, perc=1)
    plot.time_series_single(time_list_days_clean, volatility_days_clean, "Log_volatility", logy=1, perc=1)
    plot.time_series_single(time_list_days_clean, log_volumes_days_clean, "Log_volume",  perc=1)
    plot.time_series_single(time_list_days_clean, returns_days_clean, "Return_clean",  perc=1)