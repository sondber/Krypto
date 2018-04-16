import csv
import numpy as np
import linreg
import data_import
import data_import as di
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
import time
import datetime

os.chdir("/Users/Sondre/Documents/GitHub/krypto")

#local_time = 0


import_new_exchanges = False
global_volumes = True
spread_vs_global_volume_regression_daily = False
spread_vs_global_volume_regression_hourly= False
make_real_spread_csv = False
real_spread_vs_our_spread = False

if import_new_exchanges:
    for exc in range(6):
        exc_name, time_listM, pricesM, volumesM = di.get_list(exc)
        time_listH, returnsH, spreadH, volumesH, log_volumesH, illiqH, log_illiqH, rvolH, log_rvolH = dis.clean_series_hour(time_listM, pricesM, volumesM, exc=exc, convert_time_zones=local_time, plot_for_extreme=0)
        dis.write_clean_csv(exc_name, time_listH, returnsH, spreadH, volumesH, log_volumesH, illiqH, log_illiqH, rvolH, log_rvolH, freq="h", local_time=local_time)
        time_listD, returnsD, spreadD, volumesD, log_volumesD, illiqD, log_illiqD, rvolD, log_rvolD = dis.clean_series_days(time_listM, pricesM, volumesM, exc=exc, convert_time_zones=1, plot_for_extreme=0)
        dis.write_clean_csv(exc_name, time_listD, returnsD, spreadD, volumesD, log_volumesD, illiqD, log_illiqD, rvolD, log_rvolD, freq="d")

if global_volumes:

    #gvi.write_hourly_volume_index_to_csv()
    # gvi.write_daily_volume_index_to_csv()

    time_list_indexD, volume_indexD = gvi.get_global_daily_volume_index()
    time_list_indexH, volume_indexH = gvi.get_global_hourly_volume_index()
    time_listD, volumes_actualD = di.get_global_volume_actual_daily()

    plt.plot(volume_indexD)
    plt.figure()

    time_out = []
    vol_index = []
    vol_actual = []
    for i in range(len(volumes_actualD)):
        t = time_listD[i]
        try:
            j = time_list_indexD.index(t)
            time_out.append(t)
            vol_index.append(volume_indexD[i])
            vol_actual.append(volumes_actualD[i])
        except:
            pass

    volumes_actualD = vol_actual
    volume_indexD = vol_index


    plt.plot(volumes_actualD)
    plt.figure()
    plt.plot(volume_indexD)
    plt.show()


    corr = np.corrcoef(volumes_actualD, volume_indexD)
    print("Our index accounts for %0.1f%% of the volume and has a correlation of %0.1f%% with the actual volumes" % (100*sum(volume_indexD)/sum(volumes_actualD), 100*corr[0,1]))

    plot.time_series_single(time_list_indexD,volume_indexD,"global_volumes_index")
    plot.time_series_single(time_listD,volumes_actualD,"actual_global_volumes")

    corr = np.corrcoef(volumes_actualD, volume_indexD)
    print("Our index accounts for %0.1f%% of the volume and has a correlation of %0.1f%% with the actual volumes" % (
    100 * sum(volume_indexD) / sum(volumes_actualD), 100 * corr[0, 1]))

    plot.time_series_single(time_list_indexD, volume_indexD, "global_volumes_index")
    plot.time_series_single(time_listD, volumes_actualD, "actual_global_volumes")

if spread_vs_global_volume_regression_daily:
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

if spread_vs_global_volume_regression_hourly:
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

if make_real_spread_csv:

    for exc_name in ["bitstamp", "korbit"]:
        file_name= "data/long_raw_data/" + exc_name + "_new_minutes.csv"
        time_listM, pricesM, volumesM = dis.price_volume_from_raw(file_name, [], [], [], semi=1, unix=0, price_col=4)
        y, mo, d, h, mi = supp.fix_time_list(time_listM)

        unixM = []
        unixM = supp.timestamp_to_unix(time_listM)

        for i in range(1, len(time_listM)):
            if unixM[i] - unixM[i-1] != 60:
                print(i, time_listM[i])

        pricesM = supp.fill_blanks(pricesM)
        print("finihed importing")
        print(len(time_listM), time_listM[-10:])
        print(len(pricesM),(pricesM[-10:]))
        print(len(volumesM), (volumesM[-10:]))
        spread_abs, spreadH, time_listH, count_value_error = rolls.rolls(pricesM, time_listM, calc_basis="h", kill_output=1)


        write_filename = "data/export_csv/" + exc_name + "_spread_new.csv"
        with open(write_filename, 'w', newline='') as csvfile:
            writ = csv.writer(csvfile, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            print("\033[0;32;0m Writing to file '%s'...\033[0;0;0m" % write_filename)

            header3 = ["Time"]
            header3.append("Spread")
            writ.writerow(header3)

            for i in range(len(time_listH)):
                rowdata = [time_listH[i]]
                rowdata.append(spreadH[i])
                writ.writerow(rowdata)

if real_spread_vs_our_spread:
    for exc in ["bitstamp", "korbit"]:
        exc_name, time_listM, pricesM, volumesM = di.get_list(exc, freq="m", local_time="0")
        spread_abs, spreadH, time_listH, count_value_error = rolls.rolls(pricesM, time_listM, calc_basis="h", kill_output=1)

        time_list_realH, real_spreadH = di.get_real_spread(exc)
        real_spreadH = np.divide(real_spreadH, 100)

        spreadH = []
        time_listH = []

        file_name = "data/export_csv/" + exc + "_spread_new.csv"
        with open(file_name, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=';', quotechar='|')
            print("\033[0;32;0m Reading file '%s'...\033[0;0;0m" % file_name)
            i = 0
            next(reader)
            for row in reader:
                try:
                    time_listH.append(str(row[0]))
                    spreadH.append(float(row[1]))
                except ValueError:
                    print("\033[0;31;0m There was an error on row %i in '%s'\033[0;0;0m" % (i + 1, file_name))
                i = i + 1

        time_listH, rem, spreadH, real_spreadH = supp.remove_list1_zeros_from_all_lists(time_listH, [], spreadH, real_spreadH)

        std_real = (real_spreadH - np.mean(real_spreadH))/np.std(real_spreadH)
        std_calc = (spreadH - np.mean(spreadH))/np.std(spreadH)

        print("The correlation between real and estimated BAS for %s is %0.3f" % (exc_name, np.corrcoef(real_spreadH,spreadH)[0,1]))
        plot.time_series_single(time_listH, real_spreadH, "real_spread_"+exc_name, perc=1)
        plot.time_series_single(time_listH, spreadH, "calculated_spread_"+exc_name, perc=1)
        plot.scatters(real_spreadH, spreadH, xtitle="Real BAS", ytitle="Estimated BAS", x_perc=1, y_perc=1, title="BAS_estimated_vs_real_"+exc_name)

        hour_of_day, avg_spread_hour, low_spread_hour, upper_spread_hour = dis.cyclical_average(time_listH, spreadH,
                                                                                                frequency="h")
        title = "estimated_spread_" + exc_name
        plot.intraday(avg_spread_hour, low_spread_hour, upper_spread_hour, title=title, perc=1, fig_format="wide")



