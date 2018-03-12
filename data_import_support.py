import csv
import plot
import realized_volatility
from Sondre import sondre_support_formulas as supp
import numpy as np
from datetime import date
import math
import time
from matplotlib import pyplot as plt
import scipy.stats as st
import rolls
import ILLIQ
from Jacob import jacob_support as jake_supp
from Sondre.sondre_support_formulas import count_rows


def fuse_files(exchanges):
    n_exc = len(exchanges)
    time_old = []
    price_old1 = []
    volume_old1 = []
    price_old2 = []
    volume_old2 = []

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

    print("Her 1")
    print("Time old", len(time_old))
    print("Price old1", len(price_old1))

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

    print("Her 2")
    print("time old:", len(time_old))
    print("price old1:", len(price_old1))
    print("price old2:", len(price_old2))
    print("time new2: ", len(time_new))
    print("price new1:", len(price_new1))
    print("price new2:", len(price_new2))

    time_list = time_old
    for i in range(0, len(time_new)):
        time_list.append(time_new[i])

    print("Her 3")
    print("Time list:", len(time_list))

    prices = np.zeros([2, len(time_list)])
    volumes = np.zeros([2, len(time_list)])

    for i in range(0, len(price_old1)):
        prices[0, i] = price_old1[i]
        volumes[0, i] = volume_old1[i]
        prices[1, i] = price_old2[i]
        volumes[1, i] = volume_old2[i]

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

        excel_stamps.append(make_excel_stamp(y, mo, d, h, mi))
        i = i + 1

    return unix_stamps, excel_stamps


def price_volume_from_raw(file_name, time_list, price, volume, semi=0, unix=1):
    with open(file_name, newline='') as csvfile:
        if semi == 0:
            reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        else:
            reader = csv.reader(csvfile, delimiter=';', quotechar='|')
        print("\033[0;32;0m Reading file '%s'...\033[0;0;0m" % file_name)
        i = 0
        next(reader)
        for row in reader:
            try:
                if unix == 1:
                    time_list.append(int(row[0]))
                else:
                    time_list.append(str(row[0]))
                price.append(float(row[4]))
                volume.append(float(row[5]))
            except ValueError:
                print("\033[0;31;0m There was an error on row %i in '%s'\033[0;0;0m" % (i + 1, file_name))
            i = i + 1
        return time_list, price, volume


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


def make_excel_stamp(y, mo, d, h, mi):
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


def get_price_volume_from_fulls(exchanges):
    n_exc = len(exchanges)
    print("Number of exchanges: ", n_exc)
    raw_folder = "data/long_raw_data/"
    unix_stamps, excel_stamps = make_time_stamps()
    n_cols = len(excel_stamps)
    prices = np.zeros([n_exc, n_cols])
    volumes = np.zeros([n_exc, n_cols])
    for i in range(0, n_exc):
        print("Working on exchange %i/%i" % ((i + 1), n_exc))
        single_price = []
        single_volume = []
        time_list = []
        file_name = raw_folder + exchanges[i] + ".csv"
        time_list, single_price, single_volume = price_volume_from_raw(file_name, time_list, single_price,
                                                                       single_volume, semi=0)

        # Gjør om nan til 0 og så fyller inn tomme priser
        single_price = remove_nan(single_price)
        single_price = supp.fill_blanks(single_price)
        single_volume = remove_nan(single_volume)

        # Må nå finne hvilken rad vi skal lime inn på
        n = len(single_price)
        r = 0

        # Check whether the first entry in time_list is before the start of the unix_stamps
        start_j = 0
        while time_list[start_j] < unix_stamps[0]:
            start_j += 1

        for j in range(start_j, n):
            while unix_stamps[r] != time_list[j]:
                r = r + 1
            prices[i, r] = single_price[j]
            volumes[i, r] = single_volume[j]

    for i in range(n_exc):
        single = supp.fill_blanks(prices[i, :])
        for j in range(0, len(single)):
            prices[i, j] = single[j]

    return excel_stamps, unix_stamps, prices, volumes


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

        # Check whether the first entry in time_list is before the start of the unix_stamps
        start_j = 0
        while time_list[start_j] < unix_stamps[0]:
            start_j += 1

        for j in range(start_j, n):
            while unix_stamps[r] != time_list[j]:
                r = r + 1
            high[i, r] = single_high[j]
            low[i, r] = single_low[j]

    return excel_stamps, unix_stamps, high, low


