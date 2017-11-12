import csv
import numpy as np
import math


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
                print("\033[0;31;0m There was an error on row %i in '%s'\033[0;0;0m" % (i+1, file_name))
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


def fix_time_list(time_list):
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
    return year, month, day, hour, minute


def average_at_time_of_day(in_list):
    avg_per_min = np.zeros(24*60)
    mintcount = 0

    for i in range(0, len(in_list)):
        avg_per_min[mintcount] = avg_per_min[mintcount] + in_list[i]
        if mintcount == 1439:
            mintcount = 0
        else:
            mintcount = mintcount + 1
    avg_per_min = avg_per_min/(len(in_list)/(24 * 60))
    return avg_per_min


def data_analysis(in_list, number_of_intervals):
    b = number_of_intervals
    interval = max(in_list)/b
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
            perc = str(round(100*i/len(price), 2)) + "%"
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
        currency_handle.append(exc_name[len(exc_name)-3: len(exc_name)])

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
            currency = exc[len(exc)-3: len(exc)]
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
                prices[j, i] = row[1+2*j]
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
                print("\033[0;31;0m There was an error on row %i in '%s'\033[0;0;0m" % (i+1, file_name))
            try:
                rolls.append(float(row[1]))
            except ValueError:
                rolls.append(0)
            i = i + 1
        return time_list, rolls


def remove_list1_outliers_from_all_lists(list1, list2=[], list3=[], list4=[], threshold=2):
    # threshold is in number of standard deviations
    # only chekcs for positive deviations
    t_list2 = False
    t_list3 = False
    t_list4 = False
    if len(list2) > 1:
        t_list2 = True
    if len(list3) > 1:
        t_list3 = True
    if len(list4) > 1:
        t_list4 = True

    n_in = len(list1)
    std = np.std(list1)
    mean = np.mean(list1)
    list1_min = mean - threshold * std
    list1_max = mean + threshold * std
    out_list1 = []
    if t_list2:
        out_list2 = []
    if t_list3:
        out_list3 = []
    if t_list4:
        out_list4 = []
    for i in range(0, n_in):
        if list1[i] < list1_max:
            out_list1.append(list1[i])
            if t_list2:
                out_list2.append(list2[i])
            if t_list3:
                out_list3.append(list3[i])
            if t_list4:
                out_list4.append(list4[i])
    if t_list4:
        return out_list1, out_list2, out_list3, out_list4
    elif t_list3:
        return out_list1, out_list2, out_list3
    elif t_list2:
        return out_list1, out_list2
    else:
        return out_list1


def remove_list1_zeros_from_all_lists(time_list, time_list_removed_previous, list1, list2=[], list3=[], list4=[], list5=[]):
    # threshold is in number of standard deviations
    # only chekcs for positive deviations
    t_list2 = False
    t_list3 = False
    t_list4 = False
    t_list5 = False
    if len(list2) > 1:
        t_list2 = True
    if len(list3) > 1:
        t_list3 = True
    if len(list4) > 1:
        t_list4 = True
    if len(list5) > 1:
        t_list5 = True

    time_list_removed = time_list_removed_previous # from previous
    time_list_out = []
    n_in = len(list1)
    out_list1= []
    if t_list2:
        out_list2 = []
    if t_list3:
        out_list3 = []
    if t_list4:
        out_list4 = []
    if t_list5:
        out_list5 = []
    for i in range(0, n_in):
        if list1[i] != 0:
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
        else:
            time_list_removed.append(time_list[i])
    if t_list5:
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
    list1 = in_list[0 : n - lag]
    list2 = in_list[lag : n]
    corr = np.corrcoef(list1, list2)[0, 1]
    return corr

def mean_for_n_entries(in_list, n_lag):
    n_in = len(in_list)
    out_list = np.zeros(n_in - n_lag)
    initial_mean = np.mean(in_list[0:n_lag])
    out_list[0] = initial_mean
    for i in range(1, n_lag):
        out_list[i] = (initial_mean * (n_lag - i) + i * np.mean(in_list[n_lag - 1:n_lag - 1 + i]))/(n_lag-1)
    for i in range(n_lag, n_in - n_lag):
        out_list[i] =  np.mean(in_list[i: i + n_lag])
    return out_list