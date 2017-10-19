# Takes as input a csv of prices and and the corresponding currency as string. Fetches correct rate and converts.
# Exports to CSV

from Jacob import jacob_csv_handling as csv_handling
from Sondre import sondre_support_formulas as supp


def currency_converter(prices_time, prices, xrate_times, xrate):
    prices_converted = []

    prices_year, prices_month, prices_day, hour, minute = supp.fix_time_list(prices_time)
    xrate_year, xrate_month, xrate_day, hour, minute = supp.fix_time_list(xrate_times)

    for i in range(0, len(prices)):
        found = 0
        j = 0
        while not found:
            if prices_year[i] == xrate_year[j] and prices_month[i] == xrate_month[j] and prices_day[i] == xrate_day[j]:
                found = 1
                prices_converted.append(prices[i]*xrate[j])
            j += 1
        if not len(prices_time) == len(prices_converted):
            print("For some reason, all prices could not be converted")

    return prices_time, prices_converted


def convert_to_USD(price_in_foreign_currency, currency): #price_file as string, currency as string ("JPY")
    timestamp_price = []
    timestamp_xrate = []
    xrate = []
    price = []
    timestamp_price, price = csv_handling.read_price_csv(price_in_foreign_currency, timestamp_price, price)
    timestamp_xrate, xrate = csv_handling.read_currency_csv("data/Forex/" + currency + ".csv", timestamp_xrate, xrate)
    # test med csv-fetch, deretter lag kun med liste-input
    prices_time, prices_converted = currency_converter(timestamp_price, price, xrate_times, xrate)

    return prices_time, prices_converted

##testing

prices_time, prices_converted = convert_to_USD("test_NOTSYNC.csv", "JPY")


#timestamp_price = []
#timestamp_xrate = []
#xrate = []
#price = []
#timestamp_prices, prices = csv_handling.read_price_csv("test_NOTSYNC.csv",  timestamp_price, price)







