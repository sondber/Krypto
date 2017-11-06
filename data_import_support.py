import csv
from Sondre import sondre_support_formulas as supp
import numpy as np
from datetime import date
import math
from matplotlib import pyplot as plt
import scipy.stats as st


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


def read_long_csvs(file_name, time_list, price, volume):
    with open(file_name, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        print("\033[0;32;0m Reading file '%s'...\033[0;0;0m" % file_name)
        i = 0
        next(reader)
        for row in reader:
            try:
                time_list.append(int(row[0]))
                price.append(float(row[4]))
                volume.append(float(row[5]))
            except ValueError:
                print("\033[0;31;0m There was an error on row %i in '%s'\033[0;0;0m" % (i + 1, file_name))
            i = i + 1
        return time_list, price, volume


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


def get_lists_from_fulls(exchanges):
    n_exc = len(exchanges)
    print("Number of exchanges: ", n_exc)
    raw_folder = "data/long_raw_data/"
    unix_stamps, excel_stamps = make_time_stamps()
    n_cols = len(excel_stamps)
    prices = np.zeros([n_exc, n_cols])
    prices_usd = np.zeros([n_exc, n_cols])
    volumes = np.zeros([n_exc, n_cols])
    for i in range(0, n_exc):
        print("Working on exchange %i/%i" % ((i + 1), n_exc))
        single_price = []
        single_volume = []
        time_list = []
        file_name = raw_folder + exchanges[i] + ".csv"
        time_list, single_price, single_volume = read_long_csvs(file_name, time_list, single_price, single_volume)

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


def opening_hours(in_excel_stamps, in_prices, in_volumes):
    year, month, day, hour, minute = supp.fix_time_list(in_excel_stamps)
    n_mins = len(in_excel_stamps)
    out_excel_stamps = []
    out_prices = []
    out_volumes = []

    # Kan sette inn en funksjon som sjekker om det er helligdag

    for i in range(n_mins):
        w_day = int(date(year[i], month[i], day[i]).isoweekday())
        if w_day != 6 and w_day != 7:
            if 14 <= hour[i] <= 19 or (hour[i] == 13 and minute[i] >= 30):
                out_excel_stamps.append(in_excel_stamps[i])
                out_prices.append(in_prices[:, i])
                out_volumes.append(in_volumes[:, i])
    out_prices = np.transpose(np.matrix(out_prices))
    out_volumes = np.transpose(np.matrix(out_volumes))
    return out_excel_stamps, out_prices, out_volumes


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
        if 14 <= hour[i] <= 19 or (hour[i] == 13 and minute[i] >= 30):
            out_excel_stamps.append(in_excel_stamps[i])
            out_prices.append(in_prices[:, i])
            out_volumes.append(in_volumes[:, i])
    out_prices = np.transpose(np.matrix(out_prices))
    out_volumes = np.transpose(np.matrix(out_volumes))
    return out_excel_stamps, out_prices, out_volumes

"""
def convert_to_lower_freq(time_stamps, prices, volumes, conversion_rate=60):
    n_cols_high = len(time_stamps)
    n_exc = np.size(volumes, 0)
    n_cols_low = int(n_cols_high / conversion_rate)
    time_stamps_low = []
    prices_low = np.zeros([n_exc, n_cols_low])
    volumes_low = np.zeros([n_exc, n_cols_low])
    for i in range(0, n_cols_low):
        time_stamps_low.append(time_stamps[i * conversion_rate])
        for j in range(0, n_exc):
            prices_low[j, i] = prices[j, i * conversion_rate]
            volumes_low[j, i] = np.sum(volumes[j, i * conversion_rate: (i + 1) * conversion_rate])
    return time_stamps_low, prices_low, volumes_low
"""


def convert_to_hour(time_stamps, prices, volumes):
    print(" \033[32;0;0mConverting to hourly data...\033[0;0;0m")
    year, month, day, hour, minute = supp.fix_time_list(time_stamps)
    n_mins = len(time_stamps)
    time_stamps_out = []
    k = 0
    n_exc = np.size(prices, 0)

    if hour[0] == 0:
        opening_hours_only = 0
    else:
        opening_hours_only = 1
        print("  Opening hours only")

    if opening_hours_only == 1:
        n_hours = int(math.ceil(n_mins * (7 / 390)))
        prices_out = np.zeros([n_exc, n_hours])
        volumes_out = np.zeros([n_exc, n_hours])
        for i in range(n_mins - 59):
            if hour[i] == 13 and minute[i] == 30:
                time_stamps_out.append(time_stamps[i])
                for j in range(n_exc):
                    prices_out[j, k] = prices[j, i + 29]  # The price at the last minute of the hour
                    volumes_out[j, k] = np.sum(volumes[j, i:(i + 30)]) * 2  # To make up for missing half hour
                k += 1
            elif minute[i] == 0:
                time_stamps_out.append(time_stamps[i])
                for j in range(n_exc):
                    prices_out[j, k] = prices[j, i + 59]  # The price at the last minute of the hour
                    volumes_out[j, k] = np.sum(volumes[j, i:(i + 60)])
                k += 1
    else:
        n_hours = int(n_mins / 60)
        prices_out = np.zeros([n_exc, n_hours])
        volumes_out = np.zeros([n_exc, n_hours])
        for i in range(n_mins - 59):
            if minute[i] == 0:
                time_stamps_out.append(time_stamps[i])
                for j in range(n_exc):
                    prices_out[j, k] = prices[j, i + 59]  # The price at the last minute of the hour
                    volumes_out[j, k] = np.sum(volumes[j, i:(i + 60)])
                k += 1
    return time_stamps_out, prices_out, volumes_out


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
            if hour[i] == 13 and minute[i] == 30:
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


def average_over_day(time_list, data, frequency="h"):
    year, month, day, hour, minute = supp.fix_time_list(time_list)
    n_entries = len(time_list)
    day_time = []  # Excel stamps for each minute in the day
    h_list = []  # integer indicating which hour it is
    m_list = []  # integer indicating which minute it is

    # Generating day_time ---------------
    if frequency == "h":
        if hour[0] == 13:
            for h in range(13, 20):
                if h < 10:
                    hs = "0" + str(h)
                else:
                    hs = str(h)
                day_time.append(hs + ":" + "00")
                h_list.append(h)
        elif hour[0] == 0:
            for h in range(0, 24):
                if h < 10:
                    hs = "0" + str(h)
                else:
                    hs = str(h)
                day_time.append(hs + ":" + "00")
                h_list.append(h)
        else:
            print("di.average_over_day: Something was wrong with the time_list....")
            return None
    elif frequency == "m":
        if hour[0] == 13:
            for h in range(13, 20):
                if h < 10:
                    hs = "0" + str(h)
                else:
                    hs = str(h)
                if h == 13:
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
        elif hour[0] == 0:
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
            index = hour[i] - hour[0]  # Hvis dagen starter på 13:30 vil vi også at indexen skal starte der
            if index == 0:
                temp_list[index] = data[i]
                temp_matrix.append(temp_list)
                k += 1
                temp_list = np.zeros(n_out)
            else:
                temp_list[index] = data[i]
    elif frequency == "m":
        for i in range(n_entries):
            index = (hour[i] - hour[0]) * 60 + minute[i] - minute[0]  # Hvis dagen starter på 13:30 vil vi også...
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
        lower[i], upper[i] = st.t.interval(percentile, len(temp_matrix[:, i])-1, loc=np.mean(temp_matrix[:, i]), scale=st.sem(temp_matrix[:, i]))

    return day_time, out_data, lower, upper
