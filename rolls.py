import math
from Sondre import sondre_support_formulas as supp
import numpy as np
import linreg


# SISTE NYE FRA JACOB 16/11
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


def rolls(prices_minute, time_list_minute, calc_basis=0, kill_output=0):  # calc_basis 0/1 hour/day
    year, month, day, hour, minute = supp.fix_time_list(time_list_minute)

    spread = []
    spread_rel = []
    time_list = []
    count_value_error = 0
    count_corr_below = 0
    alpha_count_below = 0
    corr_threshold = 0.2
    alpha = 0.05
    if kill_output == 0:
        print("Calculating first price differences ...")
    price_differences = first_price_differences(prices_minute)  # calculates price difference
    if kill_output == 0:
        print("Price differences-calculation finished. ")

    """
    # determine opening hours yes/no
    if hour[0] == 14:  # this indicates that opening times are being investigated
        opening_times = 1
        opening_hours_desc = "opening hours"
    else:
        opening_times = 0
        opening_hours_desc = "full day"
    """

    # determine minutes_in_window based on calc_basis
    if calc_basis == 0:  # hourly with full data
        minutes_in_window = 60
        freq_desc = "hourly"
    else:  # daily with full data
        minutes_in_window = 60 * 24
        freq_desc = "daily"

    if kill_output == 0:
        print("Calculating spreads on a/an", freq_desc, "basis")

    # calculation

    if calc_basis == 1:
        if hour[0] == 0:
            start_index = 0
        else:
            start_index = hour[0]*60  # this is for the continued calc after day 1

            minutes_in_window_day1 = (24 - hour[0]) * 60
            sum_inside = 0
            #list1 = price_differences[0:minutes_in_window_day1 - 1]
            #list2 = price_differences[1:minutes_in_window_day1]
            #corr = np.corrcoef(list1, list2)[0, 1]
            #p_val = linreg.linreg_coeffs(list1, list2)[3]
            #if abs(corr) < corr_threshold:
            #    count_corr_below += 1

            for y in range(1, minutes_in_window_day1):
                sum_inside = sum_inside + (price_differences[y] * price_differences[y - 1])
            try:
                ba_calc = 2 * math.sqrt(-sum_inside / (minutes_in_window_day1 - 2))
            except ValueError:
                count_value_error += 1
                ba_calc = 0
                if p_val < alpha:
                    alpha_count_below += 1
            spread.append(ba_calc)
            time_list.append(time_list_minute[0])
            spread_rel.append(ba_calc / prices_minute[minutes_in_window_day1 - 1])
    else:
        start_index = 0

    sum_inside = 0
    for i in range(start_index, len(price_differences),
                   minutes_in_window):
        #list1 = price_differences[i:i + minutes_in_window - 1]
        #list2 = price_differences[i + 1:i + minutes_in_window]
        #corr = np.corrcoef(list1, list2)[0, 1]
        #p_val = linreg.linreg_coeffs(list1, list2)[3]
        #if abs(corr) < corr_threshold:
        #    count_corr_below += 1

        for y in range(i + 1, min(i + minutes_in_window, len(time_list_minute))):
            sum_inside = sum_inside + (price_differences[y] * price_differences[y - 1])
        try:
            ba_calc = 2 * math.sqrt(-sum_inside / (minutes_in_window - 2))
        except ValueError:
            count_value_error += 1
            ba_calc = 0
            if p_val < alpha:
                alpha_count_below += 1
        spread.append(ba_calc)
        time_list.append(time_list_minute[i])
        spread_rel.append(ba_calc / prices_minute[i + minutes_in_window - 1])
        sum_inside = 0

    # results

    if kill_output == 0:
        print("Spreads-calculation is finished")
        print("The length of the spread-vector is", len(spread_rel))
        print("The length of the time-vector is", len(time_list))
        print(count_value_error, "(", round(100 * (count_value_error / len(spread_rel)), 2), "%)",
              "value errors were counted when calculating Roll-spreads")
        print(count_corr_below, "correlations below threshold(", corr_threshold, ") were counted(",
              round(100 * (count_corr_below / len(spread_rel)), 2), "%)")
        #print(alpha_count_below, "of the  value-error correlations were  significantly different from zero at the",
        #      round(100 * alpha, 0), "% level(",
        #      round(100 * alpha_count_below / count_value_error, 1), "%)")

    return spread, spread_rel, time_list, count_value_error
