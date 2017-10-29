from Sondre import sondre_support_formulas as supp, user_interface as ui
import data_import_support as dis
import numpy as np
import currency_converter as curr


def get_lists(which_freq=2, data="all", opening_hours="y", make_totals="y"):
    exchanges = ["bitstampusd", "btceusd", "coinbaseusd", "krakenusd"]
    n_exc = len(exchanges)

    if which_freq == 0 or which_freq == "day" or which_freq == "d":
        freq = "daily"
    elif which_freq == 1 or which_freq == "hour" or which_freq == "h":
        freq = "hourly"
    elif which_freq == 2 or which_freq == "min" or which_freq == "m":
        freq = "minute"
    else:
        freq = "minute"
    print("Fetching %s data..." % freq)

    if opening_hours == "y":
        oh = ""
        print(" \033[32;0;0mOnly fetching data for NYSE opening hours...\033[0;0;0m")
    else:
        oh = "_full_day"

    file_name = "data/export_csv/" + freq + "_data" + oh + ".csv"
    time_list, prices, volumes = supp.fetch_aggregate_csv(file_name, n_exc)

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


def fetch_long_and_write(exchanges, opening_hours_only="y"):
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
    if opening_hours_only == "y":
        excel_stamps, prices, volumes = dis.opening_hours(excel_stamps, prices, volumes)
        filename = "data/export_csv/minute_data.csv"
    else:
        filename = "data/export_csv/minute_data_full_day.csv"

    dis.write_full_lists_to_csv(volumes, prices, excel_stamps, exchanges, filename)

    for i in range(5, 10, 5):
        time_stamps_min, prices_min, volumes_min = dis.convert_to_lower_freq(excel_stamps, prices, volumes, conversion_rate=i)
        filename = "data/export_csv/" + str(i) +"mins.csv"


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
    excel_stamps = dis.fix_gold_stamps(date, time_NYC)
    file_name = "data/export_csv/gold_data.csv"
    dis.write_to_gold_csvs(excel_stamps, volume, price, bid, ask, file_name)
