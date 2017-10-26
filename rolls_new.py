import math
import data_import as di
from Jacob import jacob_csv_handling, jacob_support
from Sondre import sondre_support_formulas as supp
import matplotlib.pyplot as plt
#import two_axis_plot as two_plot

#The following estimation of Rolls estimator is based on the formula in Haugom, Molnar (2014)


def rolls(prices, price_differences, time_list_minute, window):
    spread = []
    spread_rel = []
    prices_start = []
    time_list_hour = []
    count_value_error = 0
    half_hour = 30
    pos = 0 # position in price diff vector
    half = 1 # indicates that one half hour must be accounted for
    tod = 0 # tod to keep track of when to reset half
    sum_inside = 0
    while pos < len(price_differences)-window:
        if half == 1:
            for i in range(pos+1,pos+half_hour+1):
                sum_inside = sum_inside + (price_differences[i]*price_differences[i-1])
            try:
                ba_calc = 2*math.sqrt(-sum_inside/(half_hour-1))
            except ValueError:
                count_value_error += 1
                ba_calc = 0
            spread.append(ba_calc)
            time_list_hour.append(time_list_minute[pos])
            spread_rel.append(ba_calc/prices[pos])
            prices_start.append(prices[pos])
            half = 0
            pos += 30
            sum_inside = 0
        else:
            for i in range(pos+1, pos+window+1):
                sum_inside = sum_inside + (price_differences[i]*price_differences[i-1])
            try:
                ba_calc = 2*math.sqrt(-sum_inside/(window-1))
            except ValueError:
                count_value_error += 1
                ba_calc = 0
            spread.append(ba_calc)
            time_list_hour.append(time_list_minute[pos])
            spread_rel.append(ba_calc/prices[pos])
            prices_start.append(prices[pos])
            pos += 60
            sum_inside = 0
            if tod == 6:
                tod == 0
                half = 1
            else:
                tod += 1
    return spread, spread_rel, time_list_hour, count_value_error, prices_start


load_price_differences = 1
if load_price_differences:
    # file_name = input("From what file do you want to load data? (raw data with time, price and volume) ")
    to_file = "price_diffs_test.csv"
    time_list = []
    prices = []
    volume = []
    time_list = di.get_lists()[1]
    total_price = di.get_lists()[4]
    # data = jacob_csv_handling.read_single_csv(file_name, time_list, total_price, total_volume)
    price_differences = jacob_support.first_price_differences(total_price) # calculates price difference
    jacob_csv_handling.write_to_file(time_list, price_differences, to_file, "Price_differences")

window1 = 60 # calculate spread for this period of minutes
# window2 = 60*8

print("The length of the price_diff: ", len(price_differences))

print("Calculates BA-spread:")

spread1, spread1_rel, time_list_hour1, count_value_error_1, prices_start = rolls(total_price, price_differences, time_list, window1)
# spread2, time_list_hour2, count_value_error_2 = rolls_new(price_differences, time_list, window2)

jacob_csv_handling.write_to_file(time_list_hour1, spread1_rel, "relative_spreads.csv", "Relative spread from Roll")
jacob_csv_handling.write_to_file(time_list_hour1, prices_start, "prices_start.csv", "Price")


"""
for i in range(0,len(spread2)):
    spread2_rel.append(spread2[i]/total_price[i*window2])
"""


print(len(spread1))
print(len(spread1_rel))

# print(len(spread2))

print("The following is the BAs with window", window1)
print(time_list_hour1)
print(spread1)
print(spread1_rel)
print("With", window1, "window,", count_value_error_1, "value errors were counted")

"""
print("The following is the BAs with window",window2)
print(time_list_hour2)
print(spread2)
print("With",window2,"window,",count_value_error_2,"value errors were counted")
"""

x = []
for i in range(0, len(spread1_rel)):
    x.append(i)


print(max(spread1_rel))


plt.bar(x, spread1_rel)
plt.ylim(0.0, 0.1)
plt.show()


