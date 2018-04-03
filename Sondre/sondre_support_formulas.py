import csv
import math
import time
from datetime import datetime
from inspect import currentframe as cf, getframeinfo as gf

import numpy as np


def fill_blanks(in_list):
    out_list = in_list
    n = len(in_list)
    startlim = 100000  # How many minutes of zero at the beginning of the list do we allow? i.e. if there is more than startlim zeros, we let them stay zero
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


def move_time_list(year, month, day, hour, minute, move_n_hours=0, single_time_stamp=0):
    if single_time_stamp == 1:
        if move_n_hours < 0:  # Funker ikke for single_time_stamp
            n = -move_n_hours
            if hour >= n:
                hour -= n
            else:
                hour = 24 - n + hour
                if day >= 2:
                    day -= 1
                else:  # I use "mo" and "y" for brevity, and let the long version be assigned at the end
                    if month == 1:
                        mo = 12
                        y = year - 1
                    else:
                        mo = month - 1
                        y = year
                    if mo == 1 or mo == 3 or mo == 5 or mo == 7 or mo == 8 or mo == 10 or mo == 12:
                        n_days = 31
                    elif mo == 2:
                        if y % 4 == 0:
                            n_days = 29
                        else:
                            n_days = 28
                    else:
                        n_days = 30
                    day = n_days
                    month = mo
                    year = y
        elif move_n_hours > 0:
            n = move_n_hours
            if hour <= 23 - n:
                hour += n
            else:
                hour = n + (hour - 24)
                mo = month
                y = year
                if mo == 1 or mo == 3 or mo == 5 or mo == 7 or mo == 8 or mo == 10 or mo == 12:
                    n_days = 31
                elif mo == 2:
                    if y % 4 == 0:
                        n_days = 29
                    else:
                        n_days = 28
                else:
                    n_days = 30

                if day < n_days:
                    day += 1
                else:
                    day = 1
                    if mo == 12:
                        month = 1
                        year += 1
                    else:
                        month += 1
    else:
        n_entries = len(year)
        if move_n_hours < 0:  # Funker ikke for single_time_stamp
            n = -move_n_hours
            extra_day = 0
            while n > 24:
                n -= 24
                extra_day += 1

            for i in range(0, n_entries):
                n_days = day[i]
                mo = month[i]
                y = year[i]
                if hour[i] >= n:
                    hour[i] -= n
                else:
                    hour[i] = 24 + hour[i] - n
                    if n_days >= 2:
                        n_days -= 1
                    else:  # I use "mo" and "y" for brevity, and let the long version be assigned at the end
                        if mo == 1:
                            mo = 12
                            y -= 1
                        else:
                            mo -= 1
                            y = y
                        if mo == 1 or mo == 3 or mo == 5 or mo == 7 or mo == 8 or mo == 10 or mo == 12:
                            n_days = 31
                        elif mo == 2:
                            if y % 4 == 0:
                                n_days = 29
                            else:
                                n_days = 28
                        else:
                            n_days = 30
                    #FIRST ITERATION DONE BASED ON HOUR ONLY
                    #NOW REMOWING EXTRA DAYS
                for k in range(0, extra_day):
                    if n_days >= 2:
                        n_days -= 1
                    else:  # I use "mo" and "y" for brevity, and let the long version be assigned at the end
                        if mo == 1:
                            mo = 12
                            y -= 1
                        else:
                            mo -= 1
                            y = y
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
            for i in range(0, n_entries):
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


def fix_time_list(time_list, move_n_hours=0, single_time_stamp=0):
    day = []
    month = []
    year = []
    hour = []
    minute = []
    if single_time_stamp == 0:
        for i in range(0, len(time_list)):
            day.append(int(time_list[i][0:2]))
            month.append(int(time_list[i][3:5]))
            year.append(int(time_list[i][6:10]))
            hour.append(int(time_list[i][11:13]))
            minute.append(int(time_list[i][14:16]))

    else:
        day = (int(time_list[0:2]))
        month = (int(time_list[3:5]))
        year = (int(time_list[6:10]))
        hour = (int(time_list[11:13]))
        minute = (int(time_list[14:16]))

    if move_n_hours != 0:
        year, month, day, hour, minute = move_time_list(year, month, day, hour, minute, move_n_hours=move_n_hours,
                                                        single_time_stamp=single_time_stamp)

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
            time_list_removed = np.append(time_list_removed, time_list[i])
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


def print_n(n):
    for k in range(n + 1):
        print()


