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

exchanges, time_listM, pricesM, volumesM = di.get_lists_legacy(opening_hours="n", make_totals="n")
exc = 2  #  0=bitstamp, 1=coincheck
exc_name = "_" + exchanges[exc]

unedited = 0
transformed = 1

# Transformation
time_listD, time_list_removed, returnsD, volumesD, log_volumesD, spreadD, illiqD, log_illiqD, rvolD, log_rvolD = dis.clean_series_days(time_listM, pricesM, volumesM, exc=exc)

if unedited == 1:
    time_listD_raw, pricesD_raw, volumesD_raw = dis.convert_to_day(time_listM, pricesM, volumesM)
    time_listH_raw, pricesH_raw, volumesH_raw = dis.convert_to_hour(time_listM, pricesM, volumesM)
    returnsM_raw = jake_supp.logreturn(pricesM[exc, :])
    returnsD_raw = jake_supp.logreturn(pricesD_raw[exc, :])

    spreadD_raw = rolls.rolls(pricesM[exc, :], time_listM, calc_basis=1, kill_output=1)[1]
    illiq_timeD, illiqD_raw = ILLIQ.illiq(time_listM, returnsM_raw, volumesM[exc, :], hourly_or_daily=1)

    # Realized volatility
    volatility_days, rVol_time = realized_volatility.RVol(time_listM, pricesM[exc, :], daily=1, annualize=1)

    plot.time_series_single(time_listD_raw, pricesD_raw[exc, :], "Price" + exc_name)
    plot.time_series_single(time_listD_raw, volumesD_raw[exc, :], "Volume" + exc_name)
    plot.time_series_single(time_listD_raw, returnsD_raw, "Return" + exc_name, perc=1, ndigits=0)
    plot.time_series_single(time_listD_raw, volatility_days, "Realized_Volatility"+exc_name, perc=1, ndigits=0)
    #plot.time_series_single(time_listD_raw, volatility_days, "Realized_Volatility_cut"+exc_name, perc=1, ndigits=0, ylims=[0,5])
    plot.time_series_single(time_listD_raw, spreadD_raw, "Spread" + exc_name, perc=1, ndigits=1)
    #plot.time_series_single(time_listD_raw, spreadD_raw, "Spread_cut" + exc_name, perc=1, ndigits=1, ylims=[0, 0.015])
    plot.time_series_single(time_listD_raw, illiqD_raw, "ILLIQ" + exc_name, perc=1, ndigits=1)
    #plot.time_series_single(time_listD_raw, illiqD_raw, "ILLIQ_cut" + exc_name, perc=1, ndigits=1, ylims=[0, 0.002])

if transformed == 1:
    plot.time_series_single(time_listD, illiqD, "Log_ILLIQ"+exc_name, logy=1, perc=1, ndigits=3)
    plot.time_series_single(time_listD, rvolD, "Log_volatility"+exc_name, logy=1, perc=1, ndigits=0)
    plot.time_series_single(time_listD, log_volumesD, "Log_volume"+exc_name,  perc=0)
    plot.time_series_single(time_listD, spreadD, "Spread_clean"+exc_name, perc=1, ndigits=1)
    plot.time_series_single(time_listD, returnsD, "Return_clean"+exc_name,  perc=1, ndigits=0)