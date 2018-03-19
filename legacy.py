import csv

import numpy as np

import data_import_support as dis
from Sondre import sondre_support_formulas as supp
from data_import_support import remove_nan, get_month, price_volume_from_raw, make_single_excel_stamp


def remove_list1_outliers_from_all_lists(list1, list2=[], list3=[], list4=[], threshold=2):
    # threshold is in number of standard deviations
    # only chekcs for positive deviations
    t_list2 = False
    t_list3 = False
    t_list4 = False
    if len(list2) > 1:
        t_list2 = True
    if len(list3) > 1:
        t_list3 = True
    if len(list4) > 1:
        t_list4 = True

    n_in = len(list1)
    std = np.std(list1)
    mean = np.mean(list1)
    list1_min = mean - threshold * std
    list1_max = mean + threshold * std
    out_list1 = []
    if t_list2:
        out_list2 = []
    if t_list3:
        out_list3 = []
    if t_list4:
        out_list4 = []
    for i in range(0, n_in):
        if list1[i] < list1_max:
            out_list1.append(list1[i])
            if t_list2:
                out_list2.append(list2[i])
            if t_list3:
                out_list3.append(list3[i])
            if t_list4:
                out_list4.append(list4[i])
    if t_list4:
        return out_list1, out_list2, out_list3, out_list4
    elif t_list3:
        return out_list1, out_list2, out_list3
    elif t_list2:
        return out_list1, out_list2
    else:
        return out_list1


def get_hilo(opening_hours="n"):
    exchanges = ["bitstampusd"]
    n_exc = len(exchanges)
    print("Fetching minute data...")

    if opening_hours == "y":
        oh = ""
        print(" \033[32;0;0mOnly fetching data for NYSE opening hours...\033[0;0;0m")
    else:
        oh = "_full_day"

    file_name = "data/export_csv/hilo_minute_data" + oh + ".csv"
    time_list, high, low = fetch_aggregate_csv_hilo(file_name, n_exc)
    return exchanges, time_list, high, low


def fetch_long_and_write_hilo(exchanges, opening_hours_only="y"):
    n_exc = len(exchanges)
    excel_stamps, unix_stamps, high, low = get_hilo_from_fulls(exchanges)

    if opening_hours_only == "y":
        excel_stamps, high, low = dis.opening_hours(excel_stamps, high, low)
        filename = "data/export_csv/hilo_minute_data.csv"
    else:
        filename = "data/export_csv/hilo_minute_data_full_day.csv"

    write_hilo_to_csv(high, low, excel_stamps, exchanges, filename)#####


def import_gold_lists(s_year=2012, s_month=1, e_year=2017, e_month=9):
    date = []
    time_NYC = []
    volume = []
    price = []
    bid = []
    ask = []
    if e_year == s_year:
        y = e_year  # =s_year
        for m in range(s_month, e_month):
            if m < 10:
                ms = "0" + str(m)
            else:
                ms = str(m)
            file_name = "data/gold_raw/-" + str(y) + "-" + ms + "-SPY.P.csv"
            date, time_NYC, volume, price, bid, ask = dis.read_raw_gold(file_name, date, time_NYC, volume, price, bid, ask)
    else:
        for y in range(s_year, e_year + 1):
            if y == s_year:
                for m in range(s_month, 12 + 1):
                    if m < 10:
                        ms = "0" + str(m)
                    else:
                        ms = str(m)
                    file_name = "data/gold_raw/-" + str(y) + "-" + ms + "-SPY.P.csv"
                    date, time_NYC, volume, price, bid, ask = dis.read_raw_gold(file_name, date, time_NYC, volume, price, bid, ask)
            elif y == e_year:
                for m in range(1, e_month + 1):
                    if m < 10:
                        ms = "0" + str(m)
                    else:
                        ms = str(m)
                    file_name = "data/gold_raw/-" + str(y) + "-" + ms + "-SPY.P.csv"
                    date, time_NYC, volume, price, bid, ask = dis.read_raw_gold(file_name, date, time_NYC, volume, price, bid, ask)
            else:
                for m in range(1, 12 + 1):
                    if m < 10:
                        ms = "0" + str(m)
                    else:
                        ms = str(m)
                    file_name = "data/gold_raw/-" + str(y) + "-" + ms + "-SPY.P.csv"
                    date, time_NYC, volume, price, bid, ask = dis.read_raw_gold(file_name, date, time_NYC, volume, price, bid, ask)
    date = np.transpose(date)
    time_NYC = np.transpose(time_NYC)
    volume = np.transpose(volume)
    price = np.transpose(price)
    bid = np.transpose(bid)
    ask = np.transpose(ask)
    excel_stamps = fix_gold_stamps(date, time_NYC)
    file_name = "data/export_csv/gold_data.csv"
    write_to_gold_csvs(excel_stamps, volume, price, bid, ask, file_name)


