import csv

import realized_volatility
from Sondre import sondre_support_formulas as supp
import numpy as np
from datetime import date
import math
from matplotlib import pyplot as plt
import scipy.stats as st
import rolls
import ILLIQ
from Jacob import jacob_support as jake_supp


def fuse_files():
    time_new = []
    price_new = []
    volume_new = []

    location = "data/bitcoincharts/"
    exchange = "bitstampusd"
    exchanges = [exchange]
    year = "2017"
    for month in ["06", "07", "08", "09", "10", "11", "12"]: # iterate through the new files
        filename_new = location + exchange + "/" + year + month + ".csv"
        time_new, price_new, volume_new = price_volume_from_raw(filename_new, time_new, price_new, volume_new, semi=1, unix=0)

    price_new = remove_nan(price_new)
    price_new = supp.fill_blanks(price_new)
    volume_new = remove_nan(volume_new)

    for i in range(0, len(price_new), 1440):
        print(time_new[i], price_new[i])

    time_old = []
    price_old = []
    volume_old = []

    filename_old = "data/export_csv/minute_data_full_day.csv"
    with open(filename_old, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=';', quotechar='|')
        print("\033[0;32;0m Reading file '%s'...\033[0;0;0m" % filename_old)
        next(reader)
        next(reader)
        next(reader)
        for row in reader:
            time_old.append(str(row[0]))
            price_old.append(float(row[1]))
            volume_old.append(float(row[2]))

    time_list = time_old
    price = price_old
    volume = volume_old

    for i in range(0, len(time_new)):
        time_list.append(time_new[i])
        price.append(price_new[i])
        volume.append(volume_new[i])

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
            rowdata.append(price[i])
            rowdata.append(volume[i])
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
                1
                #print("\033[0;31;0m There was an error on row %i in '%s'\033[0;0;0m" % (i + 1, file_name))
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
        time_list, single_price, single_volume = price_volume_from_raw(file_name, time_list, single_price, single_volume, semi=0)

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


def convert_to_hour(time_stamps, list1, list2, list1_basis=0, list2_basis=1):
    # basis=0 --> start/end     basis=1 --> sum
    print(" \033[32;0;0mConverting to hourly data...\033[0;0;0m")
    year, month, day, hour, minute = supp.fix_time_list(time_stamps)
    n_mins = len(time_stamps)
    time_stamps_out = []
    k = 0

    n_exc = np.size(list1, 0)

    if hour[0] == 0:
        opening_hours_only = 0
    else:
        opening_hours_only = 1
        print("  Opening hours only")

    if opening_hours_only == 1:
        n_hours = int(math.ceil(n_mins * (7 / 390)))
        matrix1_out = np.zeros([n_exc, n_hours])
        matrix2_out = np.zeros([n_exc, n_hours])
        for i in range(n_mins - 59):
            if hour[i] == 14 and minute[i] == 30:
                time_stamps_out.append(time_stamps[i])
                for j in range(n_exc):
                    if list1_basis == 0:
                        matrix1_out[j, k] = list1[j, i + 29]  # The price at the last minute of the hour
                    else:
                        matrix1_out[j, k] = np.sum(list1[j, i:(i + 30)]) * 2  # The price at the last minute of the hour
                    if list2_basis == 0:
                        matrix2_out[j, k] = list2[j, i + 29]    # To make up for missing half hour
                    else:
                        matrix2_out[j, k] = np.sum(list2[j, i:(i + 30)]) * 2  # To make up for missing half hour
                k += 1
            elif minute[i] == 0:
                time_stamps_out.append(time_stamps[i])
                for j in range(n_exc):
                    if list1_basis == 0:
                        matrix1_out[j, k] = list1[j, i + 59]  # The price at the last minute of the hour
                    else:
                        matrix1_out[j, k] = np.sum(list1[j, i:(i + 60)])
                    if list2_basis == 0:
                        matrix2_out[j, k] = list2[j, i + 59]  # The price at the last minute of the hour
                    else:
                        matrix2_out[j, k] = np.sum(list2[j, i:(i + 60)])
                k += 1
    else:
        n_hours = int(n_mins / 60)
        matrix1_out = np.zeros([n_exc, n_hours])
        matrix2_out = np.zeros([n_exc, n_hours])
        for i in range(n_mins - 59):
            if minute[i] == 0:
                time_stamps_out.append(time_stamps[i])
                for j in range(n_exc):
                    if list1_basis == 0:
                        matrix1_out[j, k] = list1[j, i + 59]  # The price at the last minute of the hour
                    else:
                        matrix1_out[j, k] = np.sum(list1[j, i:(i + 60)])
                    if list2_basis == 0:
                        matrix2_out[j, k] = list2[j, i + 59]  # The price at the last minute of the hour
                    else:
                        matrix2_out[j, k] = np.sum(list2[j, i:(i + 60)])
                k += 1
    return time_stamps_out, matrix1_out, matrix2_out


