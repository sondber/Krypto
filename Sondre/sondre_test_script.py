import numpy as np
import data_import as di
import plot
from Jacob import jacob_support as jake_supp
from Sondre import sondre_support_formulas as supp
import descriptive_stats as desc
import data_import_support as dis
import os
from matplotlib import pyplot as plt
import rolls

os.chdir("/Users/sondre/Documents/GitHub/krypto")

exchanges = ["bitstampusd", "btceusd", "coinbaseusd", "krakenusd"]

check_freq = 0
if check_freq == 1:  # Verification of frequency consistency
    exchanges, minute_time, min_prices, min_volumes = di.get_lists(opening_hours="n", make_totals="n")
    hour_time, hour_prices, hour_volumes = dis.convert_to_hour(minute_time, min_prices, min_volumes)
    day_time, day_prices, day_volumes = dis.convert_to_day(minute_time, min_prices, min_volumes)

    k_time_m, avg_vol_m = dis.average_over_day(minute_time, min_volumes[0, :], frequency="m")
    k_time_h, avg_vol_h = dis.average_over_day(hour_time, hour_volumes[0, :], frequency="h")
    k_time_d, avg_vol_d = dis.average_over_day(day_time, day_volumes[0, :], frequency="d")

    print("Minute: ")
    print(" ", minute_time[0], minute_time[len(minute_time) - 1])
    print(" Sum of volumes: ", sum(min_volumes[0, :]))
    print(" Average volume: ", np.average(min_volumes[0, :]))
    print(" Alternative average: ", np.average(avg_vol_m))
    print()
    print("Hour: ")
    print(" ", hour_time[0], hour_time[len(hour_time)-1])
    print(" Sum of volumes: ", sum(hour_volumes[0, :]))
    print(" Average volume: ", np.average(hour_volumes[0, :]))
    print(" Alternative average: ", np.average(avg_vol_h))
    print()
    print("Day: ")
    print(" ", day_time[0], day_time[len(day_time)-1])
    print(" Sum of volumes: ", sum(day_volumes[0, :]))
    print(" Average volume: ", np.average(day_volumes[0, :]))
    print(" Alternative average: ", np.average(avg_vol_d))
    print()
