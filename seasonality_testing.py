import numpy as np
import data_import as di
import matplotlib.pyplot as plt
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

for i in range(0, 4):
    exchange, time_listM, pricesM, volumesM = di.get_list(i)
    print("Calculating for", exchange)
    # adjust = len(time_listM) - math.floor((len(time_listM) / 60)) * 60
    adjust = 0
    # accounting for faulty data
    time_listM = time_listM[0:len(time_listM) - adjust]
    pricesM = pricesM[0:len(pricesM) - adjust]
    volumesM = volumesM[0:len(volumesM) - adjust]

    time_listH, pricesH, volumesH = dis.convert_to_hour(time_listM, pricesM, volumesM)

    bas = rolls.rolls(pricesM, time_listM, kill_output=1)[1]

    volumesH_clean = []
    bas_clean = []
    time_listH_clean = []

    for j in range(len(time_listH)):
        if volumesH[j] != 0 and bas[j] != 0:
            time_listH_clean.append(time_listH[j])
            volumesH_clean.append(volumesH[j])
            bas_clean.append(bas[j])

    day_time, V_average, V_lower, V_upper = dis.cyclical_average(time_listH_clean, volumesH_clean)
    day_time, bas_average, bas_lower, bas_upper = dis.cyclical_average(time_listH_clean, bas_clean)
    plot.intraday(V_average, V_lower, V_upper, title=exchange+"_"+"V")
    plot.intraday(bas_average, bas_lower, bas_upper, title=exchange+"_"+"bas")
