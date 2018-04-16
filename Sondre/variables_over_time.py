import data_import as di
import data_import_support as dis
import legacy
import plot
import numpy as np
import os
import realized_volatility
import rolls
import ILLIQ
from Jacob import jacob_support as jake_supp

os.chdir("/Users/sondre/Documents/GitHub/krypto")


unedited = 0
transformed = 1

# Transformation

exch = ["bitstamp", "coinbase", "btcn", "korbit"]


for exc in exch:
    exc_name, time_listD, returnsD, volumesD, log_volumesD, spreadD, illiqD, log_illiqD, rvolD, log_rvolD= di.get_list(exc,freq="d", local_time=0)
    exc_name, time_listM, pricesM, volumesM = di.get_list(exc, freq="m")
    timeD, pricesD, volumes_rawD = dis.convert_to_day(time_listM, pricesM, volumesM)
    #

    plot.time_series_single(timeD, pricesD, "price_" + exc_name)
    plot.time_series_single(time_listD, volumesD, "volume_"+exc_name)
    plot.time_series_single(time_listD, illiqD, "Log_ILLIQ_"+exc_name, logy=1, perc=1, ndigits=3)
    plot.time_series_single(time_listD, rvolD, "Log_volatility_"+exc_name, logy=1, perc=1, ndigits=0)
    plot.time_series_single(time_listD, log_volumesD, "Log_volume_"+exc_name,  perc=0)
    plot.time_series_single(time_listD, spreadD, "Spread_clean_"+exc_name, perc=1, ndigits=1)
    plot.time_series_single(time_listD, returnsD, "Return_clean_"+exc_name,  perc=1, ndigits=0)