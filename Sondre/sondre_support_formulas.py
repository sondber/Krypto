import csv
import math
import os
from datetime import date

import numpy as np

import linreg

#os.chdir("/Users/sondre/Documents/GitHub/krypto")


def final_three_rows(print_rows, n_obs_array, rsquared_array, aic_array, n_cols, n_rows, double_cols=0):
    # Dette fikser de tre nedreste radene

    for c in range(0, n_cols):
        n_obs = str(int(n_obs_array[c]))
        r2 = "{0:.3f}".format(rsquared_array[c])

        if aic_array[c] > 0:
            aic = str(int(aic_array[c]))
        else:
            aic = "$-$" + str(int(abs(aic_array[c])))

        print_rows[n_rows - 3] += "   " + n_obs
        for i in range(8-len(n_obs)):
            print_rows[n_rows - 3] += " "
        print_rows[n_rows - 3] += "&"

        print_rows[n_rows - 2] += "   " + r2
        for i in range(8-len(r2)):
            print_rows[n_rows - 2] += " "
        print_rows[n_rows - 2] += "&"

        print_rows[n_rows - 1] += " " + aic

        for i in range(10-len(aic)):
            print_rows[n_rows - 1] += " "
        print_rows[n_rows - 1] += "&"

        if c % 2 == 1:
            if double_cols == 1:
                print_rows[n_rows - 3] += " &"
                print_rows[n_rows - 2] += " &"
                print_rows[n_rows - 1] += " &"

    return print_rows

def final_print_regressions_latex(print_rows):
    tightness = 1 #
    t_string = "[-" + str(tightness) + "ex]"

    for i in range(0, len(print_rows)):
        count = 0
        while (print_rows[i][len(print_rows[i]) - 1] == " " or print_rows[i][
                len(print_rows[i]) - 1] == "&") and count < 10:
            print_rows[i] = print_rows[i][0:len(print_rows[i]) - 1]
            count += 1
        if i == len(print_rows) - 3:
            print("        \\hline")
        if i < len(print_rows) - 3:
            if i % 2 == 0:
                print(print_rows[
                          i] + "  \\\\" + t_string)  # Fjerner det siste &-tegnet og legger til backslash og tightness
            else:
                print(print_rows[i] + "  \\\\")  # Fjerner det siste &-tegnet og legger til backslash
        else:
            print(print_rows[i] + "  \\\\" + "[-0.5ex]")  # Fjerner det siste &-tegnet og legger til backslash
    print()
    print()

def read_single_exc_csvs(file_name, time_list, price, volume):
    with open(file_name, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=';', quotechar='|')
        print("\033[0;32;0m Reading file '%s'...\033[0;0;0m" % file_name)
        i = 0
        next(reader)
        for row in reader:
            try:
                time_list.append(row[0])
                price.append(float(row[7]))
                volume.append(float(row[5]))
            except ValueError:
                print("\033[0;31;0m There was an error on row %i in '%s'\033[0;0;0m" % (i + 1, file_name))
            i = i + 1
        return time_list, price, volume


def fill_blanks(in_list):
    out_list = in_list
    n = len(in_list)
    startlim = 60  # How many minutes of zero at the beginning of the list do we allow? i.e. if there is more than startlim zeros, we let them stay zero
    for i in range(0, n):
        try:
            if in_list[i] == 0:
                if i == 0:
                    j = 0
                    while in_list[j] == 0 and j < startlim:
                        j = j + 1
                    out_list[0] = in_list[j]
                else:
                    out_list[i] = in_list[i - 1]
        except IndexError:
            out_list[i] = in_list[i - 1]
            print("\033[0;31;0mThere was a problem on row %i \033[0;0;0m" % i)
    return out_list


