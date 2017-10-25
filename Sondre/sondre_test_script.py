import numpy as np
import data_import as di
import plot
from Jacob import jacob_support as jake_supp
from Sondre import sondre_support_formulas as supp
import descriptive_stats as desc
import os

os.chdir("/Users/sondre/Documents/GitHub/krypto")

exchanges, time_list, prices, volumes, total_price, total_volume = di.get_lists()


bitstamp_price = prices[0, :]
bitstamp_volume = volumes[0, :]
bitstamp_returns = jake_supp.logreturn(bitstamp_price)
btce_price = prices[1, :]
btce_volume = volumes[1, :]
btce_returns = jake_supp.logreturn(btce_price)

desc.combined_stats(bitstamp_returns, btce_returns, "Bitstamp", "BTCE")