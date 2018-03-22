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


#time_listM, priceM, volumeM = dis.quick_import(4)


#dis.korbit()
exc = 5
#imp = 5

#if exc != -1 and imp == 1:
#    dis.add_new_to_old_csv(exc)

exc_name, time_listM, pricesM, volumesM = di.get_list(exc)

r = 0
while time_listM[r] != '08.01.2014 10:00':
    r += 1

time_listM = time_listM[r:]
pricesM = pricesM[r:]
volumesM = volumesM[r:]

#print(exc_name, time_listM[0], time_listM[-1])
time_listH, pricesH, volumesH = dis.convert_to_hour(time_listM, pricesM, volumesM)

daytime, avg, lo, hi = dis.cyclical_average(time_listH, volumesH)
plot.intraday(avg,lo, hi,"KRAKENTEST")


#for i in range(200):
#    print(time_listH[i], '{0:.2f}'.format(pricesH[i]), '{0:.2}'.format(volumesH[i]))

#time_listH, returnsH, spreadH, volumesH, log_volumesH, illiqH, log_illiqH, rvolH, log_rvolH = dis.clean_series_hour(time_listM, pricesM, volumesM, exc=exc, convert_time_zones=1)
#time_listD, returnsD, spreadD, volumesD, log_volumesD, illiqD, log_illiqD, rvolD, log_rvolD = dis.clean_series_days(time_listM, pricesM, volumesM, exc=exc, convert_time_zones=1)