def remove_extremes(time_list, data, threshold_upper, threshold_lower=0):
    for i in range(len(data)):
        if data[i] > threshold_upper or data[i] < threshold_lower:
            time_list.append(i)
    return time_list


def find_date_index(date_to_find, time_list_hours, next_date=0):
    c_year, c_month, c_day, c_hour, c_minute = fix_time_list(date_to_find, single_time_stamp=1)
    year, month, day, hour, minute = fix_time_list(time_list_hours)

    #print("   supp.%i: searching for %s " % (gf(cf()).lineno, date_to_find))
    index = 0
    while year[index] < c_year:
        index += 1
    while month[index] < c_month:
        index += 1
    while day[index] < c_day and day[index] < 31:
        index += 1
    while hour[index] < c_hour and hour[index] < 23:
        index += 1
    while minute[index] < c_minute and minute[index] < 59:
        index += 1

    if date_to_find != time_list_hours[index]:
        if next_date == 0:
            #print("   supp.%i: Date %s not found in time list. Returning nothing" % (gf(cf()).lineno, date_to_find))
            return "Error"
        else:
            print("   supp.%i: Date %s not found in time list. Returning %s instead" % (gf(cf()).lineno, date_to_find, time_list_hours[index]))
            return index
    else:
        return index


def get_lagged_list(data, time_list, freq="h", lag=24):
    if freq != "h":
        print("FUNCTIONALITY ONLY WRITTEN FOR HOURLY FREQUENCY")

    n_entries = len(data)
    lagged_list = np.zeros(n_entries)
    index_list = np.zeros(n_entries)
    found = 0

    y, mo, d, h, mi = fix_time_list(time_list, single_time_stamp=0, move_n_hours=-lag)
    time_stamp = make_time_list(y, mo, d, h, mi)

    for i in range(len(time_stamp) - 1, -1, -1):
        for j in range(i, i - lag - 1, -1):
            if time_stamp[i] == time_list[j]:
                lagged_list[i] = data[j]
                index_list[i] = j
                found = 1
        if found == 0:
            lagged_list[i] = -1
            index_list[i] = -1
        found = 0

    return lagged_list, index_list


def get_last_day_average(data, time_list, index_list_prev_lag, freq="h", lag=24):
    partsum = 0
    n_avg = 0
    last_day_average = np.zeros(len(data))

    for i in range(0, len(data)):
        # determine starting point of averaging. If none is found, average is set to -1
        y_i, mo_i, d_i, h_i, mi_i = fix_time_list(time_list[i], single_time_stamp=1)
        timeindex_i = y_i * (365 * 31 * 24 * 60) + mo_i * (31 * 24 * 60) + d_i * (24 * 60) + h_i * 60 + mi_i
        start_point_avg = -1
        if index_list_prev_lag[i] == -1:
            for k in range(max(0, i - lag), i):
                y_k, mo_k, d_k, h_k, mi_k = fix_time_list(time_list[k], single_time_stamp=1)
                timeindex_k = y_k * (365 * 31 * 24 * 60) + mo_k * (31 * 24 * 60) + d_k * (24 * 60) + h_k * 60 + mi_k
                if timeindex_i - timeindex_k < lag * 60:
                    start_point_avg = k
                    break
        else:
            start_point_avg = int(index_list_prev_lag[i])

        if start_point_avg == -1:
                last_day_average[i] = -1
        else:
            for j in range(start_point_avg, i):
                partsum += data[j]
                n_avg += 1
            last_day_average[i] = partsum / n_avg
            partsum = 0
            n_avg = 0

    return last_day_average


def A_before_B(time_A, time_B):
    before = False
    if timestamp_to_unix(time_A) < timestamp_to_unix(time_B):
        before = True
    return before


def unix_to_timestamp(unix_stamp): #dytt inn enten unix-integer eller liste med unix-integers. returnerer én-til-én
    single = 1
    try:
        list_length = len(unix_stamp)
    except TypeError:
        list_length = 1

    if list_length > 1:
        single = 0

    if single == 1:
        timestamp = datetime.utcfromtimestamp(unix_stamp).strftime('%d.%m.%Y %H:%M')
    else:
        timestamp = []
        for i in range(list_length):
            timestamp.append(datetime.utcfromtimestamp(unix_stamp[i]).strftime('%d.%m.%Y %H:%M'))

    return timestamp


def timestamp_to_unix(time_stamp):
    unix = time.mktime(datetime.datetime.strptime(time_stamp, '%d.%m.%Y %H:%M').timetuple())
    return unix
