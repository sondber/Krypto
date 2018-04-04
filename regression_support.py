import plot
import time
import math
from inspect import getframeinfo as gf, currentframe as cf
import numpy as np
import linreg
from Sondre import sondre_support_formulas as supp
from Sondre.sondre_support_formulas import fix_time_list, make_time_list


def benchmark_hourly(Y, time_listH, HAR_config=0, hours_in_period=4, prints=1, force_max_lag=0):
    hours_to_remove = []
    if hours_in_period != -1:
        X_dummies, n_dummies = time_of_day_dummies(time_listH,
                                                   hours_in_period=hours_in_period)  # Dette gir dummy variable
        if prints == 1:
            print("  rs.%i: x1 through x%i in the benchmark are time-based dummy variables" % (
            gf(cf()).lineno, n_dummies))
    else:
        n_dummies = 0
    n_x = n_dummies

    if HAR_config == 1:
        AR_order = 1
        max_lag = max(AR_order, force_max_lag)
        X_AR, hours_to_remove = AR_matrix(Y, time_listH, AR_order, hours_to_remove)

        X_AR = X_AR[max_lag - AR_order:, :]
        hours_to_remove = adjust_hours_for_removal(hours_to_remove, n_hours=(max_lag - AR_order))
        X_HAR = X_AR

        n_x += 1
        if prints == 1:
            print(
                "  rs.%i: x%i through x%i is the X_AR(%i) model" % (gf(cf()).lineno, n_x, n_x + AR_order - 1, AR_order))

    elif HAR_config == 2:  # Denne skal inkludere AR(24)
        AR_order = 5
        max_lag = max(AR_order, force_max_lag)
        X_AR, hours_to_remove = AR_matrix(Y, time_listH, AR_order, hours_to_remove)

        print("   \033[32;0;0mrs.%i: %0.1f percent of hours removed due to AR()\033[0;0;0m" % (
        gf(cf()).lineno, 100 * float(len(hours_to_remove) / len(Y))))
        X_AR = X_AR[max_lag - AR_order:, :]
        hours_to_remove = adjust_hours_for_removal(hours_to_remove, n_hours=(max_lag - AR_order))
        X_HAR = X_AR

        n_x += 1
        if prints == 1:
            print(
                "  rs.%i: x%i through x%i is the X_AR(%i) model" % (gf(cf()).lineno, n_x, n_x + AR_order - 1, AR_order))

    elif HAR_config == 3:  # Denne skal inkludere X_AR(1) verdi 24 timer før, snitt 24 timer før
        AR_order = 1
        max_lag = max(24, force_max_lag)
        X_AR, hours_to_remove = AR_matrix(Y, time_listH, AR_order, hours_to_remove)

        print("  rs.%i: X_AR is (%i,%i)" % (gf(cf()).lineno, np.size(X_AR,0), np.size(X_AR,1)))

        #X_AR = X_AR[max_lag - AR_order:, :]  # Hvis max lag er 24, men order=1, så vil vi kutte bort 23 entries til

        print("  rs.%i: X_AR is (%i,%i)" % (gf(cf()).lineno, np.size(X_AR,0), np.size(X_AR,1)))
        #hours_to_remove = adjust_hours_for_removal(hours_to_remove, n_hours=(max_lag - AR_order))

        lagged_list, index_list_prev_lag, hours_to_remove = get_lagged_list(Y, time_listH, lag=24, hours_to_remove_prev=hours_to_remove)
        print("  rs.%i: lagged list is (%i)" % (gf(cf()).lineno, len(lagged_list)))

        #X_lagged = np.transpose(np.matrix(lagged_list[max_lag:]))
        X_lagged = np.transpose(np.matrix(lagged_list))
        X_HAR = np.append(X_AR, X_lagged, axis=1)
        print("  rs.%i: X_HAR is (%i,%i)" % (gf(cf()).lineno, np.size(X_HAR,0), np.size(X_HAR,1)))

        last_day_average = get_last_day_average(Y, time_listH, index_list_prev_lag)
        print("  rs.%i: last day average is (%i)" % (gf(cf()).lineno, len(last_day_average)))
        #last_day_average = np.transpose(np.matrix(last_day_average[max_lag:]))
        last_day_average = np.transpose(np.matrix(last_day_average))

        if prints == 1:
            n_x += 1
            print(
                "  rs.%i: x%i through x%i is the X_AR(%i) model" % (gf(cf()).lineno, n_x, n_x + AR_order - 1, AR_order))
            n_x += AR_order
            print("  rs.%i: x%i is the value 24 hours prior" % (gf(cf()).lineno, n_x))
            n_x += 1
            print("  rs.%i: x%i is the average for the previous 24 hours" % (gf(cf()).lineno, n_x))

        X_HAR = np.append(X_HAR, last_day_average, axis=1)

    elif HAR_config == 4:  # Denne skal inkludere verdi 24 timer før, 48 timer før og snitt av 48 timer
        1

    elif HAR_config == 5:  # Denne skal inkludere X_AR(1), verdi 24 timer før, 48 timer før og snitt av 48 timer
        AR_order = 1
        max_lag = max(48, force_max_lag, AR_order)

        X_AR, hours_to_remove = AR_matrix(Y, time_listH, AR_order, hours_to_remove)
        X_AR = X_AR[max_lag - AR_order:, :]  # Hvis max lag er 24, men order=1, så vil vi kutte bort 23 entries til
        hours_to_remove = adjust_hours_for_removal(hours_to_remove, n_hours=(max_lag - AR_order))

        lagged_list_24, index_list_prev_lag_24 = get_lagged_list(Y, time_listH, lag=24)
        X_lagged = np.transpose(np.matrix(lagged_list_24[max_lag:]))

        lagged_list_48, index_list_prev_lag_48 = get_lagged_list(Y, time_listH, lag=48)
        X_lagged = np.append(X_lagged, np.transpose(np.matrix(lagged_list_48[max_lag:])), axis=1)

        X_HAR = np.append(X_AR, X_lagged, axis=1)
        last_day_average = get_last_day_average(Y, time_listH, index_list_prev_lag_48)
        last_day_average = np.transpose(np.matrix(last_day_average[max_lag:]))

        if prints == 1:
            n_x += 1
            print(
                "  rs.%i: x%i through x%i is the X_AR(%i) model" % (gf(cf()).lineno, n_x, n_x + AR_order - 1, AR_order))
            n_x += AR_order
            print("  rs.%i: x%i is the value 24 hours prior" % (gf(cf()).lineno, n_x))
            n_x += 1
            print("  rs.%i: x%i is the value 48 hours prior" % (gf(cf()).lineno, n_x))
            n_x += 1
            print("  rs.%i: x%i is the average for the previous 48 hours" % (gf(cf()).lineno, n_x))

        X_HAR = np.append(X_HAR, last_day_average, axis=1)

    if hours_in_period != -1:
        X_benchmark = X_dummies[max_lag:, :]
    else:
        X_benchmark = X_HAR

    if HAR_config > 0 and hours_in_period != -1:
        X_benchmark = np.append(X_benchmark, X_HAR, axis=1)

        # if prints == 1:
        # print("  rs.%i (END): Y is: %i, X_benchmark is (%i,%i)" % (gf(cf()).lineno, len(Y), np.size(X_benchmark, 0), np.size(X_benchmark, 1)))

    return Y, X_benchmark, max_lag, hours_to_remove


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
        for i in range(8 - len(n_obs)):
            print_rows[n_rows - 3] += " "
        print_rows[n_rows - 3] += "&"

        print_rows[n_rows - 2] += "   " + r2
        for i in range(8 - len(r2)):
            print_rows[n_rows - 2] += " "
        print_rows[n_rows - 2] += "&"

        print_rows[n_rows - 1] += " " + aic

        for i in range(10 - len(aic)):
            print_rows[n_rows - 1] += " "
        print_rows[n_rows - 1] += "&"

        if c % 2 == 1:
            if double_cols == 1:
                print_rows[n_rows - 3] += " &"
                print_rows[n_rows - 2] += " &"
                print_rows[n_rows - 1] += " &"

    return print_rows


