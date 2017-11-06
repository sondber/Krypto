import math
from Sondre import sondre_support_formulas as supp
import data_import as di
import numpy as np
import matplotlib.pyplot as plt

# The following estimation of Rolls estimator is based on the formula in Haugom, Molnar (2014)


def first_price_differences(prices):  # takes list of prices, returns equal length list of first price differences
    returnlist = [float(0)]
    for i in range(1, len(prices)):  # check the logic of setting first index to zero in relation to return calculation
        try:
            returnlist.append(prices[i] - prices[(i - 1)])
        except ValueError:
            returnlist.append(float(0))
            print("Something wrong happened when calculating price difference")
    return returnlist


def rolls(prices_minute, time_list_minute, calc_basis=0, kill_output=0):  # calc_basis 0/1/2 hour/day/week
    year, month, day, hour, minute = supp.fix_time_list(time_list_minute)
    spread = []
    spread_rel = []
    time_list = []
    count_value_error = 0
    count_corr_below = 0
    corr_threshold = 0.2
    if kill_output == 0:
        print("Calculating first price differences ...")
    price_differences = first_price_differences(prices_minute)  # calculates price difference
    if kill_output == 0:
        print("Price differences-calculation finished. ")

    # determine opening hours yes/no
    if hour[0] == 13:  # this indicates that opening times are being investigated
        opening_times = 1
        opening_hours_desc = "opening hours"
    else:
        opening_times = 0
        opening_hours_desc = "full day"

    # determine minutes_in_window based on opening_hours and calc_basis
    if opening_times == 1:
        if calc_basis == 1:  # daily with opening hours only
            minutes_in_window = (6 * 60) + 30
            freq_desc = "daily"
        elif calc_basis == 2:  # weekly with openings hours only
            minutes_in_window = ((6 * 60) + 30) * 5
            freq_desc = "weekly"
        else:  # hourly with openings hours. Minutes_in_window is not used in this case
            freq_desc = "hourly"
    else:
        if calc_basis == 0:  # hourly with full data
            minutes_in_window = 60
            freq_desc = "hourly"
        elif calc_basis == 1:  # daily with full data
            minutes_in_window = 60 * 24
            freq_desc = "daily"
        else:  # weekly with full data
            minutes_in_window = 60 * 24 * 7
            freq_desc = "weekly"

    if kill_output == 0:
        print("Calculating spreads on a/an", freq_desc, "basis using", opening_hours_desc, "data")

    if calc_basis == 0 and opening_times:  # opening times and hourly basis needs to account for half hours
        half_hour = 30
        window = 60
        pos = 0  # position in price diff vector
        half = 1  # indicates that one half hour must be accounted for
        tod = 0  # tod to keep track of when to reset half
        sum_inside = 0
        while pos < len(price_differences):
            if half == 1:
                list1 = price_differences[pos:pos + half_hour - 1]
                list2 = price_differences[pos + 1:pos + half_hour]
                corr = np.corrcoef(list1, list2)[0, 1]
                if abs(corr) < corr_threshold:
                    count_corr_below += 1
                for i in range(pos + 1, pos + half_hour):
                    sum_inside = sum_inside + (price_differences[i] * price_differences[i - 1])
                try:
                    ba_calc = 2 * math.sqrt(-sum_inside / (half_hour - 2))
                except ValueError:
                    count_value_error += 1
                    ba_calc = 0
                spread.append(ba_calc)
                time_list.append(time_list_minute[pos])
                if prices_minute[pos] == 0:
                    print("Here is a zero!")
                spread_rel.append(ba_calc / prices_minute[pos])
                half = 0
                pos += 30
                sum_inside = 0
            else:
                list1 = price_differences[pos:pos + window - 1]
                list2 = price_differences[pos + 1:pos + window]
                corr = np.corrcoef(list1, list2)[0, 1]
                if abs(corr) < corr_threshold:
                    count_corr_below += 1
                for i in range(pos + 1, pos + window):
                    sum_inside = sum_inside + (price_differences[i] * price_differences[i - 1])
                try:
                    ba_calc = 2 * math.sqrt(-sum_inside / (window - 2))
                except ValueError:
                    count_value_error += 1
                    ba_calc = 0
                spread.append(ba_calc)
                time_list.append(time_list_minute[pos])
                spread_rel.append(ba_calc / prices_minute[pos])
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
        for i in range(0, len(price_differences) - minutes_in_window if calc_basis == 2 else len(price_differences),
                       minutes_in_window):
            list1 = price_differences[i:i + minutes_in_window - 1]
            list2 = price_differences[i + 1:i + minutes_in_window]
            corr = np.corrcoef(list1, list2)[0, 1]
            if abs(corr) < corr_threshold:
                count_corr_below += 1
            for y in range(i + 1, i + minutes_in_window):
                sum_inside = sum_inside + (price_differences[y] * price_differences[y - 1])
            try:
                ba_calc = 2 * math.sqrt(-sum_inside / (minutes_in_window - 2))
            except ValueError:
                count_value_error += 1
                ba_calc = 0
            spread.append(ba_calc)
            time_list.append(time_list_minute[i])
            spread_rel.append(ba_calc / prices_minute[i])
            sum_inside = 0
    if kill_output == 0:
        print("Spreads-calculation is finished")
        print("The length of the spread-vector is", len(spread_rel))
        print("The length of the time-vector is", len(time_list))
        print(count_value_error, "(", round(100 * (count_value_error / len(spread_rel)), 2), "%)",
              "value errors were counted when calculating Roll-spreads")
        print(count_corr_below, "correlations below threshold(", corr_threshold, ") were counted(",
              round(100 * (count_corr_below / len(spread_rel)), 2), "%)")

        return spread, spread_rel, time_list, count_value_error