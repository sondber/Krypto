import numpy as np
import linreg
import data_import
import data_import as di
import data_import_support
import plot
import regression_support
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
import regression_support as rs
import global_volume_index as gvi

os.chdir("/Users/sondre/Documents/GitHub/krypto")
#os.chdir("/Users/Jacob/Documents/GitHub/krypto")


local_time = 0
"""
for exc in range(6):
    exc_name, time_listM, pricesM, volumesM = di.get_list(exc)
    time_listH, returnsH, spreadH, volumesH, log_volumesH, illiqH, log_illiqH, rvolH, log_rvolH = dis.clean_series_hour(time_listM, pricesM, volumesM, exc=exc, convert_time_zones=local_time, plot_for_extreme=0)
    dis.write_clean_csv(exc_name, time_listH, returnsH, spreadH, volumesH, log_volumesH, illiqH, log_illiqH, rvolH, log_rvolH, freq="h", local_time=local_time)
    #time_listD, returnsD, spreadD, volumesD, log_volumesD, illiqD, log_illiqD, rvolD, log_rvolD = dis.clean_series_days(time_listM, pricesM, volumesM, exc=exc, convert_time_zones=1, plot_for_extreme=0)
    #dis.write_clean_csv(exc_name, time_listD, returnsD, spreadD, volumesD, log_volumesD, illiqD, log_illiqD, rvolD, log_rvolD, freq="d")
"""

time_list_indexD, volume_indexD = gvi.get_global_daily_volume_index()
time_list_indexH, volume_indexH = gvi.get_global_hourly_volume_index()
time_listD, volumes_actualD = di.get_global_volume_actual_daily()


start_i = time_listD.index(time_list_indexD[0])
time_listD = time_listD[start_i:]
volumes_actualD = volumes_actualD[start_i:]


corr = np.corrcoef(volumes_actualD, volume_indexD)
print("Our index accounts for %0.1f%% of the volume and has a correlation of %0.1f%% with the actual volumes" % (100*sum(volume_indexD)/sum(volumes_actualD), 100*corr[0,1]))

plot.time_series_single(time_list_indexD,volume_indexD,"global_volumes_index")
plot.time_series_single(time_listD,volumes_actualD,"actual_global_volumes")
"""

exc_name, time_listM, priceM, volumeM = di.get_list(exc="korbit", freq="m")
time_list_nativeH, priceH, volume_nativeH = dis.convert_to_hour(time_listM, priceM, volumeM)
spread_abs, spreadH, time_list_spread, count_value_error = rolls.rolls(priceM, time_listM, calc_basis="h", kill_output=1)

start_i = time_list_spread.index(time_list_indexH[0])
end_i = time_list_spread.index(time_list_indexH[-1]) + 1
time_list_spread = time_list_spread[start_i:end_i]
spreadH = spreadH[start_i:end_i]
volume_nativeH = volume_nativeH[start_i:end_i]

print("It is %s that the time lists are equal" % (time_list_spread == time_list_indexH))
time_listH = time_list_spread

time_list_removed = []
time_listH, time_list_removed, spreadH, volume_indexH, volume_nativeH = supp.remove_list1_zeros_from_all_lists(time_listH, time_list_removed, spreadH, volume_indexH, volume_nativeH)



X = np.transpose(np.matrix(volume_nativeH))
volume_indexH = np.transpose(np.matrix(volume_indexH))
X = np.append(X, volume_indexH, axis=1)

linreg.reg_multiple(spreadH, X, prints=1)

plot.time_series_single(time_list_combined,volumes_combined,"global_volumes_index")
plot.time_series_single(time_listD,volumesD,"actual_global_volumes")
"""
<<<<<<< HEAD
=======

>>>>>>> jacob
"""

check = 1
lag = 3

exc, time_listM, pricesM, volumesM = di.get_list(-1)
time_listH, pricesH, volumesH = dis.convert_to_hour(time_listM, pricesM, volumesM)

for i in range(len(time_listH)):
    print(time_listH[i], pricesH[i])

ar_test, indeces_to_remove = rs.AR_matrix(pricesH, time_listH, order=lag)
print("Resulting AR:")
print(ar_test)
print("Indeces to remove:")
print(indeces_to_remove)
<<<<<<< HEAD
=======
"""

>>>>>>> jacob

"""

exc, time_listM, pricesM, volumesM = di.get_list(-1)
time_listH, pricesH, volumesH = dis.convert_to_hour(time_listM, pricesM, volumesM)

lagged_list, index_list, hours_to_remove_1 = regression_support.get_lagged_list(pricesH, time_listH, lag=24)

last_day_average, hours_to_remove = rs.get_last_day_average(pricesH,time_listH, index_list)

print(hours_to_remove)
#
# exc_name, time_listM, priceM, volumeM = di.get_list(exc="korbit", freq="m")
# time_list_nativeH, priceH, volume_nativeH = dis.convert_to_hour(time_listM, priceM, volumeM)
# spread_abs, spreadH, time_list_spread, count_value_error = rolls.rolls(priceM, time_listM, calc_basis="h", kill_output=1)
#
# start_i = time_list_spread.index(time_list_indexH[0])
# end_i = time_list_spread.index(time_list_indexH[-1]) + 1
# time_list_spread = time_list_spread[start_i:end_i]
# spreadH = spreadH[start_i:end_i]
# volume_nativeH = volume_nativeH[start_i:end_i]
#
# print("It is %s that the time lists are equal" % (time_list_spread == time_list_indexH))
# time_listH = time_list_spread
#
# time_list_removed = []
# time_listH, time_list_removed, spreadH, volume_indexH, volume_nativeH = supp.remove_list1_zeros_from_all_lists(time_listH, time_list_removed, spreadH, volume_indexH, volume_nativeH)
#
#
#
# X = np.transpose(np.matrix(volume_nativeH))
# volume_indexH = np.transpose(np.matrix(volume_indexH))
# X = np.append(X, volume_indexH, axis=1)
# linreg.reg_multiple(spreadH, X, prints=1)
<<<<<<< HEAD
=======
"""

for t in range(6):
    exc, time_listM, pricesM, volumesM = di.get_list(t)

    spread, spread_rel, time_list, count_value_error, bias_list = rolls.rolls(pricesM, time_listM, kill_output=0, bias_indicator=1)

    cntr = 0

    for i in range(len(spread_rel)):
        if spread_rel[i] == 0:
            cntr += 1

    print("Counted", cntr, "zeros. Compare with errors:", count_value_error)

    bias_cntr = 0

    for j in range(0, len(bias_list)):
        if bias_list[j] == 1:
            bias_cntr += 1


    print("Counted", bias_cntr, "errors in bias_list")


    day_time, data_average, lower, upper = dis.cyclical_average(time_list, bias_list, incl_zeros=1)
    lower = data_average
    upper = data_average
    name = exc + "_indicator_"+ str(count_value_error)
    plot.intraday(data_average, lower, upper, name)



>>>>>>> jacob