def fix_time_list(time_list, move_n_hours=0):
    day = []
    month = []
    year = []
    hour = []
    minute = []
    for i in range(0, len(time_list)):
        day.append(int(time_list[i][0:2]))
        month.append(int(time_list[i][3:5]))
        year.append(int(time_list[i][6:10]))
        hour.append(int(time_list[i][11:13]))
        minute.append(int(time_list[i][14:16]))

    if move_n_hours < 0:
        n = -move_n_hours
        for i in range(0, len(time_list)):
            if hour[i] >= n:
                hour[i] -= n
            else:
                hour[i] = 24 - n + hour[i]
                if day[i] >= 2:
                    day[i] -= 1
                else:  # I use "mo" and "y" for brevity, and let the long version be assigned at the end
                    if month[i] == 1:
                        mo = 12
                        y = year[i] - 1
                    else:
                        mo = month[i] - 1
                        y = year[i]
                    if mo == 1 or mo == 3 or mo == 5 or mo == 7 or mo == 8 or mo == 10 or mo == 12:
                        n_days = 31
                    elif mo == 2:
                        if y % 4 == 0:
                            n_days = 29
                        else:
                            n_days = 28
                    else:
                        n_days = 30
                    day[i] = n_days
                    month[i] = mo
                    year[i] = y
    elif move_n_hours > 0:
        n = move_n_hours
        for i in range(0, len(time_list)):
            if hour[i] <= 23 - n:
                hour[i] += n
            else:
                hour[i] = n + (hour[i] - 24)

                mo = month[i]
                y = year[i]
                if mo == 1 or mo == 3 or mo == 5 or mo == 7 or mo == 8 or mo == 10 or mo == 12:
                    n_days = 31
                elif mo == 2:
                    if y % 4 == 0:
                        n_days = 29
                    else:
                        n_days = 28
                else:
                    n_days = 30

                if day[i] < n_days:
                    day[i] += 1
                else:
                    day[i] = 1
                    if mo == 12:
                        month[i] = 1
                        year[i] += 1
                    else:
                        month[i] += 1

    return year, month, day, hour, minute


def make_time_list(year, month, day, hour, minute):
    time_list_out = []
    for i in range(len(minute)):
        stamp = ""
        d = day[i]
        m = month[i]
        y = year[i]
        h = hour[i]
        mi = minute[i]

        if d < 10:
            stamp += "0" + str(d)
        else:
            stamp += str(d)
        stamp += "."
        if m < 10:
            stamp += "0" + str(m)
        else:
            stamp += str(m)
        stamp += "."
        stamp += str(y)
        stamp += " "
        if h < 10:
            stamp += "0" + str(h)
        else:
            stamp += str(h)
        stamp += ":"
        if mi < 10:
            stamp += "0" + str(mi)
        else:
            stamp += str(mi)

        time_list_out.append(stamp)
    return time_list_out

def data_analysis(in_list, number_of_intervals):
    b = number_of_intervals
    interval = max(in_list) / b
    print("With an interval size of %0.1f" % interval)
    int_count = np.zeros(b)
    maximum = max(in_list)
    print("The highest value in the dataset is = " + str(max(in_list)))
    print()
    lower = 0
    upper = interval
    i = 0

    while lower <= maximum:
        int_count[i] = (sum(float(num) <= upper for num in in_list)) - (sum(float(num) <= lower for num in in_list))
        print("There are %i minutes with values between %0.1f and %0.1f" % (int_count[i], lower, upper))
        lower = lower + interval
        upper = upper + interval
        i = i + 1
    int_count[0] = int_count[0] + (sum(float(num) == 0 for num in in_list))  # include the minutes with no trading


def moving_variance(price, mins_rolling):
    returns = logreturn(price)
    var = np.zeros(len(price))
    rolling_list = np.zeros(mins_rolling)  # rolling list
    for k in range(mins_rolling):
        rolling_list[k] = returns[k]
    var[mins_rolling - 1] = np.var(rolling_list)
    for i in range(len(returns) - mins_rolling + 1):
        j = mins_rolling + i - 1
        rolling_list[j % mins_rolling] = returns[j]
        var[j] = np.var(rolling_list)
        if i % 100000 == 0 and i != 0:
            perc = str(round(100 * i / len(price), 2)) + "%"
            print("%s" % perc)
    print("100%")
    return var


