from Sondre import sondre_support_formulas as supp, user_interface as ui
import data_import_support as dis
import numpy as np
import currency_converter as curr
"""
def get_data(compare_exchanges, convert_to_usd, no_extreme, startdate, enddate):

    compex = compare_exchanges
    currency = convert_to_usd

    # If compex, we look at all the exchanges, but for a shorter time span. Otherwise we look at the full time span, but only for bitstampusd
    if compex:
        exchanges = ["bitstampusd", "coincheckjpy", "btcncny", "krakeneur", "krakenusd"]
        first_year = 2017
        final_year = 2017
        first_month = 7
        final_month = 8
        raw_data_location = "data/export_csv/raw_data_compex.csv"
    else:
        exchanges = ["bitstampusd"]
        first_year = int(startdate[0:4])
        final_year = int(enddate[0:4])
        first_month = int(startdate[4:7])
        final_month = int(enddate[4:7])
        raw_data_location = "data/export_csv/minute_data.csv"

    n_exc = len(exchanges)

    print("\nDATA IMPORT")
    print("---------------------------------------------------------------------------------\n")
    print("Gathering data...")

    volumes, prices, time_list = supp.gather_exchanges(exchanges, first_year, first_month, final_year, final_month)
    supp.write_to_raw_file(volumes, prices, time_list, exchanges, raw_data_location)

    if currency or no_extreme:
        print("\n")
        print("DATA CLEANUP AND CONVERSION")
        print("---------------------------------------------------------------------------------\n")

    if currency:
        prices = supp.convert_currencies(exchanges, prices)
    elif compex == 1:
        print("NB! Original currencies...\n")

    total_volume, total_prices = supp.make_totals(volumes, prices)

    return exchanges, time_list, prices, volumes, total_prices, total_volume, currency
"""


def convert_to_lower_freq(time_list, total_price, total_volume):
    day_time, daily_price = supp.minute_to_daily_prices(time_list, total_price)
    daily_volume = supp.minute_to_daily_volumes(time_list, total_volume)[1]  # ettallet på slutten er fordi jeg ikke trenger å hente ut tiden på nytt
    hour_time, hour_price = supp.minute_to_hourly_prices(time_list, total_price)
    hour_volume = supp.minute_to_hourly_volumes(time_list, total_volume)[1]  # ettallet på slutten er fordi jeg ikke trenger å hente ut tiden på nytt

    # Skrive til fil

    supp.write_to_daily_file(day_time, daily_volume, daily_price)
    supp.write_to_hourly_file(hour_time, hour_volume, hour_price)


# Denne krever litt jobb med ny datastruktur!
def get_lists(which_freq=2, which_loc=1, data="all", compex=0):
    # Bruker ikke which_loc
    exchanges = ["bitstampusd", "btceusd", "coinbaseusd", "krakenusd"]
    n_exc = len(exchanges)

    if compex == 0:
        if which_freq == 0 or which_freq == "day" or which_freq == "d":
            file_name = "data/export_csv/daily_data.csv"
            print("Fetching daily data...")
        elif which_freq == 1 or which_freq == "hour" or which_freq == "h":
            file_name = "data/export_csv/hourly_data.csv"
            print("Fetching hourly data...")
        elif which_freq == 2 or which_freq == "min" or which_freq == "m":
            file_name = "data/export_csv/minute_data.csv"
            print("Fetching minute data...")
        else:
            print("Bad input")
            file_name = "data/export_csv/full_raw_data.csv"
    else:
        file_name = "data/export_csv/full_raw_data.csv"

    time_list, prices, volumes = supp.fetch_aggregate_csv(file_name, n_exc)
    total_volume, total_price = supp.make_totals(volumes, prices)
    currency = 0

    if data == "price" or data == "prices" or data == "p":
        return total_price
    elif data == "volume" or data == "volumes" or data == "v":
        return total_volume
    else:
        return exchanges, time_list, prices, volumes, total_price, total_volume, currency


def fetch_long_and_write(exchanges):
    n_exc = len(exchanges)
    excel_stamps, unix_stamps, prices, volumes = dis.get_lists_from_fulls(exchanges)
    filename = "data/export_csv/full_raw_data.csv"
    dis.write_full_lists_to_csv(volumes, prices, excel_stamps, exchanges, filename)

    # Convert currencies
    print()
    print("Currency conversion:---------")
    prices_usd = []
    for i in range(0, n_exc):
        # sjekker valuta
        exc = exchanges[i]
        l_exc = len(exc)
        currency = exc[l_exc - 3:l_exc]
        if currency != "usd":
            print(" Converting currency of %s from %s to USD..." % (exc, currency.upper()))
            print("  This may take several minutes for a single conversion")
            single_price_usd = curr.convert_to_usd(excel_stamps, prices[i,:], currency)
            prices_usd.append(single_price_usd)
        else:
            print(" %s is already USD" % exc)
            prices_usd.append(prices[i,:])

    prices_usd = np.matrix(prices_usd)
    minute_total_volume, minute_total_price = supp.make_totals(volumes, prices_usd)

    minute_filename = "data/export_csv/minute_data.csv"
    minute_excel_stamps = excel_stamps
    dis.write_to_total_files(minute_total_volume, minute_total_price, minute_excel_stamps, minute_filename)

    hour_excel_stamps, hour_total_price = supp.minute_to_hourly_prices(minute_excel_stamps, minute_total_price)
    hour_total_volume = supp.minute_to_hourly_volumes(minute_excel_stamps, minute_total_volume)[1]
    hour_filename = "data/export_csv/hourly_data.csv"
    dis.write_to_total_files(hour_total_volume, hour_total_price, hour_excel_stamps, hour_filename)

    day_excel_stamps, day_total_price = supp.minute_to_daily_prices(minute_excel_stamps, minute_total_price)
    day_total_volume = supp.minute_to_daily_volumes(minute_excel_stamps, minute_total_volume)[1]
    day_filename = "data/export_csv/daily_data.csv"
    dis.write_to_total_files(day_total_volume, day_total_price, day_excel_stamps, day_filename)
