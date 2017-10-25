import numpy as np
import data_import as di
import plot
from Jacob import jacob_support as jake_supp
from Sondre import sondre_support_formulas as supp
import descriptive_stats as desc
import os

os.chdir("/Users/sondre/Documents/GitHub/krypto")


#exchanges = ["bitstampusd", "btceusd", "coinbaseusd", "krakenusd"]
#di.fetch_long_and_write(exchanges)

#exchanges, time_list, prices, volumes, total_price, total_volume = di.get_lists()
#plot.user_plots(exchanges, time_list, prices, volumes, total_price, total_volume)

di.import_gold_lists()

# print(volume)
# print(gold_price)
"""
total_price = di.get_lists("h", data="price")
total_volume = di.get_lists("h", data="volume")
returns = jake_supp.logreturn(total_price)
desc.combined_stats(total_volume, returns, "Volume", "Returns")
"""