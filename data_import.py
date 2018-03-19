import data_import_support
import data_import_support as dis
import csv
from Sondre import sondre_support_formulas as supp


def get_lists_legacy(data="all", opening_hours="y", make_totals="y"):
    exchanges = ["bitstampusd", "coincheckjpy", "btcncny"]
    n_exc = len(exchanges)
    print("Fetching minute data..." )

    if opening_hours == "y":
        oh = ""
        print(" \033[32;0;0mOnly fetching data for NYSE opening hours...\033[0;0;0m")
    else:
        oh = "_full_day"

    file_name = "data/export_csv/minute_data" + oh + ".csv"
    time_list, prices, volumes = data_import_support.fetch_aggregate_csv(file_name, n_exc)

    if make_totals == "y":
        total_volume, total_price = supp.make_totals(volumes, prices)
        if data == "price" or data == "p" or data == "prices":
            return total_price
        elif data == "volume" or data == "v" or data == "volumes":
            return total_volume
        else:
            return exchanges, time_list, prices, volumes, total_price, total_volume
    else:
        return exchanges, time_list, prices, volumes


def get_list(exc=0):
    if exc == 1:
        name = "coincheckjpy"
    elif exc == 2:
        name = "btcncny"
    elif exc == 3:
        name = "coinbaseusd"
    else:
        name = "bitstampusd"

    file_name = "data/export_csv/" + name + "_edit.csv"
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

    return time_listM, priceM, volumeM




def fetch_long_and_write(exchanges, opening_hours_only="n"):
    n_exc = len(exchanges)
    excel_stamps, unix_stamps, prices, volumes = dis.get_price_volume_from_fulls(exchanges)

    if opening_hours_only == "y":
        excel_stamps, prices, volumes = dis.opening_hours(excel_stamps, prices, volumes)
        filename = "data/export_csv/minute_data.csv"
    else:
        filename = "data/export_csv/minute_data_full_day.csv"

    dis.write_full_lists_to_csv(volumes, prices, excel_stamps, exchanges, filename)


