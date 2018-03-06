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

#os.chdir("/Users/sondre/Documents/GitHub/krypto")
os.chdir("/Users/sondre/Documents/GitHub/krypto")

exc = 0

exchanges, time_list_minutes, prices_minutes, volumes_minutes = di.get_lists(opening_hours="n", make_totals="n")
time_list_hours_clean, returns_hours_clean, spread_hours_clean, log_volumes_hours_clean, illiq_hours_clean, \
    illiq_hours_time, log_illiq_hours_clean, rvol_hours_clean, log_rvol_hours_clean = \
    dis.clean_trans_hours(time_list_minutes, prices_minutes, volumes_minutes, exc=exc, convert_time_zones=0)
