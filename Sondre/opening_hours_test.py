import numpy as np
import data_import as di
import legacy
from Jacob import jacob_support as jake_supp
import data_import_support as dis
from matplotlib import pyplot as plt
import os
os.chdir("/Users/sondre/Documents/GitHub/krypto")  # Blir ikke likt på deres pc

exchanges = ["bitstampusd", "btceusd", "coinbaseusd", "krakenusd"]

# Importing data for all minutes of the day
exchanges, time_list, prices, volumes = legacy.get_lists_legacy(opening_hours="n", make_totals="n")
# Converting to hourly data
time_list, prices, volumes = dis.convert_to_hour(time_list, prices, volumes)
full_returns = jake_supp.logreturn(prices[0, :])

# Only extracting opening hours
time_list_open, prices_open, volumes_opeen = legacy.opening_hours_w_weekends(time_list, prices, volumes)
bitstamp_price_open = np.transpose(prices_open[0, :])
open_returns = jake_supp.logreturn(bitstamp_price_open)

# Finding average for entire day
full_day_time, full_day_avg_returns = dis.cyclical_average_legacy(time_list, full_returns)
# Finding average for opening hours
open_time, open_avg_returns = dis.cyclical_average_legacy(time_list_open, open_returns)

# Want to compare the two in a single graph
x = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]
opening_y = np.zeros(24)
for i in range(0, 7):
    opening_y[i + 13] = open_avg_returns[i]

plt.plot(x[10:23], full_day_avg_returns[10:23])
plt.plot(x[10:23], opening_y[10:23])
plt.show()