def final_print_regressions_latex(print_rows):
    tightness = 1  #
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


def import_regressions(m_col, Y, X, coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array,
                       n_obs_array, prints=0, intercept=1):
    coeffs, tvalues, rsquared, aic, p_values, std_errs, n_obs = linreg.reg_multiple(Y, X, intercept=intercept,
                                                                                    prints=prints)
    coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array = \
        import_to_matrices(m_col, coeffs, std_errs, p_values, rsquared, aic, n_obs, coeff_matrix,
                           std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array)
    m_col += 1
    return m_col, coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array


def fmt_print(print_loc, data, p_value=1, type="coeff"):  # Her endrer vi antall desimaler i tabellene!
    if type == "coeff":
        if data >= 0:
            print_loc += "   "
        else:
            print_loc += "$-$"

        if abs(data) < 10:
            print_loc += "{0:.3f}".format(abs(data))
        else:
            print_loc += "{0:.2f}".format(abs(data))

        if p_value <= 0.01:
            stars = "** "
        elif p_value <= 0.05:
            stars = "*  "
        else:
            stars = "   "
        print_loc += stars + "&"

    elif type == "std_err":
        print_loc += "  (" + str("{0:.3f}".format(data)) + ")" + "  &"
    else:
        pass

    return print_loc


def binary_missing_to_indeces(binary_list):
    index_list = []
    rows = np.size(binary_list, 0)

    try:
        cols = np.size(binary_list, 1)
        for i in range(rows):
            if sum(binary_list[i, :]) < cols:
                index_list.append(i)
    except IndexError:
        cols = 1
        for i in range(rows):
            if binary_list[i] == 0:
                index_list.append(i)

    return index_list