def logreturn(price):
    returnlist = np.zeros(len(price))
    for i in range(1, len(price)):
        try:
            returnlist[i] = math.log(price[i]) - math.log(price[i - 1])
        except ValueError:
            returnlist[i] = 0
    return returnlist


def make_totals(volumes, prices):  # Has to be all in USD
    print("Generating totals..")
    num_exchanges = np.size(volumes, 0)
    entries = np.size(volumes, 1)
    total_volume = np.zeros(entries)
    total_price = np.zeros(entries)
    for i in range(0, entries):
        total_volume[i] = sum(volumes[:, i])
        if total_volume[i] == 0:
            total_price[i] = total_price[i - 1]
        else:
            for j in range(0, num_exchanges):
                total_price[i] = (prices[j, i] * volumes[j, i]) + total_price[i]
            total_price[i] = float(total_price[i]) / float(total_volume[i])
    if total_price[0] == 0:
        r = 0
        while total_price[r] == 0:
            r = r + 1
        while r > 0:
            total_price[r - 1] = total_price[r]
            r = r - 1
    return total_volume, total_price


def convert_currencies(exchanges, prices):
    print("Converting currencies...")
    currency_handle = []
    for i in range(0, len(exchanges)):
        exc_name = exchanges[i]
        currency_handle.append(exc_name[len(exc_name) - 3: len(exc_name)])

    # her må vi legge inn valutakurser per dag/time/minutt og konvertere ordentlig. Dette er jalla som faen
    for i in range(0, len(exchanges)):
        if currency_handle[i] == "jpy":
            prices[i, :] = prices[i, :] / 112
        elif currency_handle[i] == "cny":
            prices[i, :] = prices[i, :] / 6.62
        elif currency_handle[i] == "eur":
            prices[i, :] = prices[i, :] * 1.19

    print("All prices converted to USD")
    prices_in_usd = prices
    return prices_in_usd