def write_full_lists_to_csv(volumes, prices, excel_stamps, exchanges, filename):
    time_list = excel_stamps  # <-- Kun for å kunne bruke gammel syntax
    n_exc = len(exchanges)
    print()
    print("Exporting data to csv-files...")
    with open(filename, 'w', newline='') as csvfile:
        writ = csv.writer(csvfile, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        n_rows = np.size(volumes, 1)

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
        for i in range(0, n_rows):
            rowdata = [time_list[i]]
            for j in range(0, n_exc):
                rowdata.append(prices[j, i])
                rowdata.append(volumes[j, i])
            writ.writerow(rowdata)
    print("Export to aggregate csv \033[33;0;0m'%s'\033[0;0;0m successful" % filename)


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


def remove_nan(in_list):
    out_list = in_list
    n = len(in_list)
    count_nans = 0
    for i in range(0, n):
        if in_list[i] != in_list[i]:
            out_list[i] = 0
    return out_list


def write_to_total_files(total_volume, total_price, excel_stamps, filename):
    n_rows = len(excel_stamps)
    with open(filename, 'w', newline='') as csvfile:
        writ = csv.writer(csvfile, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)

        header1 = [" "]
        header2 = [" "]
        header3 = ["Time"]
        header1.append("Total")
        header1.append("")
        header2.append("Price")
        header2.append("Volume")
        header3.append("USD")
        header3.append("BTC")

        writ.writerow(header1)
        writ.writerow(header2)
        writ.writerow(header3)

        for i in range(0, n_rows):
            rowdata = [" "]
            rowdata[0] = excel_stamps[i]
            rowdata.append(total_price[i])
            rowdata.append(total_volume[i])
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


def opening_hours(in_excel_stamps, in_matrix1, in_matrix2):
    year, month, day, hour, minute = supp.fix_time_list(in_excel_stamps)
    n_mins = len(in_excel_stamps)
    out_excel_stamps = []
    out_matrix1 = []
    out_matrix2 = []

    # Kan sette inn en funksjon som sjekker om det er helligdag

    for i in range(n_mins):
        w_day = int(date(year[i], month[i], day[i]).isoweekday())
        if w_day != 6 and w_day != 7:
            if 15 <= hour[i] <= 20 or (hour[i] == 14 and minute[i] >= 30):
                out_excel_stamps.append(in_excel_stamps[i])
                out_matrix1.append(in_matrix1[:, i])
                out_matrix2.append(in_matrix2[:, i])
    out_matrix1 = np.transpose(np.matrix(out_matrix1))
    out_matrix2 = np.transpose(np.matrix(out_matrix2))
    return out_excel_stamps, out_matrix1, out_matrix2


# Denne er kun et eksperiment
def opening_hours_w_weekends(in_excel_stamps, in_prices, in_volumes):
    year, month, day, hour, minute = supp.fix_time_list(in_excel_stamps)
    n_mins = len(in_excel_stamps)
    out_excel_stamps = []
    out_prices = []
    out_volumes = []

    # Kan sette inn en funksjon som sjekker om det er helligdag

    for i in range(n_mins):
        w_day = int(date(year[i], month[i], day[i]).isoweekday())
        if 15 <= hour[i] <= 20 or (hour[i] == 14 and minute[i] >= 30):
            out_excel_stamps.append(in_excel_stamps[i])
            out_prices.append(in_prices[:, i])
            out_volumes.append(in_volumes[:, i])
    out_prices = np.transpose(np.matrix(out_prices))
    out_volumes = np.transpose(np.matrix(out_volumes))
    return out_excel_stamps, out_prices, out_volumes


def convert_to_hour(time_stamps, prices, volumes, ):
    print(" \033[32;0;0mConverting to hourly data...\033[0;0;0m")
    year, month, day, hour, minute = supp.fix_time_list(time_stamps)
    n_mins = len(time_stamps)

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
            for t in range(60, n_mins, 60):
                volumes_out[exc, k] = sum(volumes[exc, t - 60:t])
                prices_out[exc, k] = prices[exc, t]
                time_stamps_out.append(time_stamps[t])
                k += 1
    else:
        volumes_out = []
        prices_out = []
        for t in range(0, n_mins, 60):
            volumes_out.append(sum(volumes[t:t+60]))
            time_stamps_out.append(time_stamps[t])
            prices_out.append(prices[t+59])

    return time_stamps_out, prices_out, volumes_out


def convert_to_day(time_stamps, prices, volumes):
    print(" \033[32;0;0mConverting to daily data...\033[0;0;0m")
    year, month, day, hour, minute = supp.fix_time_list(time_stamps)
    n_mins = len(time_stamps)

    try:
        np.size(prices, 1)
        n_exc = np.size(prices, 0)
    except IndexError:
        n_exc = 1

    start_minute = hour[0] * 60 + minute[0]
    minutes_first_day = 1440 - start_minute

    n_days = int((n_mins) / 1440)  #THIS IS A POSSIBLE BUG WITHOUT +1

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
            for t in range(minutes_first_day, min(n_mins, n_mins-start_minute), 1440):
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

        for t in range(minutes_first_day, min(n_mins, n_mins-start_minute), 1440):
            volumes_out.append(sum(volumes[t:t+1440]))
            prices_out.append(prices[t+1439])
            time_stamps_out.append(time_stamps[t])

    return time_stamps_out, prices_out, volumes_out


def read_raw_gold(file_name, date, time_NYC, volume, price, bid, ask):
    with open(file_name, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        print("\033[0;32;0m Reading file '%s'...\033[0;0;0m" % file_name)
        i = 0
        next(reader)
        for row in reader:
            date.append(str(row[1]))
            time_NYC.append(str(row[2]))
            try:
                volume.append(float(row[9]))
                price.append(float(row[10]))
            except ValueError:
                volume.append(0)
                price.append(0)
            bid.append(float(row[13]))
            ask.append(float(row[18]))
            i = i + 1
    return date, time_NYC, volume, price, bid, ask


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


def clean_trans_days(time_list_minutes, prices_minutes, volumes_minutes, exc=0, print_days_excluded=0,
                     convert_time_zones=1):
    prices_minutes = prices_minutes[exc, :]
    volumes_minutes = volumes_minutes[exc, :]

    if convert_time_zones:
        if exc == 0:
            n_hours = 0
        elif exc == 1:
            n_hours = 9
        else:
            n_hours = 0
    else:
        n_hours = 0

    print("Transforming data series...")

    year, month, day, hour, minute = supp.fix_time_list(time_list_minutes, move_n_hours=n_hours)
    if n_hours != 0:
        time_list_minutes = supp.make_time_list(year, month, day, hour, minute)

    time_list_days, prices_days, volumes_days = convert_to_day(time_list_minutes, prices_minutes, volumes_minutes)

    if exc == 0:
        #cutoff_hour = 8784  # 2012
        cutoff_date = "01.01.2013 00:00"
        cutoff_min_date = cutoff_date
        start_averaging_date = "01.01.2012 00:00"
    elif exc == 1:
        # cutoff_hour = 35064  # 2012-2015
        #cutoff_hour = 26304  # 2012-2014
        cutoff_date = "01.01.2016 00:00"
        cutoff_min_date = "01.01.2016 09:00"
        #start_averaging_date = "30.10.2014 00:00"
        start_averaging_date = "30.10.2014 00:00"
    else:
        print("Choose an exchange!")

    cutoff_day = supp.find_date_index(cutoff_date, time_list_days)
    cutoff_min = supp.find_date_index(cutoff_min_date, time_list_minutes)
    start_averaging_day = supp.find_date_index(start_averaging_date, time_list_days)

    mean_volume_prev_year = np.average(volumes_days[start_averaging_day:cutoff_day])

    n_days = len(time_list_days)
    n_mins = len(time_list_minutes)
    print("Only including days after", time_list_days[cutoff_day])
    print("Only including days after", time_list_minutes[cutoff_min])

    n_total = len(time_list_days)
    n_0 = n_days

    time_list_minutes = time_list_minutes[cutoff_min:n_mins]
    print("Only including days after", time_list_minutes[0], "to", time_list_minutes[len(time_list_minutes)-1])
    prices_minutes = prices_minutes[cutoff_min:n_mins]
    volumes_minutes = volumes_minutes[cutoff_min:n_mins]
    prices_days = prices_days[cutoff_day:n_days]
    volumes_days = volumes_days[cutoff_day:n_days]
    time_list_days = time_list_days[cutoff_day:n_days]

    n_1 = len(time_list_days)  # After removing 2012

    # Rolls
    spread_abs, spread_days, time_list_rolls, count_value_error = rolls.rolls(prices_minutes, time_list_minutes,
                                                                              calc_basis="d", kill_output=1)


    # Realized volatility
    volatility_days, RVol_time = realized_volatility.RVol(time_list_minutes, prices_minutes, daily=1, annualize=1)

    # Returns
    returns_minutes = jake_supp.logreturn(prices_minutes)
    returns_days = jake_supp.logreturn(prices_days)
    # Amihud's ILLIQ
    illiq_time, illiq_days = ILLIQ.illiq(time_list_minutes, returns_minutes, volumes_minutes, threshold=0)  # Already clean

    plot_raw = 0
    if plot_raw == 1:
        plt.plot(volatility_days)
        plt.title("Raw rvol")
        plt.figure()
        plt.plot(spread_days)
        plt.title("Raw spread")
        plt.figure()
        plt.plot(volumes_days)
        plt.title("Raw volume")
        plt.figure()
        plt.plot(illiq_days)
        plt.title("Raw illiq")
        plt.figure()
        plt.plot(returns_days)
        plt.title("Raw returns")
        plt.figure()

    n_2 = len(time_list_days)  # After removing zero-volume
    time_list_removed = []
    # Removing all days where Volume is zero
    time_list_days, time_list_removed, volumes_days, spread_days, returns_days, volatility_days \
        = supp.remove_list1_zeros_from_all_lists(time_list_days, time_list_removed, volumes_days, spread_days,
                                                 returns_days, volatility_days)

    # --------------------------------------------
    days_to_remove = []
    if exc == 0:
        days_to_remove = supp.remove_extremes(days_to_remove, returns_days, 0.1, threshold_lower=-0.1)
        days_to_remove = supp.remove_extremes(days_to_remove, volatility_days, 2)
        days_to_remove = supp.remove_extremes(days_to_remove, spread_days, 0.006)
        days_to_remove = supp.remove_extremes(days_to_remove, illiq_days, 0.003)
    elif exc == 1:
        days_to_remove = supp.remove_extremes(days_to_remove, returns_days, 0.1, threshold_lower=-0.1)
        days_to_remove = supp.remove_extremes(days_to_remove, volatility_days, 2)
        days_to_remove = supp.remove_extremes(days_to_remove, spread_days, 0.003)
        days_to_remove = supp.remove_extremes(days_to_remove, illiq_days, 0.1)
        days_to_remove = supp.remove_extremes(days_to_remove, illiq_days, 0.002)

    for d in days_to_remove:
        time_list_removed = np.append(time_list_removed, time_list_days[d])
    time_list_days = np.delete(time_list_days, days_to_remove)
    returns_days = np.delete(returns_days, days_to_remove)
    volumes_days = np.delete(volumes_days, days_to_remove)
    spread_days = np.delete(spread_days, days_to_remove)
    volatility_days = np.delete(volatility_days, days_to_remove)
    illiq_days = np.delete(illiq_days, days_to_remove)
    illiq_time = np.delete(illiq_time, days_to_remove)

    plot_after_removal = 0
    if plot_after_removal == 1:
        plt.plot(volatility_days)
        plt.title("rvol")
        plt.figure()
        plt.plot(spread_days)
        plt.title("spread")
        plt.figure()
        plt.plot(volumes_days)
        plt.title("volume")
        plt.figure()
        plt.plot(illiq_days)
        plt.title("illiq")
        plt.figure()
        plt.plot(returns_days)
        plt.title("returns")
        plt.show()

    n_3 = len(time_list_days)  # After removing the extremes

    # Removing all days where Roll is zero
    time_list_days_clean, time_list_removed, spread_days_clean, volumes_days_clean, returns_days_clean, \
    volatility_days_clean, illiq_days_clean = supp.remove_list1_zeros_from_all_lists(time_list_days,
                                                                                     time_list_removed,
                                                                                     spread_days,
                                                                                     volumes_days,
                                                                                     returns_days,
                                                                                     volatility_days,
                                                                                     illiq_days)


    n_4 = len(time_list_days_clean)  # After removing the zero-roll

    # Removing all days where Volatility is zero
    time_list_days_clean, time_list_removed, volatility_days_clean, volumes_days_clean, returns_days_clean, \
    spread_days_clean, illiq_days_clean = supp.remove_list1_zeros_from_all_lists(time_list_days_clean,
                                                                                 time_list_removed,
                                                                                 volatility_days_clean,
                                                                                 volumes_days_clean,
                                                                                 returns_days_clean,
                                                                                 spread_days_clean, illiq_days_clean)


    n_5 = len(time_list_days_clean)  # After removing the zero-volatility

    show_days_table = print_days_excluded
    if show_days_table == 1:
        print()
        print()
        print("Total days:", n_total)
        print("Week only:", n_0)
        print("Removing 2012:", n_1)
        print("Removing zero-volume:", n_2)
        print("Removing extreme days:", n_3)
        print("Removing zero-roll:", n_4)
        print("Removing zero-volatility:", n_5)

    # Turning ILLIQ, Volume and RVol into log
    log_illiq_days_clean = np.log(illiq_days_clean)
    log_volatility_days_clean = np.log(volatility_days_clean)
    log_volumes_days_clean = volume_transformation(volumes_days_clean, mean_volume_prev_year)

    return time_list_days_clean, time_list_removed, returns_days_clean, volumes_days_clean, log_volumes_days_clean, spread_days_clean, \
           illiq_days_clean, log_illiq_days_clean, volatility_days_clean, log_volatility_days_clean


def clean_trans_hours(time_list_minutes, prices_minutes, volumes_minutes, exc=0, convert_time_zones=1):

    remove_extremes = 1

    if convert_time_zones:  # Flytter nå Coincheck ni timer, men lar Bitstamp stå
        if exc == 0:
            n_hours = 0
        elif exc == 1:
            n_hours = 9
            print("Converting time zones: moving series %i hours" % n_hours)
        else:
            n_hours = 0
    else:
        n_hours = 0

    year, month, day, hour, minute = supp.fix_time_list(time_list_minutes, move_n_hours=n_hours) # Flytter nå Coincheck ni timer, men lar Bitstamp stå
    if n_hours != 0:
        time_list_minutes = supp.make_time_list(year, month, day, hour, minute)  # Lager en ny tidsliste fra de flyttede listene

    prices_minutes = prices_minutes[exc, :]
    volumes_minutes = volumes_minutes[exc, :]
    returns_minutes = jake_supp.logreturn(prices_minutes)

    time_list_hours, prices_hours, volumes_hours = convert_to_hour(time_list_minutes, prices_minutes, volumes_minutes)
    returns_hours = jake_supp.logreturn(prices_hours)

    spread_abs, spread_hours, time_list_spread, count_value_error = rolls.rolls(prices_minutes, time_list_minutes, calc_basis="h", kill_output=1)
    illiq_hours_time, illiq_hours = ILLIQ.illiq(time_list_minutes, returns_minutes, volumes_minutes, hourly_or_daily="h", threshold=0)
    rvol_hours, time_list_rvol = realized_volatility.RVol(time_list_minutes, prices_minutes, daily=0, annualize=1)

    n_0 = len(time_list_hours) # initial number of hours

    time_list_removed = []
    # Removing all hours where Volume is zero
    time_list_hours, time_list_removed, volumes_hours, spread_hours, returns_hours, rvol_hours \
        = supp.remove_list1_zeros_from_all_lists(time_list_hours, time_list_removed, volumes_hours, spread_hours,
                                                 returns_hours, rvol_hours)

    n_1 = len(time_list_hours)  # After removing the zero-volume

    if exc == 0:
        #cutoff_hour = 8784  # 2012
        cutoff_date = "01.01.2013 00:00"
        start_averaging_date = "01.01.2012 00:00"
    elif exc == 1:
        # cutoff_hour = 35064  # 2012-2015
        #cutoff_hour = 26304  # 2012-2014
        cutoff_date = "01.01.2017 00:00"
        start_averaging_date = "30.10.2014 00:00"
    else:
        print("Choose an exchange!")

    cutoff_hour = supp.find_date_index(cutoff_date, time_list_hours)
    start_averaging_hour = supp.find_date_index(start_averaging_date, time_list_hours)

    mean_volume_prev_year = np.average(volumes_hours[start_averaging_hour:cutoff_hour])

    total_hours = len(time_list_hours) - 1
    time_list_hours = time_list_hours[cutoff_hour:total_hours]
    returns_hours = returns_hours[cutoff_hour:total_hours]
    volumes_hours = volumes_hours[cutoff_hour:total_hours]
    spread_hours = spread_hours[cutoff_hour:total_hours]
    illiq_hours = illiq_hours[cutoff_hour:len(illiq_hours) - 1]
    rvol_hours = rvol_hours[cutoff_hour:total_hours]

    plot_raw = 1
    if plot_raw == 1:
        #lt.plot(rvol_hours)
        #plt.title("Raw rvol")
        #plt.figure()
        plt.plot(spread_hours)
        plt.title("Raw spread")
        plt.figure()
        plt.plot(volumes_hours)
        plt.title("Raw volume")
        plt.figure()
        plt.plot(illiq_hours)
        plt.title("Raw illiq")
        plt.figure()
        #plt.plot(returns_hours)
        #plt.title("Raw returns")
        #plt.figure()

    n_1 = len(time_list_hours)

    hours_to_remove = []

    if remove_extremes == 1:
        if exc == 0:
            hours_to_remove = supp.remove_extremes(hours_to_remove, returns_hours, 0.1, threshold_lower=-0.1)
            hours_to_remove = supp.remove_extremes(hours_to_remove, rvol_hours, 2)
            hours_to_remove = supp.remove_extremes(hours_to_remove, spread_hours, 0.02)
            hours_to_remove = supp.remove_extremes(hours_to_remove, illiq_hours, 0.01)
        elif exc == 1:
            hours_to_remove = supp.remove_extremes(hours_to_remove, returns_hours, 0.075, threshold_lower=-0.075)
            hours_to_remove = supp.remove_extremes(hours_to_remove, rvol_hours, 2)
            hours_to_remove = supp.remove_extremes(hours_to_remove, spread_hours, 0.05)
            hours_to_remove = supp.remove_extremes(hours_to_remove, illiq_hours, 0.01)

    time_list_hours = np.delete(time_list_hours, hours_to_remove)
    returns_hours = np.delete(returns_hours, hours_to_remove)
    volumes_hours = np.delete(volumes_hours, hours_to_remove)
    spread_hours = np.delete(spread_hours, hours_to_remove)
    illiq_hours = np.delete(illiq_hours, hours_to_remove)
    rvol_hours = np.delete(rvol_hours, hours_to_remove)

    plot_after_removal = 1
    if plot_after_removal == 1:
        #plt.plot(rvol_hours)
        #plt.title("rvol")
        #plt.figure()
        plt.plot(spread_hours)
        plt.title("spread")
        plt.figure()
        plt.plot(volumes_hours)
        plt.title("volume")
        plt.figure()
        plt.plot(illiq_hours)
        plt.title("illiq")
        #plt.figure()
        #plt.plot(returns_hours)
        #plt.title("returns")



    # Removing all days where Roll is zero
    time_list_hours, time_list_removed, spread_hours, volumes_hours, returns_hours, \
    illiq_hours, rvol_hours = supp.remove_list1_zeros_from_all_lists(time_list_hours,
                                                                     time_list_removed,
                                                                     spread_hours,
                                                                     volumes_hours,
                                                                     returns_hours,
                                                                     illiq_hours, rvol_hours)


    n_4 = len(time_list_hours)  # After removing the zero-roll

    # Removing all hours where Rvol is zero
    time_list_hours, time_list_removed, rvol_hours, spread_hours, volumes_hours, returns_hours, \
    illiq_hours = supp.remove_list1_zeros_from_all_lists(time_list_hours,
                                                         time_list_removed,
                                                         rvol_hours,
                                                         spread_hours,
                                                         volumes_hours,
                                                         returns_hours,
                                                         illiq_hours)


    n_5 = len(time_list_hours)  # After removing the zero-volatility


    illiq_hours_time = time_list_hours

    illiq_hours_time, time_list_removed, illiq_hours = supp.remove_list1_zeros_from_all_lists(
        time_list_hours,
        time_list_removed,
        illiq_hours)

    show_hours_table = 0
    if show_hours_table == 1:
        print()
        print()
        print("Total:", n_0)
        print("Removing beginning:", n_1)
        print("Removing crazy :", n_2)
        print("Removing zero-volume:", n_3)
        print("Removing zero-roll:", n_4)
        print("Removing zero-vol:", n_5)

    # Turning ILLIQ, Volume and rvol into log
    log_illiq_hours = np.log(illiq_hours)
    log_volumes_hours = volume_transformation(volumes_hours, mean_volume_prev_year)
    log_rvol_hours = np.log(rvol_hours)

    if plot_raw + plot_after_removal > 0:
        plt.show()

    return time_list_hours, returns_hours, spread_hours, log_volumes_hours, illiq_hours, illiq_hours_time, log_illiq_hours, rvol_hours, log_rvol_hours


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
        return time_list, price, volume


def write_to_raw_file(volumes, prices, time_list, exchanges, filename):
    n_exc = len(exchanges)
    print("Exporting data to csv-file...")
    with open(filename, 'w', newline='') as csvfile:
        writ = csv.writer(csvfile, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        n_rows = np.size(volumes, 1)

        header1 = [" "]
        header2 = [" "]
        header3 = ["Time"]
        for exc in exchanges:
            currency = exc[len(exc) - 3: len(exc)]
            header1.append(exc)
            header1.append("")
            header2.append("Price")
            header2.append("Volume")
            header3.append(currency.upper())
            header3.append("BTC")

        writ.writerow(header1)
        writ.writerow(header2)
        writ.writerow(header3)
        for i in range(0, n_rows):
            rowdata = [time_list[i]]
            for j in range(0, n_exc):
                rowdata.append(prices[j, i])
                rowdata.append(volumes[j, i])
            writ.writerow(rowdata)
    print("Export to aggregate csv \033[33;0;0m'%s'\033[0;0;0m successful" % filename)


def fetch_aggregate_csv(file_name, n_exc):
    n_rows = count_rows(file_name)
    n_exc = int(n_exc)
    print("\033[0;32;0m Reading file '%s'...\033[0;0;0m" % file_name)
    with open(file_name, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=';', quotechar='|')
        i = 0
        time_list = []
        prices = np.zeros([n_exc, n_rows - 3])  # minus tre for å ikke få med headere
        volumes = np.zeros([n_exc, n_rows - 3])  # minus tre for å ikke få med headere
        next(reader)
        next(reader)
        next(reader)
        for row in reader:
            time_list.append(row[0])
            for j in range(0, n_exc):
                prices[j, i] = row[1 + 2 * j]
                volumes[j, i] = row[2 + 2 * j]
            i = i + 1
    return time_list, prices, volumes