import numpy as np
import data_import as di
import plot
from Jacob import jacob_support as jake_supp
from Sondre import sondre_support_formulas as supp
import descriptive_stats as desc
import data_import_support as dis
import os

os.chdir("/Users/sondre/Documents/GitHub/krypto")

exchanges = ["bitstampusd", "btceusd", "coinbaseusd", "krakenusd"]
di.fetch_long_and_write(exchanges)

"""
exchanges, time_list, prices, volumes, total_price, total_volume = di.get_lists()
time_list, prices, volumes = dis.convert_to_hour(time_list, prices, volumes)


bitstamp_price = prices[0, :]
bitstamp_volume = volumes[0, :]
bitstamp_returns = jake_supp.logreturn(bitstamp_price)
btce_price = prices[1, :]
btce_volume = volumes[1, :]
btce_returns = jake_supp.logreturn(btce_price)

print("Bistamp: ")
print("Length:", len(time_list))
print(time_list[0])
print(time_list[len(time_list) - 1])

time_list_rolls, rolls = supp.get_rolls()
print("Rolls: ")
print("Length:", len(rolls))
print(time_list_rolls[0])
print(time_list_rolls[len(rolls) - 1])


day_list, average_return = dis.average_over_day(time_list, bitstamp_returns, frequency="h")
day_list, average_rolls = dis.average_over_day(time_list, rolls, frequency="h")

plot.two_axis(average_return, average_rolls, scale1="custom", scale2="custom", title1="Returns", title2="Rolls", type1="plot", type2="plot", color1="red", color2="blue")
"""