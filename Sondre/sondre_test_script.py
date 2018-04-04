import numpy as np
import linreg
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
import regression_support as rs

#os.chdir("/Users/sondre/Documents/GitHub/krypto")
os.chdir("/Users/Jacob/Documents/GitHub/krypto")


local_time = 0
"""
for exc in range(6):
    exc_name, time_listM, pricesM, volumesM = di.get_list(exc)
    time_listH, returnsH, spreadH, volumesH, log_volumesH, illiqH, log_illiqH, rvolH, log_rvolH = dis.clean_series_hour(time_listM, pricesM, volumesM, exc=exc, convert_time_zones=local_time, plot_for_extreme=0)
    dis.write_clean_csv(exc_name, time_listH, returnsH, spreadH, volumesH, log_volumesH, illiqH, log_illiqH, rvolH, log_rvolH, freq="h", local_time=local_time)
    #time_listD, returnsD, spreadD, volumesD, log_volumesD, illiqD, log_illiqD, rvolD, log_rvolD = dis.clean_series_days(time_listM, pricesM, volumesM, exc=exc, convert_time_zones=1, plot_for_extreme=0)
    #dis.write_clean_csv(exc_name, time_listD, returnsD, spreadD, volumesD, log_volumesD, illiqD, log_illiqD, rvolD, log_rvolD, freq="d")
"""


"""
bitstamp, time_list_bitstampM, prices_bitstampM, volumes_bitstampM = di.get_list(exc="bitstampusd")
coinbase, time_list_coinbaseM, prices_coinbaseM, volumes_coinbaseM = di.get_list(exc="coinbaseusd")
#btcncny, time_list_btcncnyM, prices_btcncnyM, volumes_btcncnyM = di.get_list(exc="btcncny")
korbit, time_list_korbitM, prices_korbitM, volumes_korbitM = di.get_list(exc="korbitkrw")
krak, time_list_krakM, prices_krakM, volumes_krakM = di.get_list(exc="krakeneur")
cc, time_list_ccM, prices_ccM, volumes_ccM = di.get_list(exc="coincheckjpy")


bitstamp_day_list, prices, volumes_bitstampD = dis.convert_to_day(time_list_bitstampM, prices_bitstampM,volumes_bitstampM)
coinbase_day_list, prices, volumes_coinbaseD = dis.convert_to_day(time_list_coinbaseM, prices_coinbaseM,volumes_coinbaseM)
#btcncny_day_list, prices, volumes_btcncnyD = dis.convert_to_day(time_list_btcncnyM, prices_btcncnyM,volumes_btcncnyM)
korbit_day_list, prices, volumes_korbitD = dis.convert_to_day(time_list_korbitM, prices_korbitM,volumes_korbitM)
krak_day_list, prices, volumes_krakD = dis.convert_to_day(time_list_krakM, prices_krakM,volumes_krakM)
cc_day_list, prices, volumes_ccD = dis.convert_to_day(time_list_ccM, prices_ccM,volumes_ccM)


time_list_combined2, volumes_combined2 = dis.add_two_series_w_different_times(coinbase_day_list, volumes_coinbaseD,bitstamp_day_list, volumes_bitstampD)
#time_list_combined1, volumes_combined1 = dis.add_two_series_w_different_times(time_list_combined2, volumes_combined2,btcncny_day_list, volumes_btcncnyD)
time_list_combined0, volumes_combined0 = dis.add_two_series_w_different_times(time_list_combined2, volumes_combined2,korbit_day_list, volumes_korbitD)
time_list_combined00, volumes_combined00 = dis.add_two_series_w_different_times(time_list_combined0, volumes_combined0,krak_day_list, volumes_krakD)
time_list_combined, volumes_combined = dis.add_two_series_w_different_times(cc_day_list, volumes_ccD,time_list_combined00, volumes_combined00)



time_listD, volumesD = di.get_global_volume()


start_index = time_listD.index(time_list_combined[0])
time_listD = time_listD[start_index:]
volumesD = volumesD[start_index:]


corr = np.corrcoef(volumes_combined, volumesD)
print(corr)

linreg.reg_multiple(volumesD, volumes_combined,prints=1)



plot.time_series_single(time_list_combined,volumes_combined,"global_volumes_index")
plot.time_series_single(time_listD,volumesD,"actual_global_volumes")
"""
"""

check = 1
lag = 3

exc, time_listM, pricesM, volumesM = di.get_list(-1)
time_listH, pricesH, volumesH = dis.convert_to_hour(time_listM, pricesM, volumesM)

for i in range(len(time_listH)):
    print(time_listH[i], pricesH[i])

ar_test, indeces_to_remove = rs.AR_matrix(pricesH, time_listH, order=lag)
print("Resulting AR:")
print(ar_test)
print("Indeces to remove:")
print(indeces_to_remove)

"""