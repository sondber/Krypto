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
import regression_support as rs

os.chdir("/Users/sondre/Documents/GitHub/krypto")
#os.chdir("/Users/Jacob/Documents/GitHub/krypto")


local_time = 0
for exc in range(6):
    exc_name, time_listM, pricesM, volumesM = di.get_list(exc)
    time_listH, returnsH, spreadH, volumesH, log_volumesH, illiqH, log_illiqH, rvolH, log_rvolH = dis.clean_series_hour(time_listM, pricesM, volumesM, exc=exc, convert_time_zones=local_time, plot_for_extreme=0)
    dis.write_clean_csv(exc_name, time_listH, returnsH, spreadH, volumesH, log_volumesH, illiqH, log_illiqH, rvolH, log_rvolH, freq="h", local_time=local_time)
    #time_listD, returnsD, spreadD, volumesD, log_volumesD, illiqD, log_illiqD, rvolD, log_rvolD = dis.clean_series_days(time_listM, pricesM, volumesM, exc=exc, convert_time_zones=1, plot_for_extreme=0)
    #dis.write_clean_csv(exc_name, time_listD, returnsD, spreadD, volumesD, log_volumesD, illiqD, log_illiqD, rvolD, log_rvolD, freq="d")




"""
check = 1
lag = 3

exc, time_listM, pricesM, volumesM = di.get_list(-1)
time_listH, pricesH, volumesH = dis.convert_to_hour(time_listM, pricesM, volumesM)

index_test, x_test = rs.AR_matrix(pricesH, time_listH, order=lag)
print(index_test)

if check == 1:
    if lag == 1:
        for i in range(0,lag):
            print(time_listH[i], pricesH[i], index_test[i])
        for j in range(0, len(x_test)):
            print(time_listH[j+lag], pricesH[j+lag], index_test[j+lag], x_test[j])
    else:
        col = 0  #HER SJEKKER DU DE ULIKE AR(COL) (husk at 0 er 1)
        for i in range(0, lag):
            print(time_listH[i], pricesH[i], index_test[i,col])
        for j in range(0, len(x_test)):
            print(time_listH[j + lag], pricesH[j + lag], index_test[j + lag, col], x_test[j, col])
"""