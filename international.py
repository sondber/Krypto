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
print()

time_list_master = time_list_bitstampM
n = len(time_list_master)

