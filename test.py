import numpy as np
import data_import as di
import matplotlib.pyplot as plt
import plot
from Jacob import jacob_support as jake_supp
from Sondre import sondre_support_formulas as supp
import data_import_support as dis
import os
import rolls
import scipy.stats as st
import ILLIQ
import realized_volatility
import math

exc = 2
conv = 1

exch, time_listM, pricesM, volumesM = di.get_list(exc)

#time_stamps_out, prices_out, volumes_out = dis.convert_to_hour(time_listM, pricesM, volumesM)
time_stampsD, pricesD, volumesD = dis.convert_to_day(time_listM, pricesM, volumesM)

#time_listD, returnsD, volumesD, log_volumesD, spreadD, illiqD, log_illiqD, rvolD, log_rvolD = dis.clean_series_days(
#    time_listM, pricesM, volumesM, exc=exc, print_days_excluded=0, convert_time_zones=conv)
