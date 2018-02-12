import os

import numpy as np

import data_import as di
import data_import_support as dis
import linreg
from Sondre import sondre_support_formulas as supp
from linreg import univariate_with_print


def print_n(n):
    for i in range(n+1):
        print()

os.chdir("/Users/sondre/Documents/GitHub/krypto")


dayofweek = 0
multivariate_regs = 1
autoreg = 0
har = 0


exchanges, time_list_minutes, prices_minutes, volumes_minutes = di.get_lists(opening_hours="n", make_totals="n")

print("Number of minutes: ", len(time_list_minutes))

time_list_days_clean, time_list_removed, returns_days_clean, volumes_days_clean, log_volumes_days_clean, spread_days_clean, \
illiq_days_clean, log_illiq_days_clean, volatility_days_clean, log_volatility_days_clean = dis.clean_trans_days(
    time_list_minutes, prices_minutes,
    volumes_minutes, full_week=1, exchange=0, days_excluded=1)

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

if dayofweek == 1:
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
            print("x%i: BAS with %i days lag" % (j + 1, lags[j]))
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

        #X_benchmark = np.append(X_benchmark, weekend, axis=1)

        X_contemporary = X_benchmark
        X_lagged = X_benchmark
        print_n(20)
        linreg.reg_multiple(Y, X_benchmark)

        print("Spread - Return")
        print("x_11 = " + "Return")
        x = returns_days_clean[start_index : end_index]
        x = np.transpose(np.matrix(x))
        X = np.append(X_benchmark, x, axis=1)
        X_contemporary = np.append(X_contemporary, x, axis=1)
        linreg.reg_multiple(Y, X)

        print("Spread - Return with 1 lag")
        print("x_11 = " + "Return with 1 lag ")
        x = returns_days_clean[start_index - 1 : end_index - 1]
        x = np.transpose(np.matrix(x))
        X = np.append(X_benchmark, x, axis=1)
        X_lagged = np.append(X_lagged, x, axis=1)
        linreg.reg_multiple(Y, X)

        print("Spread - Volume")
        print("x_11 = " + "log-Volume")
        x = log_volumes_days_clean[start_index : end_index]
        x = np.transpose(np.matrix(x))
        X = np.append(X_benchmark, x, axis=1)
        X_contemporary = np.append(X_contemporary, x, axis=1)
        linreg.reg_multiple(Y, X)

        print("Spread - Volume with lag")
        print("x_11= " + "volume with lag")
        x = log_volumes_days_clean[start_index - 1 : end_index - 1]
        x = np.transpose(np.matrix(x))
        X = np.append(X_benchmark, x, axis=1)
        X_lagged = np.append(X_lagged, x, axis=1)
        linreg.reg_multiple(Y, X)

        print("Spread - Volatility")
        print("x_11 = " + "Log-RVol")
        x = log_volatility_days_clean[start_index : end_index]
        x = np.transpose(np.matrix(x))
        X = np.append(X_benchmark, x, axis=1)
        X_contemporary = np.append(X_contemporary, x, axis=1)
        linreg.reg_multiple(Y, X)

        print("Spread - Volatility with lag")
        print("x_11 = " + "Log_RVol with lag")
        x = log_volatility_days_clean[start_index - 1 : end_index - 1]
        x = np.transpose(np.matrix(x))
        X = np.append(X_benchmark, x, axis=1)
        X_lagged = np.append(X_lagged, x, axis=1)
        linreg.reg_multiple(Y, X)

        print("Contemporaneous")
        print("x_1-x_3 = " + "lagged Rolls")
        print("x_4-10 = " + "Weekday")
        print("x_11 = " + "Return")
        print("x_12 = " + "Volume")
        print("x_13 = " + "Volatility")
        linreg.reg_multiple(Y, X_contemporary)

        print("Lagged")
        print("x_1-x_3 = " + "lagged Rolls")
        print("x_4-10 = " + "Weekend")
        print("x_11 = " + "Return with 1 lag")
        print("x_12 = " + "Volume with 1 lag")
        print("x_13 = " + "Volatility with 1 lag")
        linreg.reg_multiple(Y, X_lagged)

    if illiq_multi == 1:
        Y = log_illiq_days_clean[max_lag: len(log_illiq_days_clean)]
        n_entries = len(Y)
        start_index = len(log_illiq_days_clean) - n_entries
        end_index = len(log_illiq_days_clean)
        X = []

        print("ILLIQ")
        print("----------------------------------------------------------------------------------------------------------------------------")
        print("----------------------------------------------------------------------------------------------------------------------------")

        for j in range(n_lags):
            print("x%i: ILLIQ with %i days lag" % (j + 1, lags[j]))
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
        print_n(15)
        linreg.reg_multiple(Y, X_benchmark)

        print("ILLIQ - Return")
        print("x_11 = " + "Return")
        x = returns_days_clean[start_index: end_index]
        x = np.transpose(np.matrix(x))
        X = np.append(X_benchmark, x, axis=1)
        X_contemporary = np.append(X_contemporary, x, axis=1)
        linreg.reg_multiple(Y, X)

        print("ILLIQ - Return with 1 lag")
        print("x_11 = " + "Return with 1 lag ")
        x = returns_days_clean[start_index - 1: end_index - 1]
        x = np.transpose(np.matrix(x))
        X = np.append(X_benchmark, x, axis=1)
        X_lagged = np.append(X_lagged, x, axis=1)
        linreg.reg_multiple(Y, X)

        print("ILLIQ - Volume")
        print("x_11 = " + "log-Volume")
        x = log_volumes_days_clean[start_index: end_index]
        x = np.transpose(np.matrix(x))
        X = np.append(X_benchmark, x, axis=1)
        X_contemporary = np.append(X_contemporary, x, axis=1)
        linreg.reg_multiple(Y, X)


        print("ILLIQ - Volume with lag")
        print("x_11 = " + "volume with lag")
        x = log_volumes_days_clean[start_index - 1: end_index - 1]
        x = np.transpose(np.matrix(x))
        X = np.append(X_benchmark, x, axis=1)
        X_lagged = np.append(X_lagged, x, axis=1)
        linreg.reg_multiple(Y, X)

        print("ILLIQ - Volatility")
        print("x_11 = " + "Log-RVol")
        x = log_volatility_days_clean[start_index: end_index]
        x = np.transpose(np.matrix(x))
        X = np.append(X_benchmark, x, axis=1)
        X_contemporary = np.append(X_contemporary, x, axis=1)
        linreg.reg_multiple(Y, X)

        print("ILLIQ - Volatility with lag")
        print("x_11 = " + "Log_RVol with lag")
        x = log_volatility_days_clean[start_index - 1: end_index - 1]
        x = np.transpose(np.matrix(x))
        X = np.append(X_benchmark, x, axis=1)
        X_lagged = np.append(X_lagged, x, axis=1)
        linreg.reg_multiple(Y, X)

        print("Contemporaneous")
        print("x_1-x_3 = " + "lagged ILLIQ")
        print("x_4-10 = " + "Weekend")
        print("x_11 = " + "Return")
        print("x_12 = " + "Volume")
        print("x_13 = " + "Volatility")
        linreg.reg_multiple(Y, X_contemporary)

        print("Lagged")
        print("x_1-x_3 = " + "lagged ILLIQ")
        print("x_4-10 = " + "Weekend")
        print("x_11 = " + "Return with 1 lag")
        print("x_12 = " + "Volume with 1 lag")
        print("x_13 = " + "Volatility with 1 lag")
        linreg.reg_multiple(Y, X_lagged)

    if return_multi == 1:

        Y = returns_days_clean[max_lag: len(returns_days_clean)]
        n_entries = len(Y)
        start_index = len(returns_days_clean) - n_entries
        end_index = len(returns_days_clean)
        X = []

        print("Return")
        print("----------------------------------------------------------------------------------------------------------------------------")
        print("----------------------------------------------------------------------------------------------------------------------------")

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
        print_n(20)
        linreg.reg_multiple(Y, X_benchmark)

        print("Return - Volume")
        print("x_11 = " + "log-Volume")
        x = log_volumes_days_clean[start_index: end_index]
        x = np.transpose(np.matrix(x))
        X = np.append(X_benchmark, x, axis=1)
        X_contemporary = np.append(X_contemporary, x, axis=1)
        linreg.reg_multiple(Y, X)

        print("Return - Volume with lag")
        print("x_11 = " + "volume with lag")
        x = log_volumes_days_clean[start_index - 1: end_index - 1]
        x = np.transpose(np.matrix(x))
        X = np.append(X_benchmark, x, axis=1)
        X_lagged = np.append(X_lagged, x, axis=1)
        linreg.reg_multiple(Y, X)

        print("Return - Volatility")
        print("x_11 = " + "Log-RVol")
        x = log_volatility_days_clean[start_index: end_index]
        x = np.transpose(np.matrix(x))
        X = np.append(X_benchmark, x, axis=1)
        X_contemporary = np.append(X_contemporary, x, axis=1)
        linreg.reg_multiple(Y, X)

        print("Return - Volatility with lag")
        print("x_11 = " + "Log_RVol with lag")
        x = log_volatility_days_clean[start_index - 1: end_index - 1]
        x = np.transpose(np.matrix(x))
        X = np.append(X_benchmark, x, axis=1)
        X_lagged = np.append(X_lagged, x, axis=1)
        linreg.reg_multiple(Y, X)

        print("Return - Spread")
        print("x_11 = " + "Spread")
        x = spread_days_clean[start_index: end_index]
        x = np.transpose(np.matrix(x))
        X = np.append(X_benchmark, x, axis=1)
        X_contemporary = np.append(X_contemporary, x, axis=1)
        linreg.reg_multiple(Y, X)

        print("Return - Spread with lag")
        print("x_11 = " + "Spread with lag")
        x = spread_days_clean[start_index - 1: end_index - 1]
        x = np.transpose(np.matrix(x))
        X = np.append(X_benchmark, x, axis=1)
        X_lagged = np.append(X_lagged, x, axis=1)
        linreg.reg_multiple(Y, X)

        print("Return - ILLIQ")
        print("x_11 = " + "ILLIQ")
        x = log_illiq_days_clean[start_index: end_index]
        x = np.transpose(np.matrix(x))
        X = np.append(X_benchmark, x, axis=1)
        X_contemporary = np.append(X_contemporary, x, axis=1)
        linreg.reg_multiple(Y, X)

        print("Return - ILLIQ with lag")
        print("x_11 = " + "ILLIQ with lag")
        x = log_illiq_days_clean[start_index - 1: end_index - 1]
        x = np.transpose(np.matrix(x))
        X = np.append(X_benchmark, x, axis=1)
        X_lagged = np.append(X_lagged, x, axis=1)
        linreg.reg_multiple(Y, X)


        print("Contemporaneous")
        print("x_1-x_3 = " + "lagged returns")
        print("x_4-10 = " + "Weekend")
        print("x_11 = " + "Volume")
        print("x_12 = " + "Volatility")
        print("x_13 = " + "Spread")
        print("x_14 = " + "ILLIQ")
        linreg.reg_multiple(Y, X_contemporary)

        print("Lagged")
        print("x_1-x_3 = " + "lagged returns")
        print("x_4-10 = " + "Weekend")
        print("x_11 = " + "Volume with 1 lag")
        print("x_12 = " + "Volatility with 1 lag")
        print("x_13 = " + "Spread with 1 lag")
        print("x_14 = " + "ILLIQ with 1 lag")
        linreg.reg_multiple(Y, X_lagged)

if autoreg == 1:
    print_n(20)
    print("Rolls regression:")
    linreg.autocorr_linreg(spread_days_clean, 1, max_lag=60)
    print_n(5)
    #print("Log-ILLIQ regression:")
    #linreg.autocorr_linreg(log_illiq_days_clean, 22)
