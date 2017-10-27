import math
import data_import as di
from Jacob import jacob_csv_handling, jacob_support
import matplotlib.pyplot as plt


# The following estimation of Rolls estimator is based on the formula in Haugom, Molnar (2014)


def rolls(prices, price_differences, time_list_minute, day=0):
    window = 60
    spread = []
    spread_rel = []
    prices_start = []
    time_list_hour = []
    count_value_error = 0
    half_hour = 30
    if day == 0:
        pos = 0  # position in price diff vector
        half = 1  # indicates that one half hour must be accounted for
        tod = 0  # tod to keep track of when to reset half
        sum_inside = 0
        while pos < len(price_differences):
            if half == 1:
                for i in range(pos + 1, pos + half_hour):
                    sum_inside = sum_inside + (price_differences[i] * price_differences[i - 1])
                try:
                    ba_calc = 2 * math.sqrt(-sum_inside / (half_hour - 1))
                except ValueError:
                    count_value_error += 1
                    ba_calc = 0
                spread.append(ba_calc)
                time_list_hour.append(time_list_minute[pos])
                spread_rel.append(ba_calc / prices[pos])
                prices_start.append(prices[pos])
                half = 0
                pos += 30
                sum_inside = 0
            else:
                for i in range(pos + 1, pos + window):
                    sum_inside = sum_inside + (price_differences[i] * price_differences[i - 1])
                try:
                    ba_calc = 2 * math.sqrt(-sum_inside / (window - 1))
                except ValueError:
                    count_value_error += 1
                    ba_calc = 0
                spread.append(ba_calc)
                time_list_hour.append(time_list_minute[pos])
                spread_rel.append(ba_calc / prices[pos])
                prices_start.append(prices[pos])
                # pos += 60
                sum_inside = 0
                if tod == 5:
                    tod = 0
                    half = 1
                    pos += 60
                else:
                    tod += 1
                    pos += 60
    else:
        sum_inside = 0
        if day == 1:
            minutes_in_window = (6*60)+30
        else:
            minutes_in_window = ((6*60)+30)*5

        for i in range(0, len(price_differences) if day == 1 else len(price_differences)-minutes_in_window, minutes_in_window):
            for y in range(i+1, i+minutes_in_window):
                sum_inside = sum_inside + (price_differences[y] * price_differences[y - 1])
            try:
                ba_calc = 2 * math.sqrt(-sum_inside / (minutes_in_window - 1))
            except ValueError:
                count_value_error += 1
                ba_calc = 0
            spread.append(ba_calc)
            time_list_hour.append(time_list_minute[i])
            spread_rel.append(ba_calc / prices[i])
            prices_start.append(prices[i])
            sum_inside = 0

    return spread, spread_rel, time_list_hour, count_value_error, prices_start

day= int(input("Calculate Rolls on an hourly (0) or daily(1) or weekly(2) basis: "))
if day == 0:
    suffix  = "hourly"
elif day == 1:
    suffix = "daily"
else:
    suffix = "weekly"


load_price_differences = 1
if load_price_differences:
    to_file = "data/export_csv/price_diffs_"+suffix+".csv"
    time_list = []
    prices = []
    volume = []
    time_list = di.get_lists()[1]
    total_price = di.get_lists()[4]
    price_differences = jacob_support.first_price_differences(total_price)  # calculates price difference
    jacob_csv_handling.write_to_file(time_list, price_differences, to_file, "Price_differences")

window1 = 60  # calculate spread for this period of minutes

print("The length of the price_diff: ", len(price_differences))

print("Calculates BA-spread ...")


spread1, spread1_rel, time_list_hour1, count_value_error_1, prices_start = rolls(total_price, price_differences,
                                                                                 time_list, day)
print("The BA-spreads are now calculated.")

jacob_csv_handling.write_to_file(time_list_hour1, spread1_rel, "data/export_csv/relative_spreads_"+suffix+".csv",
                                 "Relative spread from Roll")


print("The length of the spread-vector is", len(spread1))
print("The length of the time-vector is", len(time_list_hour1))

print("The following is the BAs calculated",suffix)
print(time_list_hour1)
print(spread1)
print(spread1_rel)
print(count_value_error_1, "value errors were counted when calculating", suffix, "Rolls")