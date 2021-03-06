import csv
import numpy as np
from Sondre.sondre_support_formulas import count_rows
from Sondre import sondre_support_formulas as supp
import data_import_support as dis


def get_list(exc=0, freq="m", local_time=0): # testtest

    if exc == 0 or exc == "bitstampusd" or exc == "bitstamp":
        exc_name = "bitstampusd"
        exc = 0
    elif exc == 1 or exc == "coincheckjpy" or exc == "coincheck":
        exc_name = "coincheckjpy"
        exc = 1
    elif exc == 2 or exc == "btcncny" or exc == "btcn":
        exc_name = "btcncny"
        exc = 2
    elif exc == 3 or exc == "coinbaseusd" or exc == "coinbase":
        exc_name = "coinbaseusd"
        exc = 3
    elif exc == 4 or exc == "korbitkrw" or exc == "korbit":
        exc_name = "korbitkrw"
        exc = 4
    elif exc == 5 or exc == "krakeneur"or exc == "kraken":
        exc_name = "krakeneur"
        exc = 5
    elif exc == -1 or exc == "test":
        exc_name = "test"
        exc = -1
    else:
        print("\033[31;0;0mYou did not choose an exchange, so I am returning bitstamp\033[0;0;0m")
        exc_name = "bitstampusd"

    if freq == "m" or freq == 0:
        file_name = "data/export_csv/" + exc_name + "_edit.csv"
        time_listM = []
        priceM = []
        volumeM = []

        with open(file_name, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=';', quotechar='|')
            print("\033[0;32;0m Reading file '%s'...\033[0;0;0m" % file_name)
            i = 0
            next(reader)
            next(reader)
            next(reader)
            for row in reader:
                try:
                    time_listM.append(str(row[0]))
                    priceM.append(float(row[1]))
                    volumeM.append(float(row[2]))
                except ValueError:
                    print("\033[0;31;0m There was an error on row %i in '%s'\033[0;0;0m" % (i + 1, file_name))
                i = i + 1

        return exc_name, time_listM, priceM, volumeM

    elif freq =="h" or freq ==1:
        file_name = "data/export_csv/" + exc_name + "_global_time_hourly.csv"

        time_listH, returnsH, spreadH, volumesH, log_volumesH, illiqH, log_illiqH, rvolH, log_rvolH = read_clean_csv(file_name)

        if local_time == 1:
            if exc == 0 or exc == 5:
                n_hours = 1
            elif exc == 1:
                n_hours = 9
            elif exc == 2:
                n_hours = 8
            elif exc == 3:
                n_hours = -5
            elif exc == 4:
                n_hours = 9
            else:
                n_hours = 0
            print("  Converting time zones: moving series %i hour(s)" % n_hours)
        else:
            n_hours = 0

        if n_hours != 0:
            year, month, day, freq, minute = supp.fix_time_list(time_listH, move_n_hours=n_hours)
            time_listH = supp.make_time_list(year, month, day, freq, minute)  # Lager en ny tidsliste fra de flyttede listene
        return exc_name, time_listH, returnsH, spreadH, volumesH, log_volumesH, illiqH, log_illiqH, rvolH, log_rvolH

    else:
        file_name = "data/export_csv/" + exc_name + "_daily.csv"
        time_listD, returnsD, spreadD, volumesD, log_volumesD, illiqD, log_illiqD, rvolD, log_rvolD = read_clean_csv(file_name)

        return exc_name, time_listD, returnsD, spreadD, volumesD, log_volumesD, illiqD, log_illiqD, rvolD, log_rvolD


def fetch_long_and_write(exchanges, opening_hours_only="n"):
    n_exc = len(exchanges)
    excel_stamps, unix_stamps, prices, volumes = legacy.get_price_volume_from_fulls(exchanges)

    if opening_hours_only == "y":
        excel_stamps, prices, volumes = legacy.opening_hours(excel_stamps, prices, volumes)
        filename = "data/export_csv/minute_data.csv"
    else:
        filename = "data/export_csv/minute_data_full_day.csv"

    legacy.write_full_lists_to_csv(volumes, prices, excel_stamps, exchanges, filename)


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


def get_global_volume_actual_daily():
    file_name = 'data/export_csv/volume_daily.csv'
    time_listD = []
    volumesD = []

    with open(file_name, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=';', quotechar='|')
        print("\033[0;32;0m Reading file '%s'...\033[0;0;0m" % file_name)
        i = 0
        next(reader)
        for row in reader:
            try:
                time_listD.append(row[0])
                volumesD.append(float(row[1]))
            except ValueError:
                print("\033[0;31;0m There was an error on row %i in '%s'\033[0;0;0m" % (i + 1, file_name))
            i = i + 1
    print("\033[0;32;0m Finished reading file '%s'...\033[0;0;0m" % file_name)
    return time_listD, volumesD


def get_real_spread(exchange_name):
    time_list = []
    spread = []

    file_name = 'data/export_csv/' + exchange_name + "_real_spread.csv"

    with open(file_name, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        print("\033[0;32;0m Reading file '%s'...\033[0;0;0m" % file_name)
        i = 0
        next(reader)
        for row in reader:
            try:
                ts = row[0][0:16]
                time_stamp = ts[8:10] + "."+ts[5:7]+"."+ts[0:4]+" "+ts[11:16]
                time_list.append(time_stamp)
                spread.append(float(row[1]))
            except ValueError:
                print("\033[0;31;0m There was an error on row %i in '%s'\033[0;0;0m" % (i + 1, file_name))
            i = i + 1
    print("\033[0;32;0m Finished reading file '%s'...\033[0;0;0m" % file_name)
    return time_list, spread


def read_clean_csv(file_name):
    time_list= []
    returns = []
    spread = []
    volumes= []
    log_volumes = []
    illiq = []
    log_illiq = []
    rvol = []
    log_rvol = []
    with open(file_name, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=';', quotechar='|')
        print("\033[0;32;0m Reading file '%s'...\033[0;0;0m" % file_name)
        i = 0
        next(reader)
        next(reader)
        next(reader)
        for row in reader:
            try:
                time_list.append(row[0])
                returns.append(float(row[1]))
                spread.append(float(row[2]))
                volumes.append(float(row[3]))
                log_volumes.append(float(row[4]))
                illiq.append(float(row[5]))
                log_illiq.append(float(row[6]))
                rvol.append(float(row[7]))
                log_rvol.append(float(row[8]))
            except ValueError:
                print("\033[0;31;0m There was an error on row %i in '%s'\033[0;0;0m" % (i + 1, file_name))
            i = i + 1
    #print("\033[0;32;0m Finished reading file '%s'...\033[0;0;0m" % file_name)
    return time_list, returns, spread, volumes, log_volumes, illiq, log_illiq, rvol, log_rvol