def AR_matrix(y, y_time, order, hours_to_remove=[]):
    # print("  \033[0;32;0mrs.%i: running 'AR_matrix'...\033[0;0;0m" % (gf(cf()).lineno))
    n = len(y)
    ar_len = n - order

    if order == 1:
        value_exists_binary = np.zeros(n)
        x_ar = np.zeros([ar_len, 1])
        i = n - 1
        year, month, day, hour, minute = supp.fix_time_list(y_time, single_time_stamp=0, move_n_hours=-1)
        y_time_moved = supp.make_time_list(year, month, day, hour, minute)

        while i >= 0:
            found = False
            j = i

            while not found and j >= 0:
                if y_time_moved[i] == y_time[j]:
                    found = True
                    value_exists_binary[i] = 1
                    x_ar[i - 1, 0] = y[j]
                j -= 1
            if not found:
                value_exists_binary[i] = 0
            i -= 1
    else:
        value_exists_binary = np.zeros([n, order])
        x_ar = np.zeros([ar_len, order])
        for k in range(order):
            # print("  \033[0;32;0mrs.%i: order %i out of %i\033[0;0;0m" % (gf(cf()).lineno, k+1, order))
            i = n - 1
            year, month, day, hour, minute = supp.fix_time_list(y_time, single_time_stamp=0, move_n_hours=-(k + 1))
            y_time_moved = supp.make_time_list(year, month, day, hour, minute)

            while i >= order:
                found = False
                j = i
                while not found and j >= 0:
                    if y_time_moved[i] == y_time[j]:
                        found = True
                        value_exists_binary[i, k] = 1
                        x_ar[i - order, k] = y[j]
                    j -= 1
                if not found:
                    value_exists_binary[i, k] = 0
                i -= 1
    indeces = binary_missing_to_indeces(value_exists_binary)
    hours_to_remove = add_two_remove_lists(hours_to_remove, indeces)
    # print("  \033[0;32;0mrs.%i: finished running 'AR_matrix'\033[0;0;0m" % (gf(cf()).lineno))
    return x_ar, hours_to_remove


def add_two_remove_lists(list1, list2):
    out_list = []
    if len(list1) == 0:
        out_list = list2
    elif len(list2) == 0:
        out_list = list1
    else:
        max_val = max(max(list1), max(list2))

        for i in range(max_val+1):
            if (i in list1) or (i in list2):
                out_list.append(i)
    return out_list


def time_of_day_dummies(time_list, hours_in_period=4):
    hour = supp.fix_time_list(time_list)[3]
    n_rows = len(time_list)

    n_dummies = int(24 / hours_in_period)  # Antall forklaringsvariable
    X_dummies = np.zeros([n_rows, n_dummies])
    for i in range(n_rows):
        j = int(math.floor(float(hour[i] / hours_in_period)))
        X_dummies[i, j] = 1

    return X_dummies, n_dummies


def adjust_hours_for_removal(hours_to_remove_list, n_hours=0):
    out_list = []
    for i in range(len(hours_to_remove_list)):
        if hours_to_remove_list[i] < n_hours:
            pass
        else:
            out_list.append(hours_to_remove_list[i] - n_hours)
    return out_list


def get_lagged_list(data, time_list, freq="h", lag=24, hours_to_remove_prev=[]):
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

    hours_to_remove = []
    for i in range(len(index_list)):
        if index_list[i] == -1:
            hours_to_remove.append(i)

    hours_to_remove = add_two_remove_lists(hours_to_remove, hours_to_remove_prev)

    return lagged_list, index_list, hours_to_remove


def get_last_day_average(data, time_list, index_list_prev_lag, freq="h", lag=24, hours_to_remove_prev=[]):
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

    hours_to_remove = []
    for i in range(len(last_day_average)):
        if last_day_average[i] == -1:
            hours_to_remove.append(i)

    hours_to_remove = add_two_remove_lists(hours_to_remove, hours_to_remove_prev)

    return last_day_average, hours_to_remove
