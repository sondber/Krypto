import numpy as np
import data_import as di
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


exchanges, time_listM, pricesM, volumesM = di.get_lists(opening_hours="n", make_totals="n")

time_listH, pricesH, volumesH = dis.convert_to_hour(time_listM, pricesM, volumesM)

# For alle tre exchanges: lag BAS_lister
bitstamp_pricesM = pricesM[0, :]
bitstamp_pricesM = pricesM[0, :]
bitstamp_pricesM = pricesM[0, :]

#
bitstamp_bas = rolls.rolls(.....)
bitstamp_bas = rolls.rolls(.....)
bitstamp_bas = rolls.rolls(.....)

#
for i in range(len(time_listH)):
    1
    # hvis enten bitstamp, btc eller coincheck har null volum eller null bas: slett append ikke
    # time_listH_clean.append()

#plt.plot()
#plt.plot()
#plt.plot()
#plt.show()