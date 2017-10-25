import csv
from Sondre import sondre_support_formulas as supp
import numpy as np


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
    tenperc = n_stamps_unix/10
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
            mo = mo +1
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
                price.append(float(row[7]))
                volume.append(float(row[5]))
            except ValueError:
                print("\033[0;31;0m There was an error on row %i in '%s'\033[0;0;0m" % (i+1, file_name))
            i = i + 1
        return time_list, price, volume


def make_excel_stamp(y, mo, d, h, mi):
    ys = str(y)
    if mo<10:
        mos = "0" + str(mo)
    else:
        mos = str(mo)
    if d<10:
        ds = "0" + str(d)
    else:
        ds = str(d)
    if h<10:
        hs = "0" + str(h)
    else:
        hs = str(h)
    if mi<10:
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
        print("Working on exchange %i/%i" % ((i+1), n_exc))
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
            currency = exc[len(exc)-3: len(exc)]
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


def opening_hours(in_excel_stamps, in_prices, in_volumes):
    year, month, day, hour, minute = supp.fix_time_list(in_excel_stamps)
    n_mins = len(in_excel_stamps)
    out_excel_stamps = []
    out_prices = []
    out_volumes = []
    for i in range(n_mins):
        if 14 <= hour[i] <= 19 or (hour[i] == 13 and minute[i] >= 30):
            out_excel_stamps.append(in_excel_stamps[i])
            out_prices.append(in_prices[:, i])
            out_volumes.append(in_volumes[:, i])
    out_prices = np.transpose(np.matrix(out_prices))
    out_volumes = np.transpose(np.matrix(out_volumes))
    return out_excel_stamps, out_prices, out_volumes


<<<<<<< HEAD
def convert_to_lower_freq(time_stamps, prices, volumes, conversion_rate=60):
    n_cols_high = len(time_stamps)
    n_exc = np.size(volumes, 0)
    n_cols_low = int(n_cols_high/conversion_rate)
    time_stamps_low = []
    prices_low = np.zeros([n_exc, n_cols_low])
    volumes_low = np.zeros([n_exc, n_cols_low])
    for i in range(0, n_cols_low):
        time_stamps_low.append(time_stamps[i * conversion_rate])
        for j in range(0, n_exc):
            prices_low[j, i] = prices[j, i * conversion_rate]
            volumes_low[j, i] = volumes[j, i * conversion_rate]
    return time_stamps_low, prices_low, volumes_low
=======
#def convert_to_lower_freq(time_stamps, prices, volumes, conversion_rate=60):
    
>>>>>>> markus
