import math
from Sondre import sondre_support_formulas as supp
import time

def spread_calc(alpha):
    numerator = 2 * (math.exp(alpha) - 1)
    denominator = 1 + math.exp(alpha)
    return numerator / denominator


def alpha_calc(beta, gamma):
    first_numerator = math.sqrt(2 * beta) - math.sqrt(beta)
    first_denom = 3 - 2 * math.sqrt(2)
    first = first_numerator / first_denom

    second_numerator = gamma
    second_denom = 3 - 2 * math.sqrt(2)
    second = math.sqrt(second_numerator / second_denom)

    return first - second


def gamma_calc(high_two, low_two):  # to implement: check for 0s
    if high_two == 0:
        return 0
    elif low_two == 0:
        return 0
    elif high_two == low_two:
        return 0
    else:
        return (math.log(high_two / low_two)) ** 2


def beta_calc(two_highs, two_lows):  # two lists of two prices each
    total = 0
    for i in range(2):
<<<<<<< HEAD
        if gamma_calc(two_highs[i],two_lows[i]) == 0:
            return 0
        else:
            total = total + gamma_calc(two_highs[i], two_lows[i])
    return total
=======
        try:
            total = total + gamma_calc(two_highs[i], two_lows[i])
        except IndexError:
            print("total:", total)
            print("highs:", two_highs)
            print("lows:", two_lows)
            print("i:", i)

    return total  # should this be divided by two? I dont think so
>>>>>>> master


def determine_hilo(two_highs, two_lows):
    high = max(two_highs)
    low = min(two_lows)
    return high, low


def hi_lo_spread(timestamps, highs, lows, prices,
                 kill_output=0, hour_yesno=0):  # returns daily spreads, spread is set to zero if lack of data (as with rolls). hour=1 if houry data
    year, month, day, hour, minute = supp.fix_time_list(timestamps)

    spreads = []
    time_list = []
    rel_spreads = []
    value_errors = 0
    na_spread = 0

    freq_desc = "daily"
    if hour_yesno == 0:
        resolution_desc = "minute"
    else:
        resolution_desc = "hour"

    n = len(highs)  # number of minutes in dataset
    # determine trading day yes/no
    if hour[0] == 0:  # this indicates that full day is being investigated
        hours_in_day = 24
        if hour_yesno == 0:
            window = int(hours_in_day * 60)
        else:
            window = int(hours_in_day)
        day_desc = "full day"
    else:
        hours_in_day = 6.5
        day_desc = "trading day"
        if hour_yesno == 0:
            window = int(hours_in_day * 60)
        else:
            window = int(hours_in_day+0.5)

    if kill_output == 0:
        print("Calculating Hi/Lo-spread on a/an", freq_desc, "basis using", day_desc, "data, with", resolution_desc)

    for i in range(0, n, window):  # iterates through days
        partsum = 0  # for averaging
        averager_adjusted = window - 1
        for j in range(i, i + window - 1):  # iterates through minutes in day
<<<<<<< HEAD
            two_highs = highs[i:i + 2]
            two_lows = lows[i:i + 2]
=======
            two_highs = highs[i:i + 2]  # endret denne fra 1 til 2 (09.02.18)
            two_lows = lows[i:i + 2]  # endret denne fra 1 til 2 (09.02.18)
>>>>>>> master
            high_two = determine_hilo(two_highs, two_lows)[0]
            low_two = determine_hilo(two_highs, two_lows)[1]
            gamma = gamma_calc(high_two, low_two)
            if gamma == 0:
                value_errors += 1
                averager_adjusted -= 1
            else:
                beta = beta_calc(two_highs, two_lows)
                if beta == 0:
                    value_errors += 1
                    averager_adjusted -= 1
                else:
                    alpha = alpha_calc(beta, gamma)
                    spread = spread_calc(alpha)
                    if spread < 0:
                        spread = 0
                    partsum += spread
        if averager_adjusted == 0:
            na_spread += 1
            spreads.append(0)
            rel_spreads.append(0)
            time_list.append(timestamps[i])
        else:
            spread_averaged = partsum / averager_adjusted
            spreads.append(spread_averaged)
            rel_spreads.append(spread_averaged/prices[i+window-1])
            time_list.append(timestamps[i])

    if kill_output == 0:
        print("Hi/Low spread-calculation is finished")
        print("The length of the spread-vector is", len(spreads))
        print("The length of the time-vector is", len(time_list))
        print("The length of the relative spread-vector is", len(rel_spreads))
        print("Number of value errors:", value_errors)
        print("Number of days set to zero due to lack of data:", na_spread)

    return time_list, spreads, rel_spreads


