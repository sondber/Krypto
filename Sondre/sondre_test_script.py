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


for exc in [0, 1, 2, 3, 4, 5]:
    exc_name, time_listM, pricesM, volumesM = di.get_list(exc)
    time_listH, returnsH, spreadH, volumesH, log_volumesH, illiqH, log_illiqH, rvolH, log_rvolH = dis.clean_series_hour(time_listM, pricesM, volumesM, exc=exc, convert_time_zones=0, plot_for_extreme=0)
    dis.write_hourly_csv(exc_name, time_listH, returnsH, spreadH, volumesH, log_volumesH, illiqH, log_illiqH, rvolH, log_rvolH)