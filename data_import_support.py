import csv
from datetime import date
from inspect import currentframe as cf, getframeinfo as gf

import numpy as np
import scipy.stats as st
from matplotlib import pyplot as plt

import ILLIQ
import realized_volatility
import rolls
from Jacob import jacob_support as jake_supp
from Sondre import sondre_support_formulas as supp
from Sondre.sondre_support_formulas import unix_to_timestamp


def add_new_to_old_csv(exc=0):

    location = "data/bitcoincharts/"
    year = '2017'

    start_date = "01.01.2012 00:00"
    start_unix = 1325376000
    end_unix = 0
    end_date = "31.12.2017 23:59"

    if exc == 1:
        exc_name = "coincheckjpy"
        month_list = ["06", "07", "08", "09", "10", "11", "12"]
        start_date = "01.11.2014 00:00"
        start_unix = 1414800000
    elif exc == 2:
        exc_name = "btcncny"
        month_list = ["06", "07", "08", "09"]
        end_date = "29.09.2017 23:59"
        #end_unix = 1506815880
    elif exc == 3:
        exc_name = "coinbaseusd"
        month_list = []
        start_date = "02.12.2014 00:00"
        start_unix = 1417478400
        end_unix = 1514764740
    else:
        exc_name = "bitstampusd"
        month_list = ["06", "07", "08", "09", "10", "11", "12"]


    time_old, price_old, volume_old = quick_import(exc)
    start_index = time_old.index(start_unix)
    if end_unix == 0:
        time_old = time_old[start_index:]
        price_old = price_old[start_index:]
        volume_old = volume_old[start_index:]
    else:
        end_index = time_old.index(end_unix) + 1
        time_old = time_old[start_index:end_index]
        price_old = price_old[start_index:end_index]
        volume_old = volume_old[start_index:end_index]

    print()
    print("Time list:", len(time_old))
    print(time_old[0:3], time_old[-3:])

    for i in range(1, len(time_old)):
        if time_old[i] - time_old[i - 1] !=60:
            print("THERE IS AN ERROR AT", time_old[i])

    print("Prices:", len(price_old))
    print("Volumes:", len(volume_old))
    print()

    time_new = []
    price_new = []
    volume_new = []

    if len(month_list) != 0:
        for month in month_list:  # iterate through the new files
            filename_new = location + exc_name + "/" + year + month + ".csv"
            time_new, price_new, volume_new = price_volume_from_raw(filename_new, time_new, price_new, volume_new, semi=1,
                                                                    unix=0)

        print("Len of new:", len(volume_new))
        print("Len of old:", len(price_old))

        time_list = np.append(time_old, time_new)
        prices = np.append(price_old, price_new)
        volumes = np.append(volume_old, volume_new)

        prices = remove_nan(prices)
        prices = supp.fill_blanks(prices)
        volumes = remove_nan(volumes)
    else:
        prices = remove_nan(price_old)
        prices = supp.fill_blanks(prices)
        volumes = remove_nan(volume_old)
        time_list = time_old

    print("Len of combined:", len(volumes))
    time_list = make_excel_stamp_list(startstamp=start_date, endstamp=end_date)

    print()
    print("Time list:", len(time_list))
    print(time_list[0:3], time_list[-3:])
    print("Prices:", len(prices))
    print("Volumes:", len(volumes))
    print()
    write_filename = "data/export_csv/" + exc_name + "_edit.csv"

    with open(write_filename, 'w', newline='') as csvfile:
        writ = csv.writer(csvfile, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        print("\033[0;32;0m Writing to file '%s'...\033[0;0;0m" % write_filename)

        header1 = [" "]
        header2 = [" "]
        header3 = ["Time"]
        currency = exc_name[- 3:]
        header1.append(exc)
        header1.append("")
        header2.append("Closing price")
        header2.append("Volume")
        header3.append(currency.upper())
        header3.append("BTC")

        writ.writerow(header1)
        writ.writerow(header2)
        writ.writerow(header3)

        for i in range(len(prices)):
            rowdata = [time_list[i]]
            rowdata.append(prices[i])
            rowdata.append(volumes[i])
            writ.writerow(rowdata)


def price_volume_from_raw(file_name, time_list, price, volume, semi=0, unix=1, price_col=4):

    with open(file_name, newline='') as csvfile:
        if semi == 0:
            reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        else:
            reader = csv.reader(csvfile, delimiter=';', quotechar='|')
        print("\033[0;32;0m Reading file '%s'...\033[0;0;0m" % file_name)
        i = 0
        next(reader)
        try:
            for row in reader:
                    try:
                        if unix == 1:
                            time_list.append(int(row[0]))
                        else:
                            time_list.append(str(row[0]))
                        price.append(float(row[price_col]))
                        volume.append(float(row[price_col + 1]))
                    except ValueError:
                        print("\033[0;31;0m There was an error on row %i in '%s'\033[0;0;0m" % (i + 1, file_name))
                    i = i + 1
        except UnicodeDecodeError:
            print("      i =", i)
        return time_list, price, volume


def make_single_excel_stamp(y, mo, d, h, mi):
    ys = str(y)
    if mo < 10:
        mos = "0" + str(mo)
    else:
        mos = str(mo)
    if d < 10:
        ds = "0" + str(d)
    else:
        ds = str(d)
    if h < 10:
        hs = "0" + str(h)
    else:
        hs = str(h)
    if mi < 10:
        mis = "0" + str(mi)
    else:
        mis = str(mi)
    stamp = ds + "." + mos + "." + ys + " " + hs + ":" + mis
    return stamp


def make_excel_stamp_list(startstamp="01.01.2012 00:00", endstamp="31.12.2017 23:59"):

    excel_stamps = [startstamp]
    i = 0
    while excel_stamps[i] != endstamp:
        d = int(excel_stamps[i][0:2])
        mo = int(excel_stamps[i][3:5])
        y = int(excel_stamps[i][6:10])
        h = int(excel_stamps[i][11:13])
        mi = int(excel_stamps[i][14:16])

        if mo == 1 or mo == 3 or mo == 5 or mo == 7 or mo == 8 or mo == 10 or mo == 12:
            n_days = 31
        elif mo == 2:
            if y % 4 == 0:
                n_days = 29
            else:
                n_days = 28
        else:
            n_days = 30

        if mi != 59:
            mi = mi + 1
        elif h != 23:
            mi = 0
            h = h + 1
        elif d != n_days:
            mi = 0
            h = 0
            d = d + 1
        elif mo != 12:
            mi = 0
            h = 0
            d = 1
            mo = mo + 1
        else:
            mi = 0
            h = 0
            d = 1
            mo = 1
            y = y + 1

        excel_stamps.append(make_single_excel_stamp(y, mo, d, h, mi))
        i += 1

    return excel_stamps


def remove_nan(in_list):
    out_list = in_list
    n = len(in_list)
    count_nans = 0
    for i in range(0, n):
        if in_list[i] != in_list[i]:
            out_list[i] = 0
    return out_list


def convert_to_hour(time_stamps, prices, volumes):
    print("  \033[32;0;0mConverting to hourly data...\033[0;0;0m")
    year, month, day, hour, minute = supp.fix_time_list(time_stamps)
    n_mins = len(time_stamps)
    if n_mins % 60 != 0:
        print("WARNING: convert_to_hour found an uneven number of minutes, with %i to spare" % (n_mins % 60))
        n_mins -= n_mins % 60
    try:
        np.size(prices, 1)
        n_exc = np.size(prices, 0)
    except IndexError:
        n_exc = 1

    n_hours = int((n_mins) / 60)

    time_stamps_out = []
    if n_exc > 1:
        volumes_out = np.zeros([n_exc, n_hours])
        prices_out = np.zeros([n_exc, n_hours])
        for exc in range(n_exc):
            k = 0
            for t in range(0, n_mins, 60):
                volumes_out[exc, k] = sum(volumes[exc, t:t+60])
                prices_out[exc, k] = prices[exc, t+59]
                k += 1
                if exc == 0:
                    time_stamps_out.append(time_stamps[t + 59])
    else:
        volumes_out = []
        prices_out = []
        for t in range(0, n_mins, 60):
            volumes_out.append(sum(volumes[t:t + 60]))
            time_stamps_out.append(time_stamps[t])
            prices_out.append(prices[t + 59])
    print("  \033[32;0;0mConversion complete...\033[0;0;0m")
    return time_stamps_out, prices_out, volumes_out


def convert_to_day(time_stamps, prices, volumes):
    print("  \033[32;0;0mConverting to daily data...\033[0;0;0m")
    year, month, day, hour, minute = supp.fix_time_list(time_stamps)
    n_mins = len(time_stamps)

    try:
        np.size(prices, 1)
        n_exc = np.size(prices, 0)
    except IndexError:
        n_exc = 1

    start_minute = hour[0] * 60 + minute[0]
    minutes_first_day = 1440 - start_minute

    n_days = int((n_mins) / 1440)  # THIS IS A POSSIBLE BUG WITHOUT +1

    time_stamps_out = []
    time_stamps_out.append(time_stamps[0])
    if n_exc > 1:
        volumes_out = np.zeros([n_exc, n_days])
        prices_out = np.zeros([n_exc, n_days])
        for exc in range(n_exc):

            for t in range(0, minutes_first_day):
                volumes_out[exc, 0] += volumes[exc, t]
            prices_out[exc, 0] = prices[exc, minutes_first_day - 1]

            k = 1
            for t in range(minutes_first_day, min(n_mins, n_mins - start_minute), 1440):
                volumes_out[exc, k] = sum(volumes[exc, t - 1440:t])
                prices_out[exc, k] = prices[exc, t]
                time_stamps_out.append(time_stamps[t])
                k += 1
    else:
        volumes_out = [0]
        prices_out = [0]
        for t in range(0, minutes_first_day):
            volumes_out[0] += volumes[t]
        prices_out[0] = prices[minutes_first_day - 1]

        for t in range(minutes_first_day, min(n_mins, n_mins - start_minute), 1440):
            volumes_out.append(sum(volumes[t:t + 1440]))
            prices_out.append(prices[t + 1439])
            time_stamps_out.append(time_stamps[t])
    print("  \033[32;0;0mConversion complete...\033[0;0;0m")
    return time_stamps_out, prices_out, volumes_out


def get_month(month_string):
    month_string = month_string.lower()
    if month_string == "jan":
        month_num = 1
    elif month_string == "feb":
        month_num = 2
    elif month_string == "mar":
        month_num = 3
    elif month_string == "apr":
        month_num = 4
    elif month_string == "may":
        month_num = 5
    elif month_string == "jun":
        month_num = 6
    elif month_string == "jul":
        month_num = 7
    elif month_string == "aug":
        month_num = 8
    elif month_string == "sep":
        month_num = 9
    elif month_string == "oct":
        month_num = 10
    elif month_string == "nov":
        month_num = 11
    elif month_string == "dec":
        month_num = 12
    else:
        print("Error in dis.get_month!")
        month_num = -1
    return month_num


def cyclical_average(time_list, data, frequency="h", print_n_entries=0, print_val_tab=0, time_zone_conversion=0):
    year, month, day, hour, minute = supp.fix_time_list(time_list, move_n_hours=time_zone_conversion)
    n_entries = len(time_list)
    day_time = []  # Excel stamps for each minute in the day
    h_list = []  # integer indicating which hour it is
    m_list = []  # integer indicating which minute it is

    # Generating day_time ---------------
    if frequency == "h":
        for h in range(0, 24):
            if h < 10:
                hs = "0" + str(h)
            else:
                hs = str(h)
            day_time.append(hs + ":" + "00")
            h_list.append(h)
    elif frequency == "d":
        day_time = ["Mon", "Tue", "Wed", "Thur", "Fri", "Sat", "Sun"]
    # -----------------------------------

    # Calculating averages
    n_out = len(day_time)
    lower = np.zeros(n_out)
    upper = np.zeros(n_out)
    data_average = np.zeros(n_out)
    count_entries = np.zeros(n_out)  # Will count actual observations, to get correct numerator in mean
    temp_list = np.zeros(n_out)

    n_cycles = int(2 * n_entries / n_out)  # trenger bare være minst like stor. Sikkerhetsmargin på 50%
    temp_matrix = np.zeros([n_cycles, n_out])
    for i in range(n_entries):
        if data[i] != 0:
            if frequency == "h":
                index = int(hour[i])
            elif frequency == "d":
                index = int(date(year[i], month[i], day[i]).isoweekday()) - 1
            cycle_nr = int(count_entries[index])
            count_entries[index] += 1
            temp_matrix[cycle_nr, index] = data[i]

    temp_matrix = np.matrix(temp_matrix)
    percentile = 0.95

    if print_val_tab == 1:
        for i in range(n_cycles):
            for j in range(7):
                print('{0:.3f}'.format(temp_matrix[i, j]), end='   ')
            print()

    if print_n_entries == 1:
        print(count_entries)

    for i in range(n_out):
        data_average[i] = float(np.sum(temp_matrix[:, i]) / count_entries[i])  # takes the mean
        lower[i], upper[i] = st.t.interval(percentile, len(temp_matrix[:, i]) - 1, loc=data_average[i],
                                           scale=st.sem(temp_matrix[:, i]))

    return day_time, data_average, lower, upper


def volume_transformation(volume, initial_mean_volume, daily=1):
    n_entries = len(volume)
    if daily == 1:
        n_entries_in_window = min(365, n_entries)
    else:
        n_entries_in_window = min((365 * 24, n_entries))

    out_volume = np.zeros(n_entries)
    for i in range(0, n_entries_in_window):
        floating_mean = (initial_mean_volume * (n_entries_in_window - i) + i * np.mean(
            volume[0: i])) / n_entries_in_window
        out_volume[i] = np.log(volume[i]) - np.log(floating_mean)
    for i in range(n_entries_in_window, n_entries):
        if volume[i] == 0 or np.mean(volume[i - n_entries_in_window:i]) == 0:
            out_volume[i] = 0
        else:
            out_volume[i] = np.log(volume[i]) - np.log(np.mean(volume[i - n_entries_in_window:i - 1]))
    out_volume[0] = np.log(volume[0]) - np.log(initial_mean_volume)
    return out_volume


def clean_series_days(time_listM, pricesM, volumesM, exc=0, print_days_excluded=0, convert_time_zones=1, plot_for_extreme=0):
    print(" \033[32;0;0mRunning 'clean_series_days' ...\033[0;0;0m")
    if convert_time_zones:
        if exc == 0:
            n_hours = 0
        elif exc == 1:
            n_hours = 9
        elif exc == 2:
            n_hours = 8
        elif exc ==3:
            n_hours = -8
        elif exc == 9:
            n_hours = 9
        else:
            n_hours = 0
        print("  Converting time zones: moving series %i hours" % n_hours)
    else:
        n_hours = 0

    year, month, day, hour, minute = supp.fix_time_list(time_listM, move_n_hours=n_hours)
    if n_hours != 0:
        time_listM = supp.make_time_list(year, month, day, hour, minute)

    time_listD, pricesD, volumesD = convert_to_day(time_listM, pricesM, volumesM)

    end_time_D = ""
    if exc == 0:
        cutoff_date = "01.01.2013 00:00"
        cutoff_min_date = cutoff_date
        start_averaging_date = "01.01.2012 00:00"
    elif exc == 1:
        cutoff_date = "01.01.2016 00:00"
        cutoff_min_date = "01.01.2016 09:00"
        start_averaging_date = "30.10.2014 00:00"
    elif exc == 2:
        cutoff_date = "01.01.2013 00:00"
        cutoff_min_date = "01.01.2013 08:00"
        end_time_D = "01.01.2017 00:00"
        end_time_M = "01.01.2017 08:00"
        start_averaging_date = "01.01.2012 00:00"
    elif exc == 3:
        cutoff_date = "01.01.2015 00:00"
        cutoff_min_date = "01.01.2015 16:00"
        start_averaging_date = "02.12.2014 00:00"
    elif exc == 4:
        cutoff_date = "01.01.2014 00:00"
        cutoff_min_date = "01.01.2014 09:00"
        start_averaging_date = "01.10.2013 00:00"
    else:
        print("  TEST SET")
        cutoff_date = "01.01.2017 00:00"
        cutoff_min_date = "01.01.2017 00:00"
        start_averaging_date = "01.01.2017 00:00"

    cutoff_day = supp.find_date_index(cutoff_date, time_listD)
    cutoff_min = supp.find_date_index(cutoff_min_date, time_listM)
    start_averaging_day = supp.find_date_index(start_averaging_date, time_listD)
    mean_volume_prev_year = np.average(volumesD[start_averaging_day:cutoff_day])
    if len(end_time_D) > 1:
        cutoff_endD = supp.find_date_index(end_time_D, time_listD)
        cutoff_endM = supp.find_date_index(end_time_M, time_listM)
    else:
        cutoff_endD = len(time_listD)
        cutoff_endM = len(time_listM)

    n_total = len(time_listD)
    n_0 = cutoff_endD

    time_listM = time_listM[cutoff_min:cutoff_endM]
    print("  Only including days after", time_listM[0], "to", time_listM[len(time_listM) - 1])
    pricesM = pricesM[cutoff_min:cutoff_endM]
    volumesM = volumesM[cutoff_min:cutoff_endM]
    pricesD = pricesD[cutoff_day:cutoff_endD]
    volumesD = volumesD[cutoff_day:cutoff_endD]
    time_listD = time_listD[cutoff_day:cutoff_endD]

    n_1 = len(time_listD)  # After removing 2012

    # Rolls
    spread_abs, spreadD, time_list_rolls, count_value_error = rolls.rolls(pricesM, time_listM, calc_basis="d", kill_output=1)

    # Realized volatility
    rvolD, RVol_time = realized_volatility.RVol(time_listM, pricesM, daily=1, annualize=1)

    # Returns
    returnsM = jake_supp.logreturn(pricesM)
    returnsD = jake_supp.logreturn(pricesD)
    # Amihud's ILLIQ
    illiq_timeD, illiqD = ILLIQ.illiq(time_listM, returnsM, volumesM, threshold=0)  # Already clean

    # print()
    # print("TABLE OF TIME STARTS AND ENDS")
    # print("Minutes", len(time_listM))
    # print(" ", time_listM[0], time_listM[len(time_listM)-1])
    # print("Days", len(time_listD))
    # print(" ", time_listD[0], time_listD[len(time_listD)-1])
    # print("Spread", len(time_list_rolls))
    # print(" ", time_list_rolls[0], time_list_rolls[len(time_list_rolls)-1])
    # print("RVOL", len(RVol_time))
    # print(" ", RVol_time[0], RVol_time[len(RVol_time)-1])
    # print("illiq", len(illiq_timeD))
    # print(" ", illiq_timeD[0], illiq_timeD[len(illiq_timeD)-1])
    # print()
    if plot_for_extreme == 1:
        plt.plot(rvolD)
        plt.title("Raw rvol")
        plt.figure()
        plt.plot(spreadD)
        plt.title("Raw spreadH")
        plt.figure()
        plt.plot(volumesD)
        plt.title("Raw volume")
        plt.figure()
        plt.plot(illiqD)
        plt.title("Raw illiq")
        plt.figure()
        plt.plot(returnsD)
        plt.title("Raw returnsH")
        plt.figure()

    n_2 = len(time_listD)  # After removing zero-volume
    time_list_removed = []
    # Removing all days where Volume is zero
    time_listD, time_list_removed, volumesD, spreadD, returnsD, rvolD = supp.remove_list1_zeros_from_all_lists(time_listD, time_list_removed, volumesD, spreadD, returnsD, rvolD)

    # --------------------------------------------
    days_to_remove = []
    if exc == 0:
        days_to_remove = supp.remove_extremes(days_to_remove, returnsD, 0.1, threshold_lower=-0.1)
        days_to_remove = supp.remove_extremes(days_to_remove, rvolD, 2)
        days_to_remove = supp.remove_extremes(days_to_remove, spreadD, 0.01)
        days_to_remove = supp.remove_extremes(days_to_remove, illiqD, 0.1)
    elif exc == 1:
        days_to_remove = supp.remove_extremes(days_to_remove, returnsD, 0.1, threshold_lower=-0.1)
        days_to_remove = supp.remove_extremes(days_to_remove, rvolD, 2)
        days_to_remove = supp.remove_extremes(days_to_remove, spreadD, 0.01)
        days_to_remove = supp.remove_extremes(days_to_remove, illiqD, 0.1)
    elif exc == 2:
        days_to_remove = supp.remove_extremes(days_to_remove, returnsD, 0.1, threshold_lower=-0.1)
        days_to_remove = supp.remove_extremes(days_to_remove, rvolD, 2)
        days_to_remove = supp.remove_extremes(days_to_remove, spreadD, 0.01)
        days_to_remove = supp.remove_extremes(days_to_remove, illiqD, 0.1)
    elif exc == 3:
        days_to_remove = supp.remove_extremes(days_to_remove, returnsD, 0.1, threshold_lower=-0.1)
        days_to_remove = supp.remove_extremes(days_to_remove, rvolD, 2)
        days_to_remove = supp.remove_extremes(days_to_remove, spreadD, 0.01)
        days_to_remove = supp.remove_extremes(days_to_remove, volumesD, 50000)
        days_to_remove = supp.remove_extremes(days_to_remove, illiqD, 0.01)
    elif exc == 4:
        days_to_remove = supp.remove_extremes(days_to_remove, returnsD, 0.1, threshold_lower=-0.1)
        days_to_remove = supp.remove_extremes(days_to_remove, rvolD, 2)
        days_to_remove = supp.remove_extremes(days_to_remove, spreadD, 0.01)
        days_to_remove = supp.remove_extremes(days_to_remove, volumesD, 50000)
        days_to_remove = supp.remove_extremes(days_to_remove, illiqD, 0.01)

    for d in days_to_remove:
        time_list_removed = np.append(time_list_removed, time_listD[d])
    time_listD = np.delete(time_listD, days_to_remove)
    returnsD = np.delete(returnsD, days_to_remove)
    volumesD = np.delete(volumesD, days_to_remove)
    spreadD = np.delete(spreadD, days_to_remove)
    rvolD = np.delete(rvolD, days_to_remove)
    illiqD = np.delete(illiqD, days_to_remove)
    illiq_timeD = np.delete(illiq_timeD, days_to_remove)

    if plot_for_extreme == 1:
        plt.plot(rvolD)
        plt.title("rvol")
        plt.figure()
        plt.plot(spreadD)
        plt.title("spreadH")
        plt.figure()
        plt.plot(volumesD)
        plt.title("volume")
        plt.figure()
        plt.plot(illiqD)
        plt.title("illiq")
        plt.figure()
        plt.plot(returnsD)
        plt.title("returnsH")
        plt.show()

    n_3 = len(time_listD)  # After removing the extremes

    # Removing all days where Roll is zero
    time_listD, time_list_removed, spreadD, volumesD, returnsD, \
    rvolD, illiqD = supp.remove_list1_zeros_from_all_lists(time_listD,
                                                           time_list_removed,
                                                           spreadD,
                                                           volumesD,
                                                           returnsD,
                                                           rvolD,
                                                           illiqD)

    n_4 = len(time_listD)  # After removing the zero-roll

    # Removing all days where Volatility is zero
    time_listD, time_list_removed, rvolD, volumesD, returnsD, \
    spreadD, illiqD = supp.remove_list1_zeros_from_all_lists(time_listD,
                                                             time_list_removed,
                                                             rvolD,
                                                             volumesD,
                                                             returnsD,
                                                             spreadD, illiqD)

    n_5 = len(time_listD)  # After removing the zero-volatility

    # Turning ILLIQ, Volume and RVol into log
    log_illiqD = np.log(illiqD)
    log_rvolD = np.log(rvolD)
    log_volumesD = volume_transformation(volumesD, mean_volume_prev_year)

    print("  dis.%i: Length of time %i, spread %i, rvol %i, illiq %i, and log_illiq %i" % (gf(cf()).lineno, len(time_listD), len(spreadD), len(rvolD), len(illiqD), len(log_illiqD)))
    print(" \033[32;0;0m Finished running 'clean_series_days' ...\033[0;0;0m")

    return time_listD, returnsD, volumesD, log_volumesD, spreadD, illiqD, log_illiqD, rvolD, log_rvolD


def clean_series_hour(time_listM, pricesM, volumesM, exc=0, convert_time_zones=1, plot_for_extreme=0):
    remove_extremes = 1
    print(" \033[32;0;0mRunning 'clean_series_hour' ...\033[0;0;0m")
    if convert_time_zones:  # Flytter nå Coincheck ni timer, men lar Bitstamp stå
        if exc == 0:
            n_hours = 0
        elif exc == 1:
            n_hours = 9
        elif exc == 2:
            n_hours = 8
        elif exc ==3:
            n_hours = -8
        elif exc ==4:
            n_hours =9
        else:
            n_hours = 0
        print("  Converting time zones: moving series %i hours" % n_hours)
    else:
        n_hours = 0

    year, month, day, hour, minute = supp.fix_time_list(time_listM, move_n_hours=n_hours)  # Flytter nå Coincheck ni timer, men lar Bitstamp stå

    if n_hours != 0:
        time_listM = supp.make_time_list(year, month, day, hour,
                                         minute)  # Lager en ny tidsliste fra de flyttede listene

    returnsM = jake_supp.logreturn(pricesM)
    time_listH, pricesH, volumesH = convert_to_hour(time_listM, pricesM, volumesM)
    returnsH = jake_supp.logreturn(pricesH)

    spread_abs, spreadH, time_list_spread, count_value_error = rolls.rolls(pricesM, time_listM, calc_basis="h", kill_output=1)
    illiq_hours_time, illiqH = ILLIQ.illiq(time_listM, returnsM, volumesM, hourly_or_daily="h", threshold=0)
    rvolH, time_list_rvol = realized_volatility.RVol(time_listM, pricesM, daily=0, annualize=1)

    n_0 = len(time_listH)  # initial number of hours

    time_list_removed = []
    # Removing all hours where Volume is zero
    time_listH, time_list_removed, volumesH, spreadH, returnsH, rvolH = supp.remove_list1_zeros_from_all_lists(time_listH, time_list_removed, volumesH, spreadH, returnsH, rvolH)

    print("  dis.%i: Number of hours removed due to zero-volume: %i" % (gf(cf()).lineno, len(time_list_removed)))
    n_1 = len(time_listH)  # After removing the zero-volume
    end_time = ""

    if exc == 0:
        cutoff_date = "01.01.2013 00:00"
        start_averaging_date = "01.01.2012 00:00"
    elif exc == 1:
        cutoff_date = "01.06.2016 00:00"
        start_averaging_date = "30.10.2014 00:00"
    elif exc == 2:
        cutoff_date = "01.01.2013 00:00"
        start_averaging_date = "01.01.2012 00:00"
        end_time = "30.09.2017 00:00"
    elif exc ==3:
        cutoff_date = "01.01.2015 00:00"
        start_averaging_date = "02.12.2014 00:00"
    elif exc ==4:
        cutoff_date = "01.01.2014 00:00"
        start_averaging_date = "01.10.2013 00:00"
    else:
        print("  TEST SET")
        cutoff_date = "01.01.2017 00:00"
        start_averaging_date = "01.01.2017 00:00"


    cutoff_hour = supp.find_date_index(cutoff_date, time_listH)
    start_averaging_hour = supp.find_date_index(start_averaging_date, time_listH)
    if len(end_time) > 1:
        end_hour = supp.find_date_index(end_time, time_listH)
    else:
        end_hour = len(time_listH) - 1

    mean_volume_prev_year = np.average(volumesH[start_averaging_hour:cutoff_hour])

    time_listH = time_listH[cutoff_hour:end_hour]
    print("  Only including days after", time_listH[0], "to", time_listH[-1])
    returnsH = returnsH[cutoff_hour:end_hour]
    volumesH = volumesH[cutoff_hour:end_hour]
    spreadH = spreadH[cutoff_hour:end_hour]
    illiqH = illiqH[cutoff_hour:end_hour]
    rvolH = rvolH[cutoff_hour:end_hour]

    if plot_for_extreme == 1:
        # plt.plot(rvolH)
        # plt.title("Raw rvol")
        # plt.figure()
        plt.plot(spreadH)
        plt.title("Raw spreadH")
        plt.figure()
        plt.plot(volumesH)
        plt.title("Raw volume")
        plt.figure()
        plt.plot(illiqH)
        plt.title("Raw illiq")
        plt.figure()
        # plt.plot(returnsH)
        # plt.title("Raw returnsH")
        # plt.figure()

    n_1 = len(time_listH)

    hours_to_remove = []

    if remove_extremes == 1:
        if exc == 0:
            hours_to_remove = supp.remove_extremes(hours_to_remove, returnsH, 0.1, threshold_lower=-0.1)
            hours_to_remove = supp.remove_extremes(hours_to_remove, rvolH, 2)
            hours_to_remove = supp.remove_extremes(hours_to_remove, spreadH, 0.01)
            hours_to_remove = supp.remove_extremes(hours_to_remove, illiqH, 0.1)
        elif exc == 1:
            hours_to_remove = supp.remove_extremes(hours_to_remove, returnsH, 0.075, threshold_lower=-0.075)
            hours_to_remove = supp.remove_extremes(hours_to_remove, rvolH, 2)
            hours_to_remove = supp.remove_extremes(hours_to_remove, spreadH, 0.1)
            hours_to_remove = supp.remove_extremes(hours_to_remove, illiqH, 0.1)
        elif exc == 2:
            hours_to_remove = supp.remove_extremes(hours_to_remove, returnsH, 0.075, threshold_lower=-0.075)
            hours_to_remove = supp.remove_extremes(hours_to_remove, rvolH, 2)
            hours_to_remove = supp.remove_extremes(hours_to_remove, spreadH, 0.1)
            hours_to_remove = supp.remove_extremes(hours_to_remove, illiqH, 0.1)
        elif exc == 3:
            hours_to_remove = supp.remove_extremes(hours_to_remove, returnsH, 0.075, threshold_lower=-0.075)
            hours_to_remove = supp.remove_extremes(hours_to_remove, rvolH, 2)
            hours_to_remove = supp.remove_extremes(hours_to_remove, volumesH, 15000)
            hours_to_remove = supp.remove_extremes(hours_to_remove, spreadH, 0.1)
            hours_to_remove = supp.remove_extremes(hours_to_remove, illiqH, 0.02)
        elif exc == 4:
            hours_to_remove = supp.remove_extremes(hours_to_remove, returnsH, 0.075, threshold_lower=-0.075)
            hours_to_remove = supp.remove_extremes(hours_to_remove, rvolH, 2)
            hours_to_remove = supp.remove_extremes(hours_to_remove, volumesH, 15000)
            hours_to_remove = supp.remove_extremes(hours_to_remove, spreadH, 0.1)
            hours_to_remove = supp.remove_extremes(hours_to_remove, illiqH, 0.02)

    time_listH = np.delete(time_listH, hours_to_remove)
    returnsH = np.delete(returnsH, hours_to_remove)
    volumesH = np.delete(volumesH, hours_to_remove)
    spreadH = np.delete(spreadH, hours_to_remove)
    illiqH = np.delete(illiqH, hours_to_remove)
    rvolH = np.delete(rvolH, hours_to_remove)

    if plot_for_extreme == 1:
        plt.plot(rvolH)
        plt.title("rvol")
        plt.figure()
        plt.plot(spreadH)
        plt.title("spreadH")
        plt.figure()
        plt.plot(volumesH)
        plt.title("volume")
        plt.figure()
        plt.plot(illiqH)
        plt.title("illiq")
        plt.figure()
        plt.plot(returnsH)
        plt.title("returnsH")

    # Removing all days where Roll is zero
    time_listH, time_list_removed, spreadH, volumesH, returnsH, illiqH, rvolH = supp.remove_list1_zeros_from_all_lists(time_listH,time_list_removed,spreadH,volumesH,returnsH,illiqH, rvolH)


    # Removing all hours where Rvol is zero
    time_listH, time_list_removed, rvolH, spreadH, volumesH, returnsH, illiqH = supp.remove_list1_zeros_from_all_lists(time_listH, time_list_removed,rvolH,spreadH,volumesH,returnsH,illiqH)

    # Removing all hours where ILLIQ is zero
    time_listH, time_list_removed, illiqH , rvolH, spreadH, volumesH, returnsH= supp.remove_list1_zeros_from_all_lists(time_listH, time_list_removed,illiqH,rvolH,spreadH,volumesH,returnsH)

    # Turning ILLIQ, Volume and rvol into log
    log_illiqH = np.log(illiqH)
    log_volumesH = volume_transformation(volumesH, mean_volume_prev_year)
    log_rvolH = np.log(rvolH)

    if plot_for_extreme==1:
        plt.show()

    print("  dis.%i: Length of time %i, spread %i, rvol %i, illiq %i, and log_illiq %i" % (gf(cf()).lineno, len(time_listH), len(spreadH), len(rvolH), len(illiqH), len(log_illiqH)))
    print(" \033[32;0;0mFinished running 'clean_series_hour' ...\033[0;0;0m")
    return time_listH, returnsH, spreadH, volumesH, log_volumesH, illiqH, log_illiqH, rvolH, log_rvolH


def read_single_exc_csvs(file_name, time_list, price, volume):
    with open(file_name, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=';', quotechar='|')
        print("\033[0;32;0m Reading file '%s'...\033[0;0;0m" % file_name)
        i = 0
        next(reader)
        for row in reader:
            try:
                time_list.append(row[0])
                price.append(float(row[7]))
                volume.append(float(row[5]))
            except ValueError:
                print("\033[0;31;0m There was an error on row %i in '%s'\033[0;0;0m" % (i + 1, file_name))
            i = i + 1
    print("\033[0;32;0m Finished reading file '%s'...\033[0;0;0m" % file_name)
    return time_list, price, volume


def quick_import(exc=0):

    price_col = 4  # Column number in the raw file
    if exc == 1:
        name = "coincheckjpy"
    elif exc == 2:
        name = "btcncny"
    elif exc == 3:
        name = "coinbaseusd"
    elif exc == 4:
        name = "korbitkrw"
        price_col = 1 # Column number in the raw file
    else:
        name = "bitstampusd"

    file_name = "data/long_raw_data/" + name + ".csv"
    time_listM = []
    priceM = []
    volumeM = []
    time_listM, priceM, volumeM = price_volume_from_raw(file_name, time_listM, priceM, volumeM, semi=0, unix=1, price_col=price_col)

    return time_listM, priceM, volumeM


def write_to_csv(exc_name, time_list, price, volume):
    location = "data/export_csv/"
    file_name = location + exc_name + "_edit.csv"
    with open(file_name, 'w', newline='') as csvfile:
        writ = csv.writer(csvfile, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        print("\033[0;32;0m Writing to file '%s'...\033[0;0;0m" % file_name)

        header1 = [" "]
        header2 = [" "]
        header3 = ["Time"]
        currency = exc_name[-3:]
        header1.append(exc_name[0:-2])
        header1.append("")
        header2.append("Closing price")
        header2.append("Volume")
        header3.append(currency.upper())
        header3.append("BTC")

        writ.writerow(header1)
        writ.writerow(header2)
        writ.writerow(header3)

        for i in range(len(price)):
            rowdata = [time_list[i]]
            rowdata.append(price[i])
            rowdata.append(volume[i])
            writ.writerow(rowdata)


def import_from_csv_w_ticks(exc_name, start_stamp, end_stamp):
    full_list_excel_time = make_excel_stamp_list(startstamp=start_stamp, endstamp=end_stamp)
    time_listM,priceM,volumeM=quick_import(4)
    price=np.zeros(len(full_list_excel_time))
    volume=np.zeros(len(full_list_excel_time))

    j=0 #j follows the imported dataset timelist. The intention is to save the work of searching through the whole series every time.
    t=0 #t follows the new generated timelist
    while (j != len(time_listM)):
        if t==len(full_list_excel_time):
            break
        else:
            while (unix_to_timestamp(time_listM[j])!=full_list_excel_time[t]): #Increase t in the generated timeseries until it is equal to the j in the imported dataset
                if t==len(full_list_excel_time):
                    break
                else:
                    t=t+1

            while unix_to_timestamp(time_listM[j]) == full_list_excel_time[t]: #Increase j to capture multiple trades on the same minute
                price[t]=price[t]+priceM[j]*volumeM[j]
                volume[t]=volume[t]+volumeM[j]
                j=j+1
                if j==len(time_listM):
                    break
            if volume[t]!=0:
                price[t]=price[t]/volume[t]
    price = supp.fill_blanks(price)
    write_to_csv(exc_name, full_list_excel_time, price, volume)
