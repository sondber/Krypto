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

# for exc in [0, 1, 2, 3, 4, 5]:
#      exc_name, time_listM, pricesM, volumesM = di.get_list(exc)
#      time_listH, returnsH, spreadH, volumesH, log_volumesH, illiqH, log_illiqH, rvolH, log_rvolH = dis.clean_series_hour(time_listM, pricesM, volumesM, exc=exc, convert_time_zones=0, plot_for_extreme=0)
#      dis.write_clean_csv(exc_name, time_listH, returnsH, spreadH, volumesH, log_volumesH, illiqH, log_illiqH, rvolH, log_rvolH, freq="h")
#      time_listD, returnsD, volumesD, log_volumesD, spreadD, illiqD, log_illiqD, rvolD, log_rvolD = dis.clean_series_days(time_listM, pricesM, volumesM, exc=exc, convert_time_zones=1, plot_for_extreme=0)
#      dis.write_clean_csv(exc_name, time_listD, returnsD, spreadD, volumesD, log_volumesD, illiqD, log_illiqD, rvolD, log_rvolD, freq="d")
#

#
exc_name, time_listD0, returnsD, volumesD0, log_volumesD, spreadD, illiqD, log_illiqD, rvolD, log_rvolD  = di.get_list(exc=0,freq="d")
exc_name, time_listD2, returnsD, volumesD2, log_volumesD, spreadD, illiqD, log_illiqD, rvolD, log_rvolD  = di.get_list(exc=2,freq="d")
exc_name, time_listD3, returnsD, volumesD3, log_volumesD, spreadD, illiqD, log_illiqD, rvolD, log_rvolD  = di.get_list(exc=3,freq="d")
exc_name, time_listD4, returnsD, volumesD4, log_volumesD, spreadD, illiqD, log_illiqD, rvolD, log_rvolD  = di.get_list(exc=4,freq="d")
exc_name, time_listD5, returnsD, volumesD5, log_volumesD, spreadD, illiqD, log_illiqD, rvolD, log_rvolD  = di.get_list(exc=5,freq="d")





date_comb, volume_comb = supp.add_two_series_w_different_time_lists(time_listD0, volumesD0, time_listD2, volumesD2)
date_comb, volume_comb = supp.add_two_series_w_different_time_lists(date_comb, volume_comb, time_listD3, volumesD3)
date_comb, volume_comb = supp.add_two_series_w_different_time_lists(date_comb, volume_comb, time_listD4, volumesD4)
date_comb, volume_comb = supp.add_two_series_w_different_time_lists(date_comb, volume_comb, time_listD5, volumesD5)

time_list_global, volumes_global = di.get_global_volume()

plt.plot(volume_comb)
plt.figure()
plt.plot(volumes_global)
plt.show()


print(time_listD0[0:10])
test_time_1 = ['02.01.2013 00:00', '03.01.2013 00:00', '08.01.2013 00:00', '09.01.2013 00:00', '11.01.2013 00:00', '12.01.2013 00:00', '16.01.2013 00:00', '19.01.2013 00:00', '21.01.2013 00:00', '22.01.2013 00:00']
test_time_2 = ['08.01.2013 00:00', '09.01.2013 00:00', '11.01.2013 00:00', '16.01.2013 00:00', '19.01.2013 00:00', '21.01.2013 00:00', '22.01.2013 00:00']
