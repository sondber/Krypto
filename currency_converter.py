# Takes as input a csv of prices and and the corresponding currency as string. Fetches correct rate and converts.
# Exports to CSV

from Jacob import jacob_csv_handling as csv_handling
from Sondre import sondre_support_formulas as supp


def currency_converter(prices_time, prices, xrate_times, xrate):
    prices_day = []
    prices_month = []
    prices_year = []
    xrate_date = []
    xrate_month = []
    xrate_year = []
    prices_converted = []

    prices_year, prices_month, prices_day = supp.fix_time_list(prices_time) #this is probably inccorect, need to decide the output
    xrate_year, xrate_month, xrate_day = supp.fix_time_list(xrate_times) #see line above

    for i in range(0,len(prices)):
        found = 0
        j = 0
        while not found:
            if prices_year[i] == xrate_year[j] and prices_month[i] == xrate_month[j] and prices_day[i] == xrate_day[j]:
                found = 1
                prices_converted.append(prices[i]*xrate[j])
            j += 1
        if not len(prices_time)==len(prices_converted):
            print("For some reason, all prices could not be converted")

    return prices_time, prices_converted

def import_data(price_file, currency): #price_file as string, currency as string ("JPY")
    timestamp_price = []
    timestamp_xrate = []
    xrate = []
    price = []
    timestamp_price, price = csv_handling.read_price_csv(price_file, timestamp_price, price)
    timestamp_xrate, xrate = csv_handling.read_currency_csv("data/bitcoincharts/"+ currency + ".csv", timestamp_xrate, xrate)
    return timestamp_price, price, timestamp_xrate, xrate

##testing










