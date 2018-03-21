import csv
import numpy as np
from Sondre.sondre_support_formulas import count_rows


def get_list(exc=0):

    if exc == 0:
        exc_name = "bitstampusd"
    elif exc == 1:
        exc_name = "coincheckjpy"
    elif exc == 2:
        exc_name = "btcncny"
    elif exc == 3:
        exc_name = "coinbaseusd"
    elif exc == 4:
        exc_name = "korbitkrw"
    elif exc == -1:
        exc_name = "test"

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