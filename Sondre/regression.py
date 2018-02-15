import os
import numpy as np
import data_import as di
import data_import_support as dis
import linreg
from Sondre import sondre_support_formulas as supp
from tabulate import tabulate as tbl


def print_n(n):
    for k in range(n+1):
        print()


def import_to_matrices(m_col, coeffs, std_errs, p_values, rsquared, aic, n_obs, coeff_matrix,
                               std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array):
    for i in range(0, len(coeffs)):
        coeff_matrix[i, m_col] = coeffs[i]
        std_errs_matrix[i, m_col] = std_errs[i]
        p_values_matrix[i, m_col] = p_values[i]
    rsquared_array[m_col] = rsquared
    aic_array[m_col] = aic
    n_obs_array[m_col] = n_obs
    return coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array


def fmt_print(print_loc, data, p_value=1, type="coeff"):

    if type == "coeff":

        if data >= 0:
            print_loc += "   "
        else:
            print_loc += "$-$"

        print_loc += "{0:.4f}".format(abs(data))

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


os.chdir("/Users/sondre/Documents/GitHub/krypto")


dayofweek = 0
multivariate_regs = 1
autoreg = 0
har = 0
exc = 0


exchanges, time_list_minutes, prices_minutes, volumes_minutes = di.get_lists(opening_hours="n", make_totals="n")


time_list_days_clean, time_list_removed, returns_days_clean, volumes_days_clean, log_volumes_days_clean, spread_days_clean, \
illiq_days_clean, log_illiq_days_clean, volatility_days_clean, log_volatility_days_clean = dis.clean_trans_days(
    time_list_minutes, prices_minutes,
    volumes_minutes, full_week=1, exchange=exc, days_excluded=0)

if dayofweek == 0:
    # standardize all variables
    log_volumes_days_clean = supp.standardize(log_volumes_days_clean)
    spread_days_clean = supp.standardize(spread_days_clean)
    log_illiq_days_clean =  supp.standardize(log_illiq_days_clean)
    returns_days_clean = supp.standardize(returns_days_clean)
    log_volatility_days_clean = supp.standardize(log_volatility_days_clean)
else:
    mean_volume = np.mean(log_volumes_days_clean)
    mean_spread = np.mean(spread_days_clean)
    mean_illiq = np.mean(log_illiq_days_clean)
    mean_return = np.mean(returns_days_clean)
    mean_volatility = np.mean(log_volatility_days_clean)

    log_volumes_days_clean -= mean_volume
    spread_days_clean -= mean_spread
    log_illiq_days_clean -= mean_illiq
    returns_days_clean -= mean_return
    log_volatility_days_clean -= mean_volatility

mon, tue, wed, thu, fri, sat, sun, day_string = supp.week_vars(time_list_days_clean)
weekend = np.zeros(len(mon))
for i in range(0, len(mon)):
    if sat[i] + sun[i] > 0:
        weekend[i] = 1

if dayofweek == 1:  # Er ikke oppdatert med ny output!
    X = np.matrix(mon)
    X = np.append(X, np.matrix(tue), axis=0)
    X = np.append(X, np.matrix(wed), axis=0)
    X = np.append(X, np.matrix(thu), axis=0)
    X = np.append(X, np.matrix(fri), axis=0)
    X = np.append(X, np.matrix(sat), axis=0)
    X = np.append(X, np.matrix(sun), axis=0)
    X = np.transpose(X)

    print_n(20)
    print("Returns")
    Y = returns_days_clean
    linreg.reg_multiple(Y, X, intercept=0)
    linreg.reg_multiple(Y, weekend)
    print("Volumes")
    Y = log_volumes_days_clean
    linreg.reg_multiple(Y, X, intercept=0)
    linreg.reg_multiple(Y, weekend)
    print("RVol")
    Y = log_volatility_days_clean
    linreg.reg_multiple(Y, X, intercept=0)
    linreg.reg_multiple(Y, weekend)
    print("SPREAD")
    Y = spread_days_clean
    linreg.reg_multiple(Y, X, intercept=0)
    linreg.reg_multiple(Y, weekend)
    print("ILLIQ")
    Y = log_illiq_days_clean
    linreg.reg_multiple(Y, X, intercept=0)
    linreg.reg_multiple(Y, weekend)


