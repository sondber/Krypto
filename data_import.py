from Sondre import sondre_support_formulas as supp, user_interface as ui
import data_import_support as dis
import numpy as np
import currency_converter as curr


# Denne krever litt jobb med ny datastruktur!
def get_lists(which_freq=2, data="all", compex=1):
    # Bruker ikke which_loc
    exchanges = ["bitstampusd", "btceusd", "coinbaseusd", "krakenusd"]
    n_exc = len(exchanges)


    if compex == 0:
        comp ="_total"
    else:
        comp = ""

    if which_freq == 0 or which_freq == "day" or which_freq == "d":
        freq = "daily"
    elif which_freq == 1 or which_freq == "hour" or which_freq == "h":
        freq = "hourly"
    elif which_freq == 2 or which_freq == "min" or which_freq == "m":
        freq = "minute"
    else:
        freq = "minute"
    print("Fetching %s data..." % freq)

    file_name = "data/export_csv/" + freq + "_data" + comp + ".csv"
    time_list, prices, volumes = supp.fetch_aggregate_csv(file_name, n_exc)
    total_volume, total_price = supp.make_totals(volumes, prices)
    currency = 0

    if data == "price" or data == "p":
        return total_price
    elif data == "volume" or data == "v":
        return total_volume
    else:
        return exchanges, time_list, prices, volumes, total_price, total_volume, currency


def fetch_long_and_write(exchanges):
    n_exc = len(exchanges)
    excel_stamps, unix_stamps, prices, volumes = dis.get_lists_from_fulls(exchanges)

    # Convert currencies
    """
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
    """

    excel_stamps, prices, volumes = dis.opening_hours(excel_stamps, prices, volumes)

    filename = "data/export_csv/minute_data.csv"
    dis.write_full_lists_to_csv(volumes, prices, excel_stamps, exchanges, filename)
