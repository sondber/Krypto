import sondre_support_formulas as supp  # Egen
import user_interface as ui  # Egen


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

    if no_extreme:
        n_stds_volume = int(input("How many standard deviations away from mean do we allow? ") or 3)
        for i in range(0, n_exc):
            volumes[i, :] = supp.remove_extremes(volumes[i, :], n_stds_volume, 1, 0)

    total_volume, total_prices = supp.all_in_one_list(volumes, prices)

    return exchanges, time_list, prices, volumes, total_prices, total_volume, currency


def convert_to_lower_freq(time_list, total_price, total_volume):
    day_time, daily_price = supp.minute_to_daily_prices(time_list, total_price)
    daily_volume = supp.minute_to_daily_volumes(time_list, total_volume)[1]  # ettallet på slutten er fordi jeg ikke trenger å hente ut tiden på nytt
    hour_time, hour_price = supp.minute_to_hourly_prices(time_list, total_price)
    hour_volume = supp.minute_to_hourly_volumes(time_list, total_volume)[1]  # ettallet på slutten er fordi jeg ikke trenger å hente ut tiden på nytt

    # Skrive til fil

    supp.write_to_daily_file(day_time, daily_volume, daily_price)
    supp.write_to_hourly_file(hour_time, hour_volume, hour_price)


def get_lists(which_freq, which_loc):
    startdate = "201301"
    enddate = "201709"

    if which_freq == 0:
        file_name = 'data/export_csv/daily_data.csv'
    elif which_freq == 1:
        file_name = 'data/export_csv/hourly_data.csv'
    elif which_freq == 2:
        file_name = 'data/export_csv/minute_data.csv'

    if which_loc == 1:
        time_list, prices, volumes = supp.fetch_aggregate_csv(file_name, 1)
        total_volume, total_price = supp.all_in_one_list(volumes, prices)
        exchanges = ["bitstampusd"]
        currency = 0
    else:
        compex, currency, no_extreme = ui.import_data()
        exchanges, time_list, prices, volumes, total_price, total_volume, currency = get_data(compex, currency, no_extreme, startdate, enddate)
        if compex == 0:
            convert_to_lower_freq(time_list, total_price, total_volume)
        else:
            file_name = "data/export_csv/raw_data_compex.csv"

        n_exc = len(exchanges)
        # Gjør akkurat det samme som if which_loc == 1
        time_list, prices, volumes = supp.fetch_aggregate_csv(file_name, n_exc)

    return exchanges, time_list, prices, volumes, total_price, total_volume, currency
