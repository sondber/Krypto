import numpy as np

import data_import
import data_import as di
import data_import_support
import plot
from Jacob import jacob_support as jake_supp
from Sondre import sondre_support_formulas as supp
import descriptive_stats as desc
import data_import_support as dis
import os
from matplotlib import pyplot as plt
import matplotlib.ticker as mtick
import realized_volatility
import rolls
import ILLIQ

os.chdir("/Users/sondre/Documents/GitHub/krypto")
#os.chdir("/Users/Jacob/Documents/GitHub/krypto")

dis.add_new_to_old_csv(0)

#di.get_list(1)



#exchanges = ["bitstampusd", "coincheckjpy", "btcncny"]
#di.fetch_long_and_write(exchanges)
#dis.fuse_files(exchanges)


#time, price, volume = data_import_support.quick_import(3)
#exchanges, time_listM, pricesM, volumesM = di.get_lists(opening_hours="n", make_totals="n")


#time_listH, returnsH, spreadH, log_volumesH, illiqH, log_illiqH, rvolH, log_rvolH = dis.clean_series_hour(time_listM, pricesM, volumesM, exc=exc, convert_time_zones=0)

