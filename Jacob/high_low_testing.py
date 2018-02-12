import high_low_spread as hilo
import data_import as di
import matplotlib.pyplot as plt
import os

os.chdir("/Users/Jacob/Documents/GitHub/krypto")

exchanges, time_list, hi, lo = di.get_hilo(opening_hours="y")

timestamps = time_list

#timelist, spreads = hilo.hi_lo_spread(timestamps, highs, lows)

#plt.plot(spreads)
#plt.show()