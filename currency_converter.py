# Takes as input a csv of prices and and the corresponding currency as string. Fetches correct rate and converts.
# Exports to CSV
# Function to call is  "convert_to_usd"

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
                prices_converted.append(prices[i]/xrate[j])
            j += 1
    if not len(prices_time) == len(prices_converted):
        print("For some reason, all prices could not be converted")

    return prices_time, prices_converted


def convert_to_usd(timestamp_price, price_in_foreign_currency, currency): # prices as 2D-matrix with timestamp and price WITHOUT HEADER, currency as string ("JPY")
    # timestamp_price = price_in_foreign_currency[0] # stores timestamp of prices in own vector
    # price = price_in_foreign_currency[1] # stores prices of prices in own vector
    price = price_in_foreign_currency
    timestamp_xrate = []
    currency = currency.upper()  # Makes sure the currency code is all upper case
    xrate = []
    timestamp_xrate, xrate = csv_handling.read_currency_csv("data/Forex/" + currency + ".csv", timestamp_xrate, xrate) # fetches xrates
    prices_time, prices_converted = currency_converter(timestamp_price, price, timestamp_xrate, xrate)  # processes each price

    return prices_time, prices_converted

##testing
#prices_time, prices_converted = convert_to_USD(TESTLIST(TWODIM_teimstamp_price), "EUR")