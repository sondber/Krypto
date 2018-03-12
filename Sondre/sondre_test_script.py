import numpy as np
import data_import as di
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

exc = 1

exchanges, time_list_minutes, prices_minutes, volumes_minutes = di.get_lists(opening_hours="n", make_totals="n")
#time_listH, returnsH, spreadH, log_volumesH, illiq_hours, illiq_timeH, log_illiq_hours, rvol_hours, log_rvol_hours = dis.clean_trans_hours(time_listM, pricesM, volumesM, exc=exc, convert_time_zones=0)


time_list_days, time_list_removed, returns_days, volumes_days, log_volumes_days, spread_days, \
illiq_days, log_illiq_days, rvol_days, log_rvol_days = dis.clean_trans_days(
    time_list_minutes, prices_minutes, volumes_minutes, exc=exc, print_days_excluded=0,
    convert_time_zones=1)

