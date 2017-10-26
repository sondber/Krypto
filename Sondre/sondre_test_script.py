import numpy as np
import data_import as di
import plot
from Jacob import jacob_support as jake_supp
from Sondre import sondre_support_formulas as supp
import descriptive_stats as desc
import data_import_support as dis
import two_axis_plot as tap
import os

os.chdir("/Users/sondre/Documents/GitHub/krypto")

exchanges, time_list, prices, volumes, total_price, total_volume = di.get_lists()

time_list, prices, volumes = dis.convert_to_hour(time_list, prices, volumes)

start = 0
end = 100
interval = 1
for i in range(start, end, interval):
    print(i, time_list[i], volumes[0, i])


"""
bitstamp_price = prices[0, :]
bitstamp_volume = volumes[0, :]
bitstamp_returns = jake_supp.logreturn(bitstamp_price)
btce_price = prices[1, :]
btce_volume = volumes[1, :]
btce_returns = jake_supp.logreturn(btce_price)
"""

#time_list_rolls, rolls = supp.get_rolls()

#print(len(rolls))

#tap.two_axis(volumes[0, 0:41495], rolls, scale1="custom", scale2="custom", title1="Bitstamp Prices", title2="BTCE Prices", type1="plot", type2="plot")