import numpy as np
import data_import as di
import matplotlib.pyplot as plt

import legacy
import plot
from Jacob import jacob_support as jake_supp
from Sondre import sondre_support_formulas as supp
import data_import_support as dis
import os
import rolls
import scipy.stats as st
import ILLIQ
import realized_volatility
import math

exchanges, time_listM, pricesM, volumesM = legacy.get_lists_legacy(opening_hours="n", make_totals="n")

time_listH, pricesH, volumesH = dis.convert_to_hour(time_listM, pricesM, volumesM)

# For alle tre exchanges: lag BAS_lister
bitstamp_pricesM = pricesM[0, :]
coincheck_pricesM = pricesM[1, :]
btcn_pricesM = pricesM[2, :]

bitstamp_pricesH = pricesH[0, :]
coincheck_pricesH = pricesH[1, :]
btcn_pricesH = pricesH[2, :]

bitstamp_volumesH = volumesH[0, :]
coincheck_volumesH = volumesH[1, :]
btcn_volumesH = volumesH[2, :]

bitstamp_bas = rolls.rolls(bitstamp_pricesM, time_listM, kill_output=1)[1]
coincheck_bas = rolls.rolls(coincheck_pricesM, time_listM, kill_output=1)[1]
btcn_bas = rolls.rolls(btcn_pricesM, time_listM, kill_output=1)[1]

print(len(time_listH), len(bitstamp_volumesH), len(coincheck_volumesH), len(btcn_volumesH))

bitstamp_volumeH_clean = []
coincheck_volumeH_clean = []
btcn_volumeH_clean = []

bitstamp_bas_clean = []
coincheck_bas_clean = []
btcn_bas_clean = []

time_listH_clean = []

for i in range(len(time_listH)):
    if bitstamp_volumesH[i] != 0 and coincheck_volumesH[i] != 0 and btcn_volumesH[i] != 0 and bitstamp_bas[i] != 0 and \
                    coincheck_bas[i] != 0 and btcn_bas[i] != 0:
        time_listH_clean.append(time_listH[i])

        bitstamp_volumeH_clean.append(bitstamp_volumesH[i])
        coincheck_volumeH_clean.append(coincheck_volumesH[i])
        btcn_volumeH_clean.append(btcn_volumesH[i])

        bitstamp_bas_clean.append(bitstamp_bas[i])
        coincheck_bas_clean.append(coincheck_bas[i])
        btcn_bas_clean.append(btcn_bas[i])

print(len(time_listH_clean), len(bitstamp_volumeH_clean), len(coincheck_volumeH_clean), len(btcn_volumeH_clean),
      len(bitstamp_bas_clean), len(coincheck_bas_clean), len(btcn_bas_clean))

day_time, bitstampV_average, bitstampV_lower, bitstampV_upper = dis.cyclical_average(time_listH_clean, bitstamp_volumeH_clean)
day_time, coincheckV_average, coincheckV_lower, coincheckV_upper = dis.cyclical_average(time_listH_clean, coincheck_volumeH_clean)
day_time, btcnV_average, btcnV_lower, btcnV_upper = dis.cyclical_average(time_listH_clean, btcn_volumeH_clean)
plot.intraday(bitstampV_average,bitstampV_lower,bitstampV_upper,title="bitstamp")
plot.intraday(coincheckV_average,coincheckV_lower,coincheckV_upper,title="coincheck")
plot.intraday(btcnV_average,btcnV_lower,btcnV_upper,title="btcn")


