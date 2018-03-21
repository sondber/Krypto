import numpy as np
import time
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



# Hente inn alle 5


exc_name, time_list_bitstampM, prices_bitstampM, volumes_bitstampM = di.get_list(0)
#exc_name, time_list_coincheckM, prices_coincheckM, volumes_coincheckM = di.get_list(1)
#exc_name, time_list_btcnM, prices_btcnM, volumes_btcnM = di.get_list(2)
#exc_name, time_list_coinbaseM, prices_coinbaseM, volumes_coinbaseM = di.get_list(3)
exc_name, time_list_korbitM, prices_korbitM, volumes_korbitM = di.get_list(4)

s_abs, spread_bitstampH, spread_time_bitstamp, errs = rolls.rolls(prices_bitstampM, time_list_bitstampM, kill_output=1)
s_abs, spread_korbitH, spread_time_korbit, errs  = rolls.rolls(prices_korbitM, time_list_korbitM, kill_output=1)

print()
print("Lengths:")
print()
print("Bitstamp time minutes:", len(time_list_bitstampM))
print(time_list_bitstampM[0],time_list_bitstampM[-1])
print("Bitstamp time hours:", len(spread_bitstampH))
print(spread_time_bitstamp[0],spread_time_bitstamp[-1])
print("Korbit time minutes:", len(time_list_korbitM))
print(time_list_korbitM[0], time_list_korbitM[-1])
print("Korbit time hours:", len(spread_korbitH))
print(spread_time_korbit[0],spread_time_korbit[-1])

time_list_master = []
spread_master = []
n1 = len(spread_time_bitstamp)
n2 = len(spread_time_korbit)

prev_j = 0
print()
print("searching......")
for i in range(0, n1):
    time_stamp = spread_time_bitstamp[i]
    j = max(0, prev_j)
    if not supp.A_before_B(time_stamp, spread_time_korbit[0]):
        while spread_time_korbit[j] != time_stamp and j < n2:
            j += 1
        spread_row = [spread_bitstampH[i], spread_korbitH[j]]
        spread_row = np.matrix(spread_row)
        if len(spread_master) == 0:
            spread_master = spread_row
        else:
            spread_master = np.append(spread_master,spread_row, axis=1)
        time_list_master.append(time_stamp)
        prev_j = j

print("finished searching.")
print(spread_master)
print(np.size(spread_master,0), np.size(spread_master,1))
for i in range(len(time_list_master)):
    print(time_list_master[i])