def convert_to_day(time_stamps, prices, volumes):
    print(" \033[32;0;0mConverting to daily data...\033[0;0;0m")
    year, month, day, hour, minute = supp.fix_time_list(time_stamps)
    n_mins = len(time_stamps)
    time_stamps_out = []
    k = 0
    n_exc = np.size(prices, 0)

    if hour[0] == 0:
        opening_hours_only = 0
    else:
        opening_hours_only = 1

    if opening_hours_only == 1:
        n_days = int(math.ceil(n_mins / 390))
        prices_out = np.zeros([n_exc, n_days])
        volumes_out = np.zeros([n_exc, n_days])
        for i in range(n_mins - 59):
            if hour[i] == 14 and minute[i] == 30:
                time_stamps_out.append(time_stamps[i])
                for j in range(n_exc):
                    prices_out[j, k] = prices[j, i + 389]  # The price at the last minute of the hour
                    volumes_out[j, k] = np.sum(volumes[j, i:(i + 390)])
                k += 1
    else:
        n_days = int(n_mins / 1440)
        prices_out = np.zeros([n_exc, n_days])
        volumes_out = np.zeros([n_exc, n_days])
        for i in range(n_mins - 59):
            if hour[i] == 0 and minute[i] == 0:
                time_stamps_out.append(time_stamps[i])
                for j in range(n_exc):
                    prices_out[j, k] = prices[j, i + 1439]  # The price at the last minute of the hour
                    volumes_out[j, k] = np.sum(volumes[j, i:(i + 1440)])
                k += 1
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


def cyclical_average(time_list, data, frequency="h"):
    year, month, day, hour, minute = supp.fix_time_list(time_list)
    n_entries = len(time_list)
    day_time = []  # Excel stamps for each minute in the day
    h_list = []  # integer indicating which hour it is
    m_list = []  # integer indicating which minute it is

    # Generating day_time ---------------
    if frequency == "h":
        if hour[0] == 14:
            for h in range(14, 21):
                if h < 10:
                    hs = "0" + str(h)
                else:
                    hs = str(h)
                day_time.append(hs + ":" + "00")
                h_list.append(h)
        else:
            for h in range(0, 24):
                if h < 10:
                    hs = "0" + str(h)
                else:
                    hs = str(h)
                day_time.append(hs + ":" + "00")
                h_list.append(h)
    elif frequency == "m":
        if hour[0] == 14:
            for h in range(14, 21):
                if h < 10:
                    hs = "0" + str(h)
                else:
                    hs = str(h)
                if h == 14:
                    mins_in_hour = 30
                else:
                    mins_in_hour = 60
                for m in range(0, mins_in_hour):
                    if m < 10:
                        ms = "0" + str(m)
                    else:
                        ms = str(m)
                    day_time.append(hs + ":" + ms)
                    h_list.append(h)
                    m_list.append(m)
        else:
            for h in range(0, 24):
                if h < 10:
                    hs = "0" + str(h)
                else:
                    hs = str(h)
                for m in range(0, 60):
                    if m < 10:
                        ms = "0" + str(m)
                    else:
                        ms = str(m)
                    day_time.append(hs + ":" + ms)
                    h_list.append(h)
                    m_list.append(m)
    elif frequency == "d":
        if hour[0] == 0:
            day_time = ["Mon", "Tue", "Wed", "Thur", "Fri", "Sat", "Sun"]
        else:
            day_time = ["Mon", "Tue", "Wed", "Thur", "Fri"]
    else:
        print("di.average_over_day: Something was wrong with the time_list....")
        return None
    # -----------------------------------

    # Calculating averages
    n_out = len(day_time)
    lower = np.zeros(n_out)
    upper = np.zeros(n_out)
    out_data = np.zeros(n_out)
    temp_list = np.zeros(n_out)
    temp_matrix = []
    k = -1
    if frequency == "h":
        for i in range(n_entries):
            index = hour[i] - hour[0]  # Hvis dagen starter på 14:30 vil vi også at indexen skal starte der
            if index == 0:
                temp_list[index] = data[i]
                temp_matrix.append(temp_list)
                k += 1
                temp_list = np.zeros(n_out)
            else:
                temp_list[index] = data[i]
    elif frequency == "m":
        for i in range(n_entries):
            index = (hour[i] - hour[0]) * 60 + minute[i] - minute[0]  # Hvis dagen starter på 14:30 vil vi også...
            if index == 0:
                try:
                    temp_list[index] = data[i]
                except ValueError:
                    print("Error on index = %i and i = %i" % (index, i))
                    print("Data: ", data[i])
                    print("templist: ", temp_list[index])
                    return
                temp_matrix.append(temp_list)
                k += 1
                temp_list = np.zeros(n_out)
            else:
                temp_list[index] = data[i]
    elif frequency == "d":
        for i in range(n_entries):
            index = int(date(year[i], month[i], day[i]).isoweekday()) - 1
            if index == 0:
                temp_list[index] = data[i]
                temp_matrix.append(temp_list)
                k += 1
                temp_list = np.zeros(n_out)
            else:
                temp_list[index] = data[i]

    temp_matrix = np.matrix(temp_matrix)

    percentile = 0.95
    for i in range(n_out):
        out_data[i] = np.mean(temp_matrix[:, i])
        lower[i], upper[i] = st.t.interval(percentile, len(temp_matrix[:, i]) - 1, loc=np.mean(temp_matrix[:, i]),
                                           scale=st.sem(temp_matrix[:, i]))

    return day_time, out_data, lower, upper


