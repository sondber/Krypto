import data_import as di
import data_import_support as dis
import plot
import numpy as np
import os
import realized_volatility
import rolls
import ILLIQ
from Jacob import jacob_support as jake_supp

os.chdir("/Users/sondre/Documents/GitHub/krypto")

exchanges, time_list_minutes, prices_minutes, volumes_minutes = di.get_lists(opening_hours="n", make_totals="n")
exc = 1  #  0=bitstamp, 1=coincheck
exc_name = "_" + exchanges[exc]

unedited = 1
transformed = 1

# Transformation
time_list_days_clean, time_list_removed, returns_days_clean, volumes_days_clean, log_volumes_days_clean, spread_days_clean, \
illiq_days_clean, log_illiq_days_clean, volatility_days_clean, log_volatility_days_clean = dis.clean_trans_days(
    time_list_minutes, prices_minutes, volumes_minutes, full_week=1, exchange=exc)

if unedited == 1:
    time_list_days, prices_days, volumes_days = dis.convert_to_day(time_list_minutes, prices_minutes, volumes_minutes)
    time_list_hours, prices_hours, volumes_hours = dis.convert_to_hour(time_list_minutes, prices_minutes,
                                                                       volumes_minutes)
    returns_minutes = jake_supp.logreturn(prices_minutes[exc, :])
    returns_days = jake_supp.logreturn(prices_days[exc, :])

    spread_days = rolls.rolls(prices_minutes[exc, :], time_list_minutes, calc_basis=1, kill_output=1)[1]
    illiq_days_time, illiq_days = ILLIQ.illiq(time_list_minutes, returns_minutes, volumes_minutes[exc, :], day_or_hour=1)

    # Realized volatility
    volatility_days, rVol_time = realized_volatility.daily_Rvol(time_list_minutes, prices_minutes[0, :])
    # Annualize the volatility
    volatility_days = np.multiply(volatility_days, 365 ** 0.5)


    plot.time_series_single(time_list_days, prices_days[exc, :], "Price"+exc_name)
    #plot.time_series_single(time_list_days, volumes_days[exc, :], "Volume"+exc_name)
    #plot.time_series_single(time_list_days, returns_days, "Return"+exc_name, perc=1, ndigits=0)
    #plot.time_series_single(time_list_days, volatility_days, "Realized_Volatility"+exc_name, perc=1, ndigits=0)
    #plot.time_series_single(time_list_days, volatility_days, "Realized_Volatility_cut"+exc_name, perc=1, ndigits=0, ylims=[0,5])
    #plot.time_series_single(time_list_days, spread_days, "Spread"+exc_name, perc=1, ndigits=1)
    #plot.time_series_single(time_list_days, spread_days, "Spread_cut"+exc_name, perc=1, ndigits=1, ylims=[0,0.015])
    #plot.time_series_single(time_list_days, illiq_days, "ILLIQ"+exc_name, perc=1, ndigits=1)
    #plot.time_series_single(time_list_days, illiq_days, "ILLIQ_cut"+exc_name, perc=1, ndigits=1, ylims=[0, 0.002])

if transformed == 1:
    plot.time_series_single(time_list_days_clean, illiq_days_clean, "Log_ILLIQ"+exc_name, logy=1, perc=1, ndigits=3)
    plot.time_series_single(time_list_days_clean, volatility_days_clean, "Log_volatility"+exc_name, logy=1, perc=1, ndigits=0)
    plot.time_series_single(time_list_days_clean, log_volumes_days_clean, "Log_volume"+exc_name,  perc=0)
    plot.time_series_single(time_list_days_clean, spread_days_clean, "Spread_clean"+exc_name, perc=1, ndigits=1)
    plot.time_series_single(time_list_days_clean, returns_days_clean, "Return_clean"+exc_name,  perc=1, ndigits=0)