def hilo_from_raw(file_name, time_list, high, low):
    with open(file_name, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        print("\033[0;32;0m Reading file '%s'...\033[0;0;0m" % file_name)
        i = 0
        next(reader)
        for row in reader:
            try:
                time_list.append(int(row[0]))
                high.append(float(row[2]))
                low.append(float(row[3]))
            except ValueError:
                print("\033[0;31;0m There was an error on row %i in '%s'\033[0;0;0m" % (i + 1, file_name))
            i = i + 1
        return time_list, high, low


def get_hilo_from_fulls(exchanges):
    n_exc = len(exchanges)
    print("Number of exchanges: ", n_exc)
    raw_folder = "data/long_raw_data/"
    unix_stamps, excel_stamps = make_time_stamps()
    n_cols = len(excel_stamps)
    high = np.zeros([n_exc, n_cols])
    low = np.zeros([n_exc, n_cols])
    for i in range(0, n_exc):
        print("Working on exchange %i/%i" % ((i + 1), n_exc))
        single_high = []
        single_low = []
        time_list = []
        file_name = raw_folder + exchanges[i] + ".csv"
        time_list, single_high, single_low = hilo_from_raw(file_name, time_list, single_high, single_low)

        # Gjør om nan til 0 og så fyller inn tomme priser
        single_high = remove_nan(single_high)
        single_low = remove_nan(single_low)
        single_high = supp.fill_blanks(single_high)
        single_low = supp.fill_blanks(single_low)

        # Må nå finne hvilken rad vi skal lime inn på
        n = len(single_high)
        r = 0

        # Check whether the first entry in time_listH is before the start of the unix_stamps
        start_j = 0
        while time_list[start_j] < unix_stamps[0]:
            start_j += 1

        for j in range(start_j, n):
            while unix_stamps[r] != time_list[j]:
                r = r + 1
            high[i, r] = single_high[j]
            low[i, r] = single_low[j]

    return excel_stamps, unix_stamps, high, low


def write_hilo_to_csv(high, low, excel_stamps, exchanges, filename):
    time_list = excel_stamps  # <-- Kun for å kunne bruke gammel syntax
    n_exc = len(exchanges)
    print("Exporting data to csv-files...")
    with open(filename, 'w', newline='') as csvfile:
        writ = csv.writer(csvfile, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        n_rows = np.size(high, 1)

        header1 = [" "]
        header2 = [" "]
        header3 = ["Time"]
        for exc in exchanges:
            currency = exc[len(exc) - 3: len(exc)]
            header1.append(exc)
            header1.append("")
            header2.append("High")
            header2.append("Low")
            header3.append(currency.lower())
            header3.append(currency.lower())

        writ.writerow(header1)
        writ.writerow(header2)
        writ.writerow(header3)
        for i in range(0, n_rows):
            rowdata = [time_list[i]]
            for j in range(0, n_exc):
                rowdata.append(high[j, i])
                rowdata.append(low[j, i])
            writ.writerow(rowdata)
    print("Export to aggregate csv \033[33;0;0m'%s'\033[0;0;0m successful" % filename)


def write_to_gold_csvs(excel_stamps, volume, price, bid, ask, filename):
    n_rows = len(excel_stamps)
    with open(filename, 'w', newline='') as csvfile:
        writ = csv.writer(csvfile, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        header1 = ["Time", "Price", "Volume", "Bid", "Ask"]
        writ.writerow(header1)
        for i in range(0, n_rows):
            rowdata = [" "]
            rowdata[0] = excel_stamps[i]
            rowdata.append(price[i])
            rowdata.append(volume[i])
            rowdata.append(bid[i])
            rowdata.append(ask[i])
            writ.writerow(rowdata)
    print("Export to aggregate csv \033[33;0;0m'%s'\033[0;0;0m successful" % filename)


def fix_gold_stamps(gold_date, time_NYC):
    n_rows = len(gold_date)
    excel_stamps = []
    for i in range(n_rows):
        day = int(gold_date[i][0:2])
        hour = int(time_NYC[i][0:2]) + 5

        if hour > 23:
            day = day + 1
            hour = hour - 24

        if day < 10:
            day_s = "0" + str(day)
        else:
            day_s = str(day)
        month = get_month(gold_date[i][3:6])
        if month < 10:
            month_s = "0" + str(month)
        else:
            month_s = str(month)
        year_s = gold_date[i][7:12]

        if hour < 10:
            hour_s = "0" + str(hour)
        else:
            hour_s = str(hour)
        min_s = time_NYC[i][3:5]
        excel_stamps.append(day_s + "." + month_s + "." + year_s + " " + hour_s + ":" + min_s)

    return excel_stamps


def fetch_aggregate_csv_hilo(file_name, n_exc):
    n_rows = supp.count_rows(file_name)
    n_exc = int(n_exc)
    print("\033[0;32;0m Reading file '%s'...\033[0;0;0m" % file_name)
    with open(file_name, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=';', quotechar='|')
        i = 0
        time_list = []
        high = np.zeros([n_exc, n_rows - 3])  # minus tre for å ikke få med headere
        low = np.zeros([n_exc, n_rows - 3])  # minus tre for å ikke få med headere
        next(reader)
        next(reader)
        next(reader)
        for row in reader:
            time_list.append(row[0])
            for j in range(0, n_exc):
                high[j, i] = row[1 + 2 * j]
                low[j, i] = row[2 + 2 * j]
            i = i + 1
    return time_list, high, low


def fuse_files(exchanges):
    n_exc = len(exchanges)
    time_old = []
    price_old1 = []
    volume_old1 = []
    price_old2 = []
    volume_old2 = []
    price_old3 = []
    volume_old3 = []

    filename_old = "data/export_csv/minute_data_full_day.csv"
    with open(filename_old, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=';', quotechar='|')
        print("\033[0;32;0m Reading file '%s'...\033[0;0;0m" % filename_old)
        next(reader)
        next(reader)
        next(reader)
        for row in reader:
            time_old.append(str(row[0]))
            price_old1.append(float(row[1]))
            volume_old1.append(float(row[2]))
            price_old2.append(float(row[3]))
            volume_old2.append(float(row[4]))
            price_old3.append(float(row[5]))
            volume_old3.append(float(row[6]))

    print("Her 1")
    print("Time old", len(time_old))
    print("Price old1", len(price_old1))
    print("Price old2", len(price_old2))
    print("Price old3", len(price_old3))

    location = "data/bitcoincharts/"
    year = "2017"
    time_new = []
    price_new = []
    volume_new = []

    exc = "bitstampusd"
    for month in ["06", "07", "08", "09", "10", "11", "12"]:  # iterate through the new files
        filename_new = location + exc + "/" + year + month + ".csv"
        time_new, price_new, volume_new = price_volume_from_raw(filename_new, time_new, price_new, volume_new, semi=1,
                                                                unix=0)

    price_new1 = remove_nan(price_new)
    price_new1 = supp.fill_blanks(price_new1)
    volume_new1 = remove_nan(volume_new)

    time_new_saved = time_new  # Denne brukes videre
    time_new = []
    price_new = []
    volume_new = []

    exc = "coincheckjpy"
    for month in ["06", "07", "08", "09", "10", "11", "12"]:  # iterate through the new files
        filename_new = location + exc + "/" + year + month + ".csv"
        time_new, price_new, volume_new = price_volume_from_raw(filename_new, time_new, price_new, volume_new, semi=1,
                                                                unix=0)

    price_new2 = remove_nan(price_new)
    price_new2 = supp.fill_blanks(price_new2)
    volume_new2 = remove_nan(volume_new)

    time_new = []
    price_new = []
    volume_new = []

    exc = "btcncny"
    for month in ["06", "07", "08", "09"]:  # iterate through the new files
        filename_new = location + exc + "/" + year + month + ".csv"
        time_new, price_new, volume_new = price_volume_from_raw(filename_new, time_new, price_new, volume_new, semi=1,
                                                                unix=0)
    price_new3 = remove_nan(price_new)
    price_new3 = supp.fill_blanks(price_new3)
    volume_new3 = remove_nan(volume_new)

    time_new = time_new_saved  # Saved from Bitstamp

    print("Length of old series: ")
    print("  time old:", len(time_old))
    print("  price old1:", len(price_old1))
    print("  price old2:", len(price_old2))

    print("Length of new series: ")
    print("  time new: ", len(time_new))
    print("  price new1:", len(price_new1))
    print("  price new2:", len(price_new2))
    print("  price new3:", len(price_new3))

    time_list = time_old
    for i in range(0, len(time_new)):
        time_list.append(time_new[i])

    print("Her 3")
    print("Time list:", len(time_list))

    prices = np.zeros([n_exc, len(time_list)])
    volumes = np.zeros([n_exc, len(time_list)])

    for i in range(0, len(price_old1)):
        prices[0, i] = price_old1[i]
        volumes[0, i] = volume_old1[i]
        prices[1, i] = price_old2[i]
        volumes[1, i] = volume_old2[i]
        try:
            prices[2, i] = price_old3[i]
            volumes[2, i] = volume_old3[i]
        except IndexError:
            pass

    k = 0  # Counts the entries in the new lists
    for i in range(len(price_old1), len(time_list)):
        try:
            prices[0, i] = price_new1[k]
        except IndexError:
            print("Error when i =", i, " k =", k)
            try:
                print(price_new1[k])
            except IndexError:
                print("Price new!!!")
        volumes[0, i] = volume_new1[k]
        prices[1, i] = price_new2[k]
        volumes[1, i] = volume_new2[k]
        try:
            prices[2, i] = price_new3[k]
            volumes[2, i] = volume_new3[k]
        except IndexError:
            pass
        k += 1

    with open(filename_old, 'w', newline='') as csvfile:
        writ = csv.writer(csvfile, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        print("\033[0;32;0m Writing to file '%s'...\033[0;0;0m" % filename_old)

        header1 = [" "]
        header2 = [" "]
        header3 = ["Time"]
        for exc in exchanges:
            currency = exc[len(exc) - 3: len(exc)]
            header1.append(exc)
            header1.append("")
            header2.append("Closing price")
            header2.append("Volume")
            header3.append(currency.upper())
            header3.append("BTC")

        writ.writerow(header1)
        writ.writerow(header2)
        writ.writerow(header3)

        for i in range(0, len(time_list)):
            rowdata = [time_list[i]]
            for j in range(0, n_exc):
                rowdata.append(prices[j, i])
                rowdata.append(volumes[j, i])
            writ.writerow(rowdata)


def make_time_stamps():
    print("Generating time stamps...")
    short = 0  # <-------------- For å teste modell bare
    if short == 1:
        start_stamp_excel = "01.04.2017 00:00"  # <-- Må matche startdate
        end_stamp_excel = "31.05.2017 23:59"  # <-- Må matche startdate
        start_stamp_unix = 1491004800  # <-- Må matche startdate
        end_stamp_unix = 1496275140  # <-- Må matche enddate
    else:
        start_stamp_excel = "01.01.2012 00:00"  # <-- Må matche startdate
        end_stamp_excel = "31.05.2017 23:59"  # <-- Må matche startdate
        start_stamp_unix = 1325376000  # <-- Må matche startdate
        end_stamp_unix = 1496275140  # <-- Må matche enddate

    unix_stamps = list(range(start_stamp_unix, end_stamp_unix + 60, 60))
    n_stamps_unix = len(unix_stamps)
    excel_stamps = [start_stamp_excel]
    i = 1
    print(" Progress:")
    print("  0.0%%")
    tenperc = n_stamps_unix / 10
    while excel_stamps[i - 1] != end_stamp_excel:
        d = int(excel_stamps[i - 1][0:2])
        mo = int(excel_stamps[i - 1][3:5])
        y = int(excel_stamps[i - 1][6:10])
        h = int(excel_stamps[i - 1][11:13])
        mi = int(excel_stamps[i - 1][14:16])

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

        if i % tenperc == 0:
            perc = 100 * i / n_stamps_unix
            print("  %0.1f%%" % perc)

        excel_stamps.append(make_single_excel_stamp(y, mo, d, h, mi))
        i = i + 1

    return unix_stamps, excel_stamps