def volume_transformation(volume, initial_mean_volume):
    n_entries = len(volume)
    n_days_in_window = 365
    out_volume = np.zeros(n_entries)
    for i in range(0, n_days_in_window):
        floating_mean = (initial_mean_volume * (n_days_in_window - i) + i * np.mean(volume[0: i])) / n_days_in_window
        out_volume[i] = np.log(volume[i]) - np.log(floating_mean)
    for i in range(n_days_in_window, n_entries):
        if volume[i] == 0 or np.mean(volume[i - n_days_in_window:i]) == 0:
            out_volume[i] = 0
        else:
            out_volume[i] = np.log(volume[i]) - np.log(np.mean(volume[i - n_days_in_window:i - 1]))
    out_volume[0] = np.log(volume[0]) - np.log(initial_mean_volume)
    return out_volume


def clean_trans_2013(time_list_minutes, prices_minutes, volumes_minutes, full_week=1, exchange=0, days_excluded=0):

    # Opening hours only
    print("Transforming data series...")
    time_list_hours, prices_hours, volumes_hours = convert_to_hour(time_list_minutes, prices_minutes,
                                                                   volumes_minutes)
    time_list_days, prices_days, volumes_days = convert_to_day(time_list_minutes, prices_minutes, volumes_minutes)

    if full_week == 0:
        cutoff_day = 261
        cutoff_hour = cutoff_day * 7
        cutoff_min = cutoff_day * 390
    else:
        cutoff_day = 366
        cutoff_hour = cutoff_day * 24
        cutoff_min = cutoff_day * 1440

    mean_volume_2012 = np.mean(volumes_days[exchange, 0:cutoff_day])  # <-- Bitstamp
    n_days = len(time_list_days)
    n_hours = len(time_list_hours)
    n_mins = len(time_list_minutes)
    print("Only including days after", time_list_days[cutoff_day])

    n_total = len(time_list_days)
    n_0 = n_days # Mon-Friday

    # Bistamp only, cutoff day # <-- Bitstamp
    prices_minutes = prices_minutes[exchange, cutoff_min:n_mins]
    volumes_minutes = volumes_minutes[exchange, cutoff_min:n_mins]
    time_list_minutes = time_list_minutes[cutoff_min:n_mins]
    prices_hours = prices_hours[exchange, cutoff_hour:n_hours]
    volumes_hours = volumes_hours[exchange, cutoff_hour:n_hours]
    prices_days = prices_days[exchange, cutoff_day:n_days]
    volumes_days = volumes_days[exchange, cutoff_day:n_days]
    time_list_days = time_list_days[cutoff_day:n_days]

    n_1 = len(time_list_days) # After removing 2013

    # Rolls
    spread_abs, spread_days, time_list_rolls, count_value_error = rolls.rolls(prices_minutes, time_list_minutes,
                                                                              calc_basis=1, kill_output=1)

    # Realized volatility
    volatility_days, rVol_time = realized_volatility.daily_Rvol(time_list_minutes, prices_minutes)
    # Annualize the volatility
    if full_week == 0:
        volatility_days = np.multiply(volatility_days, 252 ** 0.5)
    else:
        volatility_days = np.multiply(volatility_days, 365 ** 0.5)
    # Returns
    returns_minutes = jake_supp.logreturn(prices_minutes)
    returns_days = jake_supp.logreturn(prices_days)
    # Amihud's ILLIQ
    illiq_time, illiq_days_clean = ILLIQ.illiq(time_list_minutes, returns_minutes, volumes_minutes) # Already clean

    # --------------------------------------------

    if exchange == 0:
        if full_week == 0:
            cray_s = 69
            cray_e = 74
        else:
            cray_s= 97
            cray_e= 103
        cray_day = 1269
    elif exchange == 1:
        cray_day = 405
        cray_s = 927
        cray_e = 928
    remove_crazy = 1
    remove_crazy_week = 1  # Removes the week starting at 08.04.2013

    if remove_crazy == 1:
        time_list_removed = time_list_days[cray_day]
        time_list_days = np.delete(time_list_days, cray_day)
        returns_days = np.delete(returns_days, cray_day)
        volumes_days = np.delete(volumes_days, cray_day)
        spread_days = np.delete(spread_days, cray_day)
        volatility_days = np.delete(volatility_days, cray_day)
        illiq_days_clean = np.delete(illiq_days_clean, cray_day)
        illiq_time = np.delete(illiq_time, cray_day)
    if remove_crazy_week == 1:
        time_list_removed = np.append(time_list_removed, time_list_days[cray_s:cray_e])
        time_list_days = np.delete(time_list_days, range(cray_s, cray_e))
        returns_days = np.delete(returns_days, range(cray_s, cray_e))
        volumes_days = np.delete(volumes_days, range(cray_s, cray_e))
        spread_days = np.delete(spread_days, range(cray_s, cray_e))
        volatility_days = np.delete(volatility_days, range(cray_s, cray_e))
        illiq_days_clean = np.delete(illiq_days_clean, range(cray_s, cray_e))
        illiq_time = np.delete(illiq_time, range(cray_s, cray_e))

    n_2 = len(time_list_days) # After removing the crazy

    # Removing all days where Volume is zero
    time_list_days_clean, time_list_removed, volumes_days_clean, spread_days_clean, returns_days_clean, volatility_days_clean \
        = supp.remove_list1_zeros_from_all_lists(time_list_days, time_list_removed, volumes_days, spread_days,
                                                 returns_days, volatility_days)

    n_3 = len(time_list_days_clean) # After removing the zero-volume

    # Removing all days where Roll is zero
    time_list_days_clean, time_list_removed, spread_days_clean, volumes_days_clean, returns_days_clean, \
    volatility_days_clean, illiq_days_clean = supp.remove_list1_zeros_from_all_lists(time_list_days_clean,
                                                                                     time_list_removed,
                                                                                     spread_days_clean,
                                                                                     volumes_days_clean,
                                                                                     returns_days_clean,
                                                                                     volatility_days_clean,
                                                                                     illiq_days_clean)

    n_4 = len(time_list_days_clean) # After removing the zero-roll


    # Removing all days where Volatility is zero
    time_list_days_clean, time_list_removed, volatility_days_clean, volumes_days_clean, returns_days_clean, \
    spread_days_clean, illiq_days_clean = supp.remove_list1_zeros_from_all_lists(time_list_days_clean,
                                                                                 time_list_removed,
                                                                                 volatility_days_clean,
                                                                                 volumes_days_clean,
                                                                                 returns_days_clean,
                                                                                 spread_days_clean, illiq_days_clean)

    n_5 = len(time_list_days_clean) # After removing the zero-volatility

    show_days_table = days_excluded
    if show_days_table == 1:
        print()
        print()
        print("Total days:", n_total)
        print("Week only:", n_0)
        print("Removing 2012:", n_1)
        print("Removing extreme week:", n_2)
        print("Removing zero-volume:", n_3)
        print("Removing zero-roll:", n_4)
        print("Removing zero-volatility:", n_5)

    # Turning ILLIQ, Volume and RVol into log
    log_illiq_days_clean = np.log(illiq_days_clean)
    log_volatility_days_clean = np.log(volatility_days_clean)
    log_volumes_days_clean = volume_transformation(volumes_days_clean, mean_volume_2012)

    return time_list_days_clean, time_list_removed, returns_days_clean, volumes_days_clean, log_volumes_days_clean, spread_days_clean, \
           illiq_days_clean, log_illiq_days_clean, volatility_days_clean, log_volatility_days_clean


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