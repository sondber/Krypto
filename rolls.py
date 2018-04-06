import math
from Sondre import sondre_support_formulas as supp
import numpy as np
import linreg
import time


def first_price_differences(prices):  # takes list of prices, returnsH equal length list of first price differences
    returnlist = [float(0)]
    for i in range(1, len(prices)):  # check the logic of setting first index to zero in relation to return calculation
        try:
            returnlist.append(prices[i] - prices[(i - 1)])
        except ValueError:
            returnlist.append(float(0))
            print("Something wrong happened when calculating price difference")
    return returnlist


def rolls(prices_minute, time_list_minute, calc_basis="h", kill_output=0, bias_indicator = 0):  # calc_basis "h"/"d"
    year, month, day, hour, minute = supp.fix_time_list(time_list_minute)  # gives 5 equal length lists

    spread = []
    spread_rel = []
    time_list = []

    count_value_error = 0

    bias_indicator_list = []

    if kill_output == 0:
        print("Calculating first price differences ...")

    price_differences = first_price_differences(prices_minute)  # calculates price difference

    if kill_output == 0:
        print("Price differences-calculation finished. ")

    # determine minutes_in_window based on calc_basis
    if calc_basis == "h" or calc_basis == 0:  # hourly
        minutes_in_window = 60
        freq_desc = "hourly"
    else:  # daily with full data
        minutes_in_window = 60 * 24
        freq_desc = "daily"

    if kill_output == 0:
        print("Calculating spreads on a/an", freq_desc, "basis")

    # calculation
    if calc_basis == "h" or calc_basis == 0:  # calculating on hourly basis
        sum_inside = 0
        for i in range(0, len(price_differences), minutes_in_window):
            for y in range(i + 1, i + minutes_in_window):
                try:
                    sum_inside += (price_differences[y] * price_differences[y - 1])
                except IndexError:
                    print("There is an error when i = %i and y = %i" %(i, y))
            try:
                ba_calc = 2 * math.sqrt(-sum_inside / (minutes_in_window - 2))
                bias_indicator_list.append(0)
            except ValueError:
                count_value_error += 1
                ba_calc = 0
                bias_indicator_list.append(1)
            spread.append(ba_calc)
            time_list.append(time_list_minute[i])
            spread_rel.append(ba_calc / prices_minute[i + minutes_in_window - 1])
            sum_inside = 0
    elif calc_basis == "d" or calc_basis == 1:  # calculating on daily basis
        sum_inside = 0
        start_index = 0
        if hour[0] != 0:  # first day if not starting midnight
            start_index = (24*60) - (hour[0] * 60)
            for j in range(1, start_index):
                sum_inside += (price_differences[j] * price_differences[j - 1])
            try:
                ba_calc = 2 * math.sqrt(-sum_inside / (start_index - 2))
                bias_indicator_list.append(0)
            except ValueError:
                count_value_error += 1
                ba_calc = 0
                bias_indicator_list.append(1)
            spread.append(ba_calc)
            time_list.append(time_list_minute[0])
            spread_rel.append(ba_calc / prices_minute[start_index - 1])
            sum_inside = 0
        for i in range(start_index, min(len(price_differences), len(price_differences)-hour[0]*60), minutes_in_window):  # rest of days except overshooting
            for y in range(i + 1, i + minutes_in_window):
                sum_inside += price_differences[y] * price_differences[y - 1]
            try:
                ba_calc = 2 * math.sqrt(-sum_inside / (minutes_in_window - 2))
                bias_indicator_list.append(0)
            except ValueError:
                count_value_error += 1
                ba_calc = 0
                bias_indicator_list.append(1)
            spread.append(ba_calc)
            time_list.append(time_list_minute[i])
            spread_rel.append(ba_calc / prices_minute[i + minutes_in_window - 1])
            sum_inside = 0

    if kill_output == 0:
        print("Spreads-calculation is finished")
        print("The length of the spreadH-vector is", len(spread_rel))
        print("The length of the time-vector is", len(time_list))
        print(count_value_error, "(", round(100 * (count_value_error / len(spread_rel)), 2), "%)",
              "value errors were counted when calculating Roll-spreads")
        count_value_error = round(100 * (count_value_error / len(spread_rel)), 2)

    if bias_indicator == 1:
        return spread, spread_rel, time_list, count_value_error, bias_indicator_list
    else:
        return spread, spread_rel, time_list, count_value_error