if multivariate_regs == 1:
    rolls_multi = 1
    illiq_multi = 1
    return_multi = 1

    lags = [1, 7, 60]
    max_lag = 60  # Locked
    n_lags = len(lags)

    weekend = np.matrix(weekend[max_lag: len(spread_days_clean)])
    weekend = np.transpose(weekend)
    mon = np.matrix(mon[max_lag: len(spread_days_clean)])
    mon = np.transpose(mon)
    tue = np.matrix(tue[max_lag: len(spread_days_clean)])
    tue = np.transpose(tue)
    wed = np.matrix(wed[max_lag: len(spread_days_clean)])
    wed = np.transpose(wed)
    thu = np.matrix(thu[max_lag: len(spread_days_clean)])
    thu = np.transpose(thu)
    fri = np.matrix(fri[max_lag: len(spread_days_clean)])
    fri = np.transpose(fri)
    sat = np.matrix(sat[max_lag: len(spread_days_clean)])
    sat = np.transpose(sat)
    sun = np.matrix(sun[max_lag: len(spread_days_clean)])
    sun = np.transpose(sun)

    if rolls_multi == 1:
        Y = spread_days_clean[max_lag: len(spread_days_clean)]
        n_entries = len(Y)
        start_index = len(spread_days_clean) - n_entries
        end_index = len(spread_days_clean)
        X = []

        for j in range(n_lags):
            #print("x%i: BAS with %i days lag" % (j + 1, lags[j]))
            x = supp.mean_for_n_entries(spread_days_clean, lags[j])
            x = np.matrix(x[len(x) - n_entries: len(x)])
            if j == 0:
                X = x
            else:
                X = np.append(X, x, axis=0)

        X_benchmark = np.transpose(X)  # Har model

        X_benchmark = np.append(X_benchmark, mon, axis=1)
        X_benchmark = np.append(X_benchmark, tue, axis=1)
        X_benchmark = np.append(X_benchmark, wed, axis=1)
        X_benchmark = np.append(X_benchmark, thu, axis=1)
        X_benchmark = np.append(X_benchmark, fri, axis=1)
        X_benchmark = np.append(X_benchmark, sat, axis=1)
        X_benchmark = np.append(X_benchmark, sun, axis=1)

        X_contemporary = X_benchmark
        X_lagged = X_benchmark

        #These tables are 23 rows tall, 9 wide
        n_rows = 23  # in final table
        n_entries = 15  # Må bare være minst like stor
        n_cols = 9
        coeff_matrix = np.zeros([n_entries, n_cols])
        rsquared_array = np.zeros(n_cols)
        aic_array = np.zeros(n_cols)
        n_obs_array = np.zeros(n_cols)
        p_values_matrix = np.zeros([n_entries, n_cols])
        std_errs_matrix = np.zeros([n_entries, n_cols])

        coeffs, tvalues, rsquared, aic, p_values, std_errs, n_obs = linreg.reg_multiple(Y, X_benchmark, prints=0)

        m_col = 0
        coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array = \
            import_to_matrices(m_col, coeffs, std_errs, p_values, rsquared, aic, n_obs, coeff_matrix,
                               std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array)

        # Spread - Return
        x = returns_days_clean[start_index : end_index]
        x = np.transpose(np.matrix(x))
        X = np.append(X_benchmark, x, axis=1)
        X_contemporary = np.append(X_contemporary, x, axis=1)

        coeffs, tvalues, rsquared, aic, p_values, std_errs, n_obs = linreg.reg_multiple(Y, X, prints=0)

        m_col += 1
        coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array = \
            import_to_matrices(m_col, coeffs, std_errs, p_values, rsquared, aic, n_obs, coeff_matrix,
                               std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array)

        # Spread - Return with 1 lag
        x = returns_days_clean[start_index - 1 : end_index - 1]
        x = np.transpose(np.matrix(x))
        X = np.append(X_benchmark, x, axis=1)
        X_lagged = np.append(X_lagged, x, axis=1)
        coeffs, tvalues, rsquared, aic, p_values, std_errs, n_obs = linreg.reg_multiple(Y, X, prints=0)

        m_col += 1
        coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array = \
            import_to_matrices(m_col, coeffs, std_errs, p_values, rsquared, aic, n_obs, coeff_matrix,
                               std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array)

        # Spread - Volume
        x = log_volumes_days_clean[start_index : end_index]
        x = np.transpose(np.matrix(x))
        X = np.append(X_benchmark, x, axis=1)
        X_contemporary = np.append(X_contemporary, x, axis=1)
        coeffs, tvalues, rsquared, aic, p_values, std_errs, n_obs = linreg.reg_multiple(Y, X, prints=0)

        m_col += 1
        coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array = \
            import_to_matrices(m_col, coeffs, std_errs, p_values, rsquared, aic, n_obs, coeff_matrix,
                               std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array)


        #Spread - Volume with lag
        x = log_volumes_days_clean[start_index - 1 : end_index - 1]
        x = np.transpose(np.matrix(x))
        X = np.append(X_benchmark, x, axis=1)
        X_lagged = np.append(X_lagged, x, axis=1)
        coeffs, tvalues, rsquared, aic, p_values, std_errs, n_obs = linreg.reg_multiple(Y, X, prints=0)

        m_col += 1
        coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array = \
            import_to_matrices(m_col, coeffs, std_errs, p_values, rsquared, aic, n_obs, coeff_matrix,
                               std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array)

        # Spread - Volatility
        x = log_volatility_days_clean[start_index : end_index]
        x = np.transpose(np.matrix(x))
        X = np.append(X_benchmark, x, axis=1)
        X_contemporary = np.append(X_contemporary, x, axis=1)
        coeffs, tvalues, rsquared, aic, p_values, std_errs, n_obs = linreg.reg_multiple(Y, X, prints=0)

        m_col += 1
        coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array = \
            import_to_matrices(m_col, coeffs, std_errs, p_values, rsquared, aic, n_obs, coeff_matrix,
                               std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array)

        # Spread - Volatility with lag
        x = log_volatility_days_clean[start_index - 1 : end_index - 1]
        x = np.transpose(np.matrix(x))
        X = np.append(X_benchmark, x, axis=1)
        X_lagged = np.append(X_lagged, x, axis=1)
        coeffs, tvalues, rsquared, aic, p_values, std_errs, n_obs = linreg.reg_multiple(Y, X, prints=0)

        m_col += 1
        coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array = \
            import_to_matrices(m_col, coeffs, std_errs, p_values, rsquared, aic, n_obs, coeff_matrix,
                               std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array)

        # Contemporaneous
        coeffs, tvalues, rsquared, aic, p_values, std_errs, n_obs = linreg.reg_multiple(Y, X_contemporary, prints=0)

        m_col += 1
        coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array = \
            import_to_matrices(m_col, coeffs, std_errs, p_values, rsquared, aic, n_obs, coeff_matrix,
                               std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array)

        # Lagged variables
        coeffs, tvalues, rsquared, aic, p_values, std_errs, n_obs = linreg.reg_multiple(Y, X_lagged, prints=0)

        m_col += 1
        coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array = \
            import_to_matrices(m_col, coeffs, std_errs, p_values, rsquared, aic, n_obs, coeff_matrix,
                               std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array)

        # Headers

        headers = []
        headers.append('                             ')
        for i in range(1, n_cols + 1):
            headers.append(' &     (' + str(i) + ')  ')
        headers.append("\\\\")

        first_col_entries = ['Intercept', '$bas^D$', '$bas^W$', '$bas^M$', '$r_t$', '$r_{t-1}$', '$v_{t}$',
                             '$v_{t-1}$', '$rv_{t}$', '$rv_{t-1}$', '\\textit{\\# Obs.}', '$R^2$', '\\textit{AIC}']

        first_col = []
        j = 0
        for i in range(0, len(first_col_entries)):
            first_col.append(first_col_entries[i])
            for k in range(len(first_col_entries[i]), 11):  # Tallet her skal være lengden på den lengste entrien
                first_col[j] += ' '  # Passer på at alle blir like lange
            j += 1
            if i < 10:
                first_col.append('           ')  # De første 10 radene skal ha mellomrom mellom seg
                j += 1

        print_rows = []
        # Fyller starten med tomromm så det blir lettere å sese
        for i in range(0, n_rows):
            print_rows.append('           ')
        for r in range(0, n_rows - 3):
            print_rows[r] += (first_col[r]) + "        &"
        print_rows[n_rows - 3] += (first_col[n_rows - 3]) + "   &   "
        print_rows[n_rows - 2] += (first_col[n_rows - 2]) + "        &   "
        print_rows[n_rows - 1] += (first_col[n_rows - 1]) + "       &   "

        # Dette er benchmarken
        i = 0
        for r in range(0, 8, 2):
            for c in range(0, n_cols):
                print_rows[r] = fmt_print(print_rows[r], coeff_matrix[i, c], p_values_matrix[i, c], type="coeff")
                print_rows[r + 1] = fmt_print(print_rows[r + 1], std_errs_matrix[i, c], type="std_err")
            i += 1

        # Dette er regresjonene mot en og en annen variabel
        for r in range(8, 20, 2):
            i = 11
            for c in range(0, n_cols):
                if c == int(r / 2) - 3:
                    print_rows[r] = fmt_print(print_rows[r], coeff_matrix[i, c], p_values_matrix[i, c], type="coeff")
                    print_rows[r + 1] = fmt_print(print_rows[r + 1], std_errs_matrix[i, c], type="std_err")
                    i += 1
                elif c == 7 and (r == 8 or r == 12 or r == 16):
                    i_cont = 11 + int((r - 8) / 4)
                    print_rows[r] = fmt_print(print_rows[r], coeff_matrix[i_cont, c], p_values_matrix[i_cont, c],
                                              type="coeff")
                    print_rows[r + 1] = fmt_print(print_rows[r + 1], std_errs_matrix[i_cont, c], type="std_err")
                elif c == 8 and (r == 10 or r == 14 or r == 18):
                    i_lag = 11 + int((r - 10) / 4)
                    print_rows[r] = fmt_print(print_rows[r], coeff_matrix[i_cont, c], p_values_matrix[i_cont, c],
                                              type="coeff")
                    print_rows[r + 1] = fmt_print(print_rows[r + 1], std_errs_matrix[i_lag, c], type="std_err")
                else:
                    print_rows[r] += "           &"
                    print_rows[r + 1] += "           &"
        # Dette fikser de tre nedreste radene
        for c in range(0, n_cols):
            print_rows[n_rows - 3] += str(int(n_obs_array[c])) + "    &   "
            print_rows[n_rows - 2] += "{0:.3f}".format(rsquared_array[c]) + "   &   "
            print_rows[n_rows - 1] += str(int(aic_array[c])) + "    &   "

        print()
        print()
        print()
        print("           -----------------------------------------Regression table for Bid-ask spread----------------------------------------")
        print()
        print()
        for i in range(0, len(headers)):
            print(headers[i], end='')
        print()
        for i in range(0, len(print_rows)):
            if i < len(print_rows)-3:
                print(print_rows[i][0:len(print_rows[i]) - 3] + "\\\\")  # Fjerner det siste &-tegnet og legger til backslash
            else:
                print(print_rows[i][0:len(print_rows[i]) - 6] + "\\\\")  # Fjerner det siste &-tegnet og legger til backslash

    if illiq_multi == 1:
        Y = log_illiq_days_clean[max_lag: len(log_illiq_days_clean)]
        n_entries = len(Y)
        start_index = len(log_illiq_days_clean) - n_entries
        end_index = len(log_illiq_days_clean)
        X = []

        #print("ILLIQ")
        #print("----------------------------------------------------------------------------------------------------------------------------")
        #print("----------------------------------------------------------------------------------------------------------------------------")

        for j in range(n_lags):
            #print("x%i: ILLIQ with %i days lag" % (j + 1, lags[j]))
            x = supp.mean_for_n_entries(log_illiq_days_clean, lags[j])
            x = np.matrix(x[len(x) - n_entries: len(x)])
            if j == 0:
                X = x
            else:
                X = np.append(X, x, axis=0)

        print_n(5)
        X_benchmark = np.transpose(X)  # Har model

        X_benchmark = np.append(X_benchmark, mon, axis=1)
        X_benchmark = np.append(X_benchmark, tue, axis=1)
        X_benchmark = np.append(X_benchmark, wed, axis=1)
        X_benchmark = np.append(X_benchmark, thu, axis=1)
        X_benchmark = np.append(X_benchmark, fri, axis=1)
        X_benchmark = np.append(X_benchmark, sat, axis=1)
        X_benchmark = np.append(X_benchmark, sun, axis=1)

        X_contemporary = X_benchmark
        X_lagged = X_benchmark


        #These tables are 23 rows tall, 9 wide
        n_rows = 23  # in final table
        n_entries = 15  # Må bare være minst like stor
        n_cols = 9
        coeff_matrix = np.zeros([n_entries, n_cols])
        rsquared_array = np.zeros(n_cols)
        aic_array = np.zeros(n_cols)
        n_obs_array = np.zeros(n_cols)
        p_values_matrix = np.zeros([n_entries, n_cols])
        std_errs_matrix = np.zeros([n_entries, n_cols])



        coeffs, tvalues, rsquared, aic, p_values, std_errs, n_obs = linreg.reg_multiple(Y, X_benchmark, prints=0)

        m_col = 0
        coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array = \
            import_to_matrices(m_col, coeffs, std_errs, p_values, rsquared, aic, n_obs, coeff_matrix,
                               std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array)

        # ILLIQ - Return
        x = returns_days_clean[start_index : end_index]
        x = np.transpose(np.matrix(x))
        X = np.append(X_benchmark, x, axis=1)
        X_contemporary = np.append(X_contemporary, x, axis=1)

        coeffs, tvalues, rsquared, aic, p_values, std_errs, n_obs = linreg.reg_multiple(Y, X, prints=0)

        m_col += 1
        coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array = \
            import_to_matrices(m_col, coeffs, std_errs, p_values, rsquared, aic, n_obs, coeff_matrix,
                               std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array)

        # ILLIQ  - Return with 1 lag
        x = returns_days_clean[start_index - 1 : end_index - 1]
        x = np.transpose(np.matrix(x))
        X = np.append(X_benchmark, x, axis=1)
        X_lagged = np.append(X_lagged, x, axis=1)
        coeffs, tvalues, rsquared, aic, p_values, std_errs, n_obs = linreg.reg_multiple(Y, X, prints=0)

        m_col += 1
        coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array = \
            import_to_matrices(m_col, coeffs, std_errs, p_values, rsquared, aic, n_obs, coeff_matrix,
                               std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array)

        # ILLIQ - Volume
        x = log_volumes_days_clean[start_index : end_index]
        x = np.transpose(np.matrix(x))
        X = np.append(X_benchmark, x, axis=1)
        X_contemporary = np.append(X_contemporary, x, axis=1)
        coeffs, tvalues, rsquared, aic, p_values, std_errs, n_obs = linreg.reg_multiple(Y, X, prints=0)

        m_col += 1
        coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array = \
            import_to_matrices(m_col, coeffs, std_errs, p_values, rsquared, aic, n_obs, coeff_matrix,
                               std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array)


        # ILLIQ - Volume with lag
        x = log_volumes_days_clean[start_index - 1 : end_index - 1]
        x = np.transpose(np.matrix(x))
        X = np.append(X_benchmark, x, axis=1)
        X_lagged = np.append(X_lagged, x, axis=1)
        coeffs, tvalues, rsquared, aic, p_values, std_errs, n_obs = linreg.reg_multiple(Y, X, prints=0)

        m_col += 1
        coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array = \
            import_to_matrices(m_col, coeffs, std_errs, p_values, rsquared, aic, n_obs, coeff_matrix,
                               std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array)

        # ILLIQ  - Volatility
        x = log_volatility_days_clean[start_index : end_index]
        x = np.transpose(np.matrix(x))
        X = np.append(X_benchmark, x, axis=1)
        X_contemporary = np.append(X_contemporary, x, axis=1)
        coeffs, tvalues, rsquared, aic, p_values, std_errs, n_obs = linreg.reg_multiple(Y, X, prints=0)

        m_col += 1
        coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array = \
            import_to_matrices(m_col, coeffs, std_errs, p_values, rsquared, aic, n_obs, coeff_matrix,
                               std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array)

        # ILLIQ - Volatility with lag
        x = log_volatility_days_clean[start_index - 1 : end_index - 1]
        x = np.transpose(np.matrix(x))
        X = np.append(X_benchmark, x, axis=1)
        X_lagged = np.append(X_lagged, x, axis=1)
        coeffs, tvalues, rsquared, aic, p_values, std_errs, n_obs = linreg.reg_multiple(Y, X, prints=0)

        m_col += 1
        coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array = \
            import_to_matrices(m_col, coeffs, std_errs, p_values, rsquared, aic, n_obs, coeff_matrix,
                               std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array)

        # Contemporaneous
        coeffs, tvalues, rsquared, aic, p_values, std_errs, n_obs = linreg.reg_multiple(Y, X_contemporary, prints=0)

        m_col += 1
        coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array = \
            import_to_matrices(m_col, coeffs, std_errs, p_values, rsquared, aic, n_obs, coeff_matrix,
                               std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array)

        # Lagged variables
        coeffs, tvalues, rsquared, aic, p_values, std_errs, n_obs = linreg.reg_multiple(Y, X_lagged, prints=0)

        m_col += 1
        coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array = \
            import_to_matrices(m_col, coeffs, std_errs, p_values, rsquared, aic, n_obs, coeff_matrix,
                               std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array)

        # Headers

        headers = []
        headers.append('                             ')
        for i in range(1, n_cols + 1):
            headers.append(' &     ('+str(i)+')  ')
        headers.append("\\\\")

        first_col_entries = ['Intercept', '$illiq^D$', '$illiq^W$', '$illiq^M$', '$r_t$', '$r_{t-1}$','$v_{t}$',
                             '$v_{t-1}$', '$rv_{t}$', '$rv_{t-1}$', '\\textit{\\# Obs.}', '$R^2$', '\\textit{AIC}']

        first_col = []
        j = 0
        for i in range(0, len(first_col_entries)):
            first_col.append(first_col_entries[i])
            for k in range (len(first_col_entries[i]), 11):  # Tallet her skal være lengden på den lengste entrien
                first_col[j] += ' '  # Passer på at alle blir like lange
            j += 1
            if i < 10:
                first_col.append('           ')  # De første 10 radene skal ha mellomrom mellom seg
                j += 1

        print_rows = []
        # Fyller starten med tomromm så det blir lettere å sese
        for i in range(0, n_rows):
            print_rows.append('           ')
        for r in range(0, n_rows-3):
            print_rows[r] += (first_col[r]) + "        &"
        print_rows[n_rows-3] += (first_col[n_rows-3]) + "   &   "
        print_rows[n_rows-2] += (first_col[n_rows-2]) + "        &   "
        print_rows[n_rows-1] += (first_col[n_rows-1]) + "       &   "

        # Dette er benchmarken
        i = 0
        for r in range(0, 8, 2):
            for c in range(0, n_cols):
                print_rows[r] = fmt_print(print_rows[r], coeff_matrix[i, c], p_values_matrix[i, c], type="coeff")
                print_rows[r + 1] = fmt_print(print_rows[r + 1], std_errs_matrix[i, c], type="std_err")
            i += 1

        # Dette er regresjonene mot en og en annen variabel
        for r in range(8, 20, 2):
            i = 11
            for c in range(0, n_cols):
                if c == int(r/2) - 3:
                    print_rows[r] = fmt_print(print_rows[r], coeff_matrix[i, c], p_values_matrix[i, c], type="coeff")
                    print_rows[r + 1] = fmt_print(print_rows[r + 1], std_errs_matrix[i, c], type="std_err")
                    i += 1
                elif c == 7 and (r == 8 or r == 12 or r == 16):
                    i_cont = 11 + int((r-8)/4)
                    print_rows[r] = fmt_print(print_rows[r], coeff_matrix[i_cont, c], p_values_matrix[i_cont, c], type="coeff")
                    print_rows[r + 1] = fmt_print(print_rows[r + 1], std_errs_matrix[i_cont, c], type="std_err")
                elif c == 8 and (r == 10 or r == 14 or r == 18):
                    i_lag = 11 + int((r-10)/4)
                    print_rows[r] = fmt_print(print_rows[r], coeff_matrix[i_cont, c], p_values_matrix[i_cont, c], type="coeff")
                    print_rows[r + 1] = fmt_print(print_rows[r + 1], std_errs_matrix[i_lag, c], type="std_err")
                else:
                    print_rows[r] += "           &"
                    print_rows[r + 1] += "           &"
        # Dette fikser de tre nedreste radene
        for c in range(0, n_cols):
            print_rows[n_rows-3] += str(int(n_obs_array[c])) + "    &   "
            print_rows[n_rows-2] += "{0:.3f}".format(rsquared_array[c]) + "   &   "
            print_rows[n_rows-1] += str(int(aic_array[c])) + "    &   "

        print()
        print()
        print("           -----------------------------------------Regression table for ILLIQ----------------------------------------")
        print()
        print()
        for i in range(0, len(headers)):
            print(headers[i], end='')
        print()
        for i in range(0, len(print_rows)):
            if i < len(print_rows)-3:
                print(print_rows[i][0:len(print_rows[i]) - 3] + "\\\\")  # Fjerner det siste &-tegnet og legger til backslash
            else:
                print(print_rows[i][0:len(print_rows[i]) - 6] + "\\\\")  # Fjerner det siste &-tegnet og legger til backslash

    if return_multi == 1:

        Y = returns_days_clean[max_lag: len(returns_days_clean)]
        n_entries = len(Y)
        start_index = len(returns_days_clean) - n_entries
        end_index = len(returns_days_clean)
        X = []

        #print("Return")
        #print("----------------------------------------------------------------------------------------------------------------------------")
        #print("----------------------------------------------------------------------------------------------------------------------------")

        for j in range(n_lags):
            print("x%i: Returns with %i days lag" % (j + 1, lags[j]))
            x = supp.mean_for_n_entries(returns_days_clean, lags[j])
            x = np.matrix(x[len(x) - n_entries: len(x)])
            if j == 0:
                X = x
            else:
                X = np.append(X, x, axis=0)

        X_benchmark = np.transpose(X)  # Har model

        X_benchmark = np.append(X_benchmark, mon, axis=1)
        X_benchmark = np.append(X_benchmark, tue, axis=1)
        X_benchmark = np.append(X_benchmark, wed, axis=1)
        X_benchmark = np.append(X_benchmark, thu, axis=1)
        X_benchmark = np.append(X_benchmark, fri, axis=1)
        X_benchmark = np.append(X_benchmark, sat, axis=1)
        X_benchmark = np.append(X_benchmark, sun, axis=1)

        X_contemporary = X_benchmark
        X_lagged = X_benchmark


        #These tables are 27 rows tall, 11 wide
        n_rows = 27  # in final table
        n_entries = 18  # Må bare være minst like stor
        n_cols = 11
        coeff_matrix = np.zeros([n_entries, n_cols])
        rsquared_array = np.zeros(n_cols)
        aic_array = np.zeros(n_cols)
        n_obs_array = np.zeros(n_cols)
        p_values_matrix = np.zeros([n_entries, n_cols])
        std_errs_matrix = np.zeros([n_entries, n_cols])

        coeffs, tvalues, rsquared, aic, p_values, std_errs, n_obs = linreg.reg_multiple(Y, X_benchmark, prints=0)

        m_col = 0
        coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array = \
            import_to_matrices(m_col, coeffs, std_errs, p_values, rsquared, aic, n_obs, coeff_matrix,
                               std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array)

        #Return - Volume
        x = log_volumes_days_clean[start_index: end_index]
        x = np.transpose(np.matrix(x))
        X = np.append(X_benchmark, x, axis=1)
        X_contemporary = np.append(X_contemporary, x, axis=1)
        coeffs, tvalues, rsquared, aic, p_values, std_errs, n_obs = linreg.reg_multiple(Y, X, prints=0)

        m_col += 1
        coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array = \
            import_to_matrices(m_col, coeffs, std_errs, p_values, rsquared, aic, n_obs, coeff_matrix,
                               std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array)

        # Return - Volume with lag
        x = log_volumes_days_clean[start_index - 1: end_index - 1]
        x = np.transpose(np.matrix(x))
        X = np.append(X_benchmark, x, axis=1)
        X_lagged = np.append(X_lagged, x, axis=1)
        coeffs, tvalues, rsquared, aic, p_values, std_errs, n_obs = linreg.reg_multiple(Y, X, prints=0)

        m_col += 1
        coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array = \
            import_to_matrices(m_col, coeffs, std_errs, p_values, rsquared, aic, n_obs, coeff_matrix,
                               std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array)

        # Return - Volatility
        x = log_volatility_days_clean[start_index: end_index]
        x = np.transpose(np.matrix(x))
        X = np.append(X_benchmark, x, axis=1)
        X_contemporary = np.append(X_contemporary, x, axis=1)
        coeffs, tvalues, rsquared, aic, p_values, std_errs, n_obs = linreg.reg_multiple(Y, X, prints=0)

        m_col += 1
        coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array = \
            import_to_matrices(m_col, coeffs, std_errs, p_values, rsquared, aic, n_obs, coeff_matrix,
                               std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array)

        # Return - Volatility with lag
        x = log_volatility_days_clean[start_index - 1: end_index - 1]
        x = np.transpose(np.matrix(x))
        X = np.append(X_benchmark, x, axis=1)
        X_lagged = np.append(X_lagged, x, axis=1)
        coeffs, tvalues, rsquared, aic, p_values, std_errs, n_obs = linreg.reg_multiple(Y, X, prints=0)

        m_col += 1
        coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array = \
            import_to_matrices(m_col, coeffs, std_errs, p_values, rsquared, aic, n_obs, coeff_matrix,
                               std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array)

        # Return - Spread
        x = spread_days_clean[start_index: end_index]
        x = np.transpose(np.matrix(x))
        X = np.append(X_benchmark, x, axis=1)
        X_contemporary = np.append(X_contemporary, x, axis=1)
        coeffs, tvalues, rsquared, aic, p_values, std_errs, n_obs = linreg.reg_multiple(Y, X, prints=0)

        m_col += 1
        coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array = \
            import_to_matrices(m_col, coeffs, std_errs, p_values, rsquared, aic, n_obs, coeff_matrix,
                               std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array)

        # Return - Spread with lag
        x = spread_days_clean[start_index - 1: end_index - 1]
        x = np.transpose(np.matrix(x))
        X = np.append(X_benchmark, x, axis=1)
        X_lagged = np.append(X_lagged, x, axis=1)
        coeffs, tvalues, rsquared, aic, p_values, std_errs, n_obs = linreg.reg_multiple(Y, X, prints=0)

        m_col += 1
        coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array = \
            import_to_matrices(m_col, coeffs, std_errs, p_values, rsquared, aic, n_obs, coeff_matrix,
                               std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array)

        # Return - ILLIQ
        x = log_illiq_days_clean[start_index: end_index]
        x = np.transpose(np.matrix(x))
        X = np.append(X_benchmark, x, axis=1)
        X_contemporary = np.append(X_contemporary, x, axis=1)
        coeffs, tvalues, rsquared, aic, p_values, std_errs, n_obs = linreg.reg_multiple(Y, X, prints=0)

        m_col += 1
        coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array = \
            import_to_matrices(m_col, coeffs, std_errs, p_values, rsquared, aic, n_obs, coeff_matrix,
                               std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array)

        # Return - ILLIQ with lag
        x = log_illiq_days_clean[start_index - 1: end_index - 1]
        x = np.transpose(np.matrix(x))
        X = np.append(X_benchmark, x, axis=1)
        X_lagged = np.append(X_lagged, x, axis=1)
        coeffs, tvalues, rsquared, aic, p_values, std_errs, n_obs = linreg.reg_multiple(Y, X, prints=0)

        m_col += 1
        coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array = \
            import_to_matrices(m_col, coeffs, std_errs, p_values, rsquared, aic, n_obs, coeff_matrix,
                               std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array)

        # Contemporaneous
        coeffs, tvalues, rsquared, aic, p_values, std_errs, n_obs = linreg.reg_multiple(Y, X_contemporary, prints=0)

        m_col += 1
        coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array = \
            import_to_matrices(m_col, coeffs, std_errs, p_values, rsquared, aic, n_obs, coeff_matrix,
                               std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array)

        #  Lagged
        coeffs, tvalues, rsquared, aic, p_values, std_errs, n_obs = linreg.reg_multiple(Y, X_lagged, prints=0)

        m_col += 1
        coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array = \
            import_to_matrices(m_col, coeffs, std_errs, p_values, rsquared, aic, n_obs, coeff_matrix,
                               std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array)

        # Headers

        headers = []
        headers.append('                             ')
        for i in range(1, n_cols + 1):
            headers.append(' &     ('+str(i)+')  ')
        headers.append("\\\\")

        first_col_entries = ['Intercept', '$r^D$', '$r^W$', '$r^M$', '$v_t$', '$v_{t-1}$','$rv_{t}$',
                             '$rv_{t-1}$', '$bas_{t}$', '$bas_{t-1}$', '$illiq_{t}$', '$illiq_{t-1}$',
                             '\\textit{\\# Obs.}', '$R^2$', '\\textit{AIC}']

        first_col = []
        j = 0
        for i in range(0, len(first_col_entries)):
            first_col.append(first_col_entries[i])
            for k in range (len(first_col_entries[i]), 11):  # Tallet her skal være lengden på den lengste entrien
                first_col[j] += ' '  # Passer på at alle blir like lange
            j += 1
            if i < 12:
                first_col.append('           ')  # De første 12 radene skal ha mellomrom mellom seg
                j += 1

        print_rows = []
        # Fyller starten med tomromm så det blir lettere å sese
        for i in range(0, n_rows):
            print_rows.append('           ')
        for r in range(0, n_rows-3):
            print_rows[r] += (first_col[r]) + "        &"
        print_rows[n_rows-3] += (first_col[n_rows-3]) + "   &   "
        print_rows[n_rows-2] += (first_col[n_rows-2]) + "        &   "
        print_rows[n_rows-1] += (first_col[n_rows-1]) + "       &   "


        # Dette er benchmarken
        i = 0
        for r in range(0, 8, 2):
            for c in range(0, n_cols):
                print_rows[r] = fmt_print(print_rows[r], coeff_matrix[i, c], p_values_matrix[i, c], type="coeff")
                print_rows[r + 1] = fmt_print(print_rows[r + 1], std_errs_matrix[i, c], type="std_err")
            i += 1

        # Dette er regresjonene mot en og en annen variabel
        for r in range(8, 24, 2):
            i = 11
            for c in range(0, n_cols):
                if c == int(r / 2) - 3:
                    print_rows[r] = fmt_print(print_rows[r], coeff_matrix[i, c], p_values_matrix[i, c], type="coeff")
                    print_rows[r + 1] = fmt_print(print_rows[r + 1], std_errs_matrix[i, c], type="std_err")
                    i += 1
                elif c == 7 and (r == 8 or r == 12 or r == 16 or r ==20):
                    i_cont = 11 + int((r - 8) / 4)
                    print_rows[r] = fmt_print(print_rows[r], coeff_matrix[i_cont, c], p_values_matrix[i_cont, c], type="coeff")
                    print_rows[r + 1] = fmt_print(print_rows[r + 1], std_errs_matrix[i_cont, c], type="std_err")
                elif c == 8 and (r == 10 or r == 14 or r == 18 or r == 22):
                    i_lag = 11 + int((r - 10) / 4)
                    print_rows[r] = fmt_print(print_rows[r], coeff_matrix[i_lag, c], p_values_matrix[i_lag, c], type="coeff")
                    print_rows[r + 1] = fmt_print(print_rows[r + 1], std_errs_matrix[i_lag, c], type="std_err")
                else:
                    print_rows[r] += "           &"
                    print_rows[r + 1] += "           &"

        # Dette fikser de tre nedreste radene
        for c in range(0, n_cols):
            print_rows[n_rows - 3] += str(int(n_obs_array[c])) + "    &   "
            print_rows[n_rows - 2] += "{0:.3f}".format(rsquared_array[c]) + "   &   "
            print_rows[n_rows - 1] += str(int(aic_array[c])) + "    &   "

        print()
        print()
        print(
            "           -----------------------------------------Regression table for Return----------------------------------------")
        print()
        print()
        for i in range(0, len(headers)):
            print(headers[i], end='')
        print()
        for i in range(0, len(print_rows)):
            if i < len(print_rows) - 3:
                print(print_rows[i][
                      0:len(print_rows[i]) - 3] + "\\\\")  # Fjerner det siste &-tegnet og legger til backslash
            else:
                print(print_rows[i][
                      0:len(print_rows[i]) - 6] + "\\\\")  # Fjerner det siste &-tegnet og legger til backslash

if autoreg == 1:  # Er ikke oppdatert med ny output!
    print_n(20)
    print("Rolls regression:")
    linreg.autocorr_linreg(spread_days_clean, 1, max_lag=60)
    print_n(5)
    #print("Log-ILLIQ regression:")
    #linreg.autocorr_linreg(log_illiq_days_clean, 22)