def write_to_raw_file(volumes, prices, time_list, exchanges, filename):
    n_exc = len(exchanges)
    print("Exporting data to csv-file...")
    with open(filename, 'w', newline='') as csvfile:
        writ = csv.writer(csvfile, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        n_rows = np.size(volumes, 1)

        header1 = [" "]
        header2 = [" "]
        header3 = ["Time"]
        for exc in exchanges:
            currency = exc[len(exc) - 3: len(exc)]
            header1.append(exc)
            header1.append("")
            header2.append("Price")
            header2.append("Volume")
            header3.append(currency.upper())
            header3.append("BTC")

        writ.writerow(header1)
        writ.writerow(header2)
        writ.writerow(header3)
        for i in range(0, n_rows):
            rowdata = [time_list[i]]
            for j in range(0, n_exc):
                rowdata.append(prices[j, i])
                rowdata.append(volumes[j, i])
            writ.writerow(rowdata)
    print("Export to aggregate csv \033[33;0;0m'%s'\033[0;0;0m successful" % filename)


def fetch_aggregate_csv(file_name, n_exc):
    n_rows = count_rows(file_name)
    n_exc = int(n_exc)
    print("\033[0;32;0m Reading file '%s'...\033[0;0;0m" % file_name)
    with open(file_name, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=';', quotechar='|')
        i = 0
        time_list = []
        prices = np.zeros([n_exc, n_rows - 3])  # minus tre for å ikke få med headere
        volumes = np.zeros([n_exc, n_rows - 3])  # minus tre for å ikke få med headere
        next(reader)
        next(reader)
        next(reader)
        for row in reader:
            time_list.append(row[0])
            for j in range(0, n_exc):
                prices[j, i] = row[1 + 2 * j]
                volumes[j, i] = row[2 + 2 * j]
            i = i + 1
    return time_list, prices, volumes


def count_rows(file_name):
    with open(file_name, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=';', quotechar='|')
        n_rows = 0
        for row in reader:
            n_rows = n_rows + 1
        n_rows = int(n_rows)
    return n_rows


def get_ticks(time_list, number_of_ticks):
    n = number_of_ticks
    n_mins = len(time_list)
    x = np.arange(0, n_mins + 1, n_mins / (n - 1))
    myticks = []
    for i in range(0, n + 1):
        time_row = min(int((n_mins / (n - 1)) * i), n_mins - 1)
        timestamp = time_list[time_row]
        timestamp = timestamp[0:10]
        myticks.append(timestamp)
    return x, myticks


def get_rolls():
    file_name = "data/export_csv/relative_spreads_hourly.csv"
    rolls = []
    time_list = []
    with open(file_name, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=';', quotechar='|')
        print("\033[0;32;0m Reading file '%s'...\033[0;0;0m" % file_name)
        i = 0
        next(reader)
        for row in reader:
            try:
                time_list.append(row[0])
            except ValueError:
                print("\033[0;31;0m There was an error on row %i in '%s'\033[0;0;0m" % (i + 1, file_name))
            try:
                rolls.append(float(row[1]))
            except ValueError:
                rolls.append(0)
            i = i + 1
        return time_list, rolls


def remove_list1_zeros_from_all_lists(time_list, time_list_removed_previous, list1, list2=[], list3=[], list4=[],
                                      list5=[], list6=[]):
    # threshold is in number of standard deviations
    # only chekcs for positive deviations
    t_list2 = False
    t_list3 = False
    t_list4 = False
    t_list5 = False
    t_list6 = False
    if len(list2) > 1:
        t_list2 = True
    if len(list3) > 1:
        t_list3 = True
    if len(list4) > 1:
        t_list4 = True
    if len(list5) > 1:
        t_list5 = True
    if len(list6) > 1:
        t_list6 = True

    time_list_removed = time_list_removed_previous  # from previous
    time_list_out = []
    n_in = len(list1)
    out_list1 = []
    if t_list2:
        out_list2 = []
        if len(list2) != n_in:
            print("Wrong length of list2!", len(list2), "instead of", n_in)
    if t_list3:
        out_list3 = []
        if len(list3) != n_in:
            print("Wrong length of list3!", len(list3), "instead of", n_in)
    if t_list4:
        out_list4 = []
        if len(list4) != n_in:
            print("Wrong length of list4!", len(list4), "instead of", n_in)
    if t_list5:
        out_list5 = []
        if len(list5) != n_in:
            print("Wrong length of list5!", len(list5), "instead of", n_in)
    if t_list6:
        out_list6 = []
        if len(list6) != n_in:
            print("Wrong length of list6!", len(list6), "instead of", n_in)
    for i in range(0, n_in):
        if list1[i] > 0 and not math.isinf(list1[i]):
            time_list_out.append(time_list[i])
            out_list1.append(list1[i])
            if t_list2:
                out_list2.append(list2[i])
            if t_list3:
                out_list3.append(list3[i])
            if t_list4:
                out_list4.append(list4[i])
            if t_list5:
                out_list5.append(list5[i])
            if t_list6:
                out_list6.append(list6[i])
        else:
            time_list_removed.append(time_list[i])
    if t_list6:
        return time_list_out, time_list_removed, out_list1, out_list2, out_list3, out_list4, out_list5, out_list6
    elif t_list5:
        return time_list_out, time_list_removed, out_list1, out_list2, out_list3, out_list4, out_list5
    elif t_list4:
        return time_list_out, time_list_removed, out_list1, out_list2, out_list3, out_list4
    elif t_list3:
        return time_list_out, time_list_removed, out_list1, out_list2, out_list3
    elif t_list2:
        return time_list_out, time_list_removed, out_list1, out_list2
    else:
        return time_list_out, time_list_removed, out_list1


def autocorr(in_list, lag):
    n = len(in_list)
    list1 = in_list[0: n - lag]
    list2 = in_list[lag: n]
    corr = np.corrcoef(list1, list2)[0, 1]
    return corr


def mean_for_n_entries(in_list, n_lag):
    n_in = len(in_list)
    out_list = np.zeros(n_in - n_lag)
    initial_mean = np.mean(in_list[0:n_lag])
    out_list[0] = initial_mean
    for i in range(1, n_lag):
        out_list[i] = (initial_mean * (n_lag - i) + i * np.mean(in_list[n_lag - 1:n_lag - 1 + i])) / (n_lag - 1)
    for i in range(n_lag, n_in - n_lag):
        out_list[i] = np.mean(in_list[i: i + n_lag])
    return out_list


def standardize(in_list):
    mean = np.mean(in_list)
    out_list = in_list - mean
    std = np.std(in_list)
    out_list = np.divide(out_list, std)

    return out_list


def week_vars(time_list, move_n_hours=0):
    year, month, day, hour, minute = fix_time_list(time_list, move_n_hours=move_n_hours)
    n_entries = len(time_list)

    mon = np.zeros(n_entries)
    tue = np.zeros(n_entries)
    wed = np.zeros(n_entries)
    thu = np.zeros(n_entries)
    fri = np.zeros(n_entries)
    sat = np.zeros(n_entries)
    sun = np.zeros(n_entries)
    day_string = []
    for i in range(0, n_entries):
        daynum = int(date(year[i], month[i], day[i]).isoweekday()) - 1
        if daynum == 0:
            mon[i] = 1
        elif daynum == 1:
            tue[i] = 1
        elif daynum == 2:
            wed[i] = 1
        elif daynum == 3:
            thu[i] = 1
        elif daynum == 4:
            fri[i] = 1
        elif daynum == 5:
            sat[i] = 1
        elif daynum == 6:
            sun[i] = 1
    return mon, tue, wed, thu, fri, sat, sun


def import_to_matrices(m_col, coeffs, std_errs, p_values, rsquared, aic, n_obs, coeff_matrix,
                       std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array):
    for j in range(0, len(coeffs)):
        coeff_matrix[j, m_col] = coeffs[j]
        std_errs_matrix[j, m_col] = std_errs[j]
        p_values_matrix[j, m_col] = p_values[j]
    rsquared_array[m_col] = rsquared
    aic_array[m_col] = aic
    n_obs_array[m_col] = n_obs
    return coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array


def print_n(n):
    for k in range(n + 1):
        print()


def import_regressions(m_col, Y, X, coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array,
                       n_obs_array, prints=0, intercept=1):
    coeffs, tvalues, rsquared, aic, p_values, std_errs, n_obs = linreg.reg_multiple(Y, X, intercept=intercept,
                                                                                    prints=prints)
    coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array = \
        import_to_matrices(m_col, coeffs, std_errs, p_values, rsquared, aic, n_obs, coeff_matrix,
                           std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array)
    m_col += 1
    return m_col, coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array


def fmt_print(print_loc, data, p_value=1, type="coeff"):
    if type == "coeff":
        if data >= 0:
            print_loc += "   "
        else:
            print_loc += "$-$"

        if abs(data) < 10:
            print_loc += "{0:.4f}".format(abs(data))
        else:
            print_loc += "{0:.3f}".format(abs(data))

        if p_value <= 0.01:
            stars = "**"
        elif p_value <= 0.05:
            stars = "* "
        else:
            stars = "  "
        print_loc += stars + "&"

    elif type == "std_err":
        print_loc += "  (" + str("{0:.3f}".format(data)) + ")" + "  &"
    else:
        pass

    return print_loc


def remove_extremes(time_list, data, threshold_upper, threshold_lower=0):
    for i in range(len(data)):
        if data[i] > threshold_upper or data[i] < threshold_lower:
            time_list.append(i)
    return time_list
