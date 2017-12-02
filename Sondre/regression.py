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


def HAR_model(in_list):
    lags = [1, 5, 44]
    max_lag = 44  # Locked at 44! <-------------------
    Y = in_list[max_lag : len(in_list)]
    n_entries = len(Y)
    n_lags = len(lags)
    X = np.zeros([n_entries, n_lags])

    for j in range(len(lags)):
        x = supp.mean_for_n_entries(in_list, lags[j])
        x = x[len(x) - n_entries: len(x)]
        for i in range(0, n_entries):
            X[i, j] = x[i]

    linreg.reg_multiple_pandas(Y, X)


os.chdir("/Users/sondre/Documents/GitHub/krypto")
exchanges, time_list_minutes, prices_minutes, volumes_minutes = di.get_lists(opening_hours="y", make_totals="n")
time_list_days_clean, time_list_removed, returns_days_clean, volumes_days_clean, log_volumes_days_clean, spread_days_clean, \
illiq_days_clean, log_illiq_days_clean, volatility_days_clean, log_volatility_days_clean = dis.clean_trans_2013(
    time_list_minutes, prices_minutes,
    volumes_minutes)

univariate_regs = 1
rolls_uni = 1
illiq_uni = 1
autoreg = 0
har = 0

# standardize all variables
log_volumes_days_clean = supp.standardize(log_volumes_days_clean)
spread_days_clean = supp.standardize(spread_days_clean)
log_illiq_days_clean =  supp.standardize(log_illiq_days_clean)
returns_days_clean = supp.standardize(returns_days_clean)
log_volatility_days_clean = supp.standardize(log_volatility_days_clean)

if univariate_regs == 1:
    if rolls_uni == 1:
        max_lag = 44  # Locked at 44! <-------------------
        Y = spread_days_clean[max_lag: len(spread_days_clean)]
        n_entries = len(Y)
        start_index = len(spread_days_clean) - n_entries
        end_index = len(spread_days_clean)
        lags = [1, 5, 44]
        n_lags = len(lags)
        X = []
        for j in range(n_lags):
            print("x%i: Rolls with %i days lag" % (j + 1, lags[j]))
            x = supp.mean_for_n_entries(spread_days_clean, lags[j])
            x = np.matrix(x[len(x) - n_entries: len(x)])
            if j == 0:
                X = x
            else:
                X = np.append(X, x, axis=0)

        X_benchmark = np.transpose(X)  # Har model
        X_total = X_benchmark
        X_contemporary = X_benchmark
        X_lagged = X_benchmark
        print_n(20)
        linreg.reg_multiple_pandas(Y, X_benchmark)

        print("Spread - Return")
        print("x_4 = " + "Return")
        x = returns_days_clean[start_index : end_index]
        x = np.transpose(np.matrix(x))
        X = np.append(X_benchmark, x, axis=1)
        X_total = np.append(X_total, x, axis=1)
        X_contemporary = np.append(X_contemporary, x, axis=1)
        linreg.reg_multiple_pandas(Y, X)
    
        print("Spread - Return with 1 lag")
        print("x_4 = " + "Return with 1 lag ")
        x = returns_days_clean[start_index - 1 : end_index - 1]
        x = np.transpose(np.matrix(x))
        X = np.append(X_benchmark, x, axis=1)
        X_total = np.append(X_total, x, axis=1)
        X_lagged = np.append(X_lagged, x, axis=1)
        linreg.reg_multiple_pandas(Y, X)

        print("Spread - Volume")
        print("x_4 = " + "log-Volume")
        x = log_volumes_days_clean[start_index : end_index]
        x = np.transpose(np.matrix(x))
        X = np.append(X_benchmark, x, axis=1)
        X_total = np.append(X_total, x, axis=1)
        X_contemporary = np.append(X_contemporary, x, axis=1)
        linreg.reg_multiple_pandas(Y, X)

        print("Spread - Volume with lag")
        print("x_4 = " + "volume with lag")
        x = log_volumes_days_clean[start_index - 1 : end_index - 1]
        x = np.transpose(np.matrix(x))
        X = np.append(X_benchmark, x, axis=1)
        X_total = np.append(X_total, x, axis=1)
        X_lagged = np.append(X_lagged, x, axis=1)
        linreg.reg_multiple_pandas(Y, X)

        print("Spread - Volatility")
        print("x_4 = " + "Log-RVol")
        x = log_volatility_days_clean[start_index : end_index]
        x = np.transpose(np.matrix(x))
        X = np.append(X_benchmark, x, axis=1)
        X_total = np.append(X_total, x, axis=1)
        X_contemporary = np.append(X_contemporary, x, axis=1)
        linreg.reg_multiple_pandas(Y, X)

        print("Spread - Volatility with lag")
        print("x_4 = " + "Log_RVol with lag")
        x = log_volatility_days_clean[start_index - 1 : end_index - 1]
        x = np.transpose(np.matrix(x))
        X = np.append(X_benchmark, x, axis=1)
        X_total = np.append(X_total, x, axis=1)
        X_lagged = np.append(X_lagged, x, axis=1)
        linreg.reg_multiple_pandas(Y, X)

        print("Contemporary")
        print("x_1-x_3 = " + "lagged Rolls")
        print("x_4 = " + "Return")
        print("x_5 = " + "Volume")
        print("x_6 = " + "Volatility")
        linreg.reg_multiple_pandas(Y, X_contemporary)
        print("Lagged")
        print("x_1-x_3 = " + "lagged Rolls")
        print("x_4 = " + "Return with 1 lag")
        print("x_5 = " + "Volume with 1 lag")
        print("x_6 = " + "Volatility with 1 lag")
        linreg.reg_multiple_pandas(Y, X_lagged)
        print("TOTAL")
        linreg.reg_multiple_pandas(Y, X_total)

    if illiq_uni == 1:
        max_lag = 44  # Locked at 44! <-------------------
        Y = log_illiq_days_clean[max_lag: len(log_illiq_days_clean)]
        n_entries = len(Y)
        start_index = len(log_illiq_days_clean) - n_entries
        end_index = len(log_illiq_days_clean)
        lags = [1, 5, 44]
        n_lags = len(lags)
        X = []

        print("ILLIQ")
        print("----------------------------------------------------------------------------------------------------------------------------")
        print("----------------------------------------------------------------------------------------------------------------------------")
        print("----------------------------------------------------------------------------------------------------------------------------")
        print("----------------------------------------------------------------------------------------------------------------------------")
        print("----------------------------------------------------------------------------------------------------------------------------")
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
        X_total = X_benchmark
        X_contemporary = X_benchmark
        X_lagged = X_benchmark
        print_n(15)
        linreg.reg_multiple_pandas(Y, X_benchmark)

        print("ILLIQ - Return")
        print("x_4 = " + "Return")
        x = returns_days_clean[start_index: end_index]
        x = np.transpose(np.matrix(x))
        X = np.append(X_benchmark, x, axis=1)
        X_total = np.append(X_total, x, axis=1)
        X_contemporary = np.append(X_contemporary, x, axis=1)
        linreg.reg_multiple_pandas(Y, X)

        print("ILLIQ - Return with 1 lag")
        print("x_4 = " + "Return with 1 lag ")
        x = returns_days_clean[start_index - 1: end_index - 1]
        x = np.transpose(np.matrix(x))
        X = np.append(X_benchmark, x, axis=1)
        X_total = np.append(X_total, x, axis=1)
        X_lagged = np.append(X_lagged, x, axis=1)
        linreg.reg_multiple_pandas(Y, X)

        print("ILLIQ - Volume")
        print("x_4 = " + "log-Volume")
        x = log_volumes_days_clean[start_index: end_index]
        x = np.transpose(np.matrix(x))
        X = np.append(X_benchmark, x, axis=1)
        X_total = np.append(X_total, x, axis=1)
        X_contemporary = np.append(X_contemporary, x, axis=1)
        linreg.reg_multiple_pandas(Y, X)

        print("ILLIQ - Volume with lag")
        print("x_4 = " + "volume with lag")
        x = log_volumes_days_clean[start_index - 1: end_index - 1]
        x = np.transpose(np.matrix(x))
        X = np.append(X_benchmark, x, axis=1)
        X_total = np.append(X_total, x, axis=1)
        X_lagged = np.append(X_lagged, x, axis=1)
        linreg.reg_multiple_pandas(Y, X)

        print("ILLIQ - Volatility")
        print("x_4 = " + "Log-RVol")
        x = log_volatility_days_clean[start_index: end_index]
        x = np.transpose(np.matrix(x))
        X = np.append(X_benchmark, x, axis=1)
        X_total = np.append(X_total, x, axis=1)
        X_contemporary = np.append(X_contemporary, x, axis=1)
        linreg.reg_multiple_pandas(Y, X)

        print("ILLIQ - Volatility with lag")
        print("x_4 = " + "Log_RVol with lag")
        x = log_volatility_days_clean[start_index - 1: end_index - 1]
        x = np.transpose(np.matrix(x))
        X = np.append(X_benchmark, x, axis=1)
        X_total = np.append(X_total, x, axis=1)
        X_lagged = np.append(X_lagged, x, axis=1)
        linreg.reg_multiple_pandas(Y, X)

        print("Contemporary")
        print("x_1-x_3 = " + "lagged ILLIQ")
        print("x_4 = " + "Return")
        print("x_5 = " + "Volume")
        print("x_6 = " + "Volatility")
        linreg.reg_multiple_pandas(Y, X_contemporary)
        print("Lagged")
        print("x_1-x_3 = " + "lagged ILLIQ")
        print("x_4 = " + "Return with 1 lag")
        print("x_5 = " + "Volume with 1 lag")
        print("x_6 = " + "Volatility with 1 lag")
        linreg.reg_multiple_pandas(Y, X_lagged)
        print("TOTAL")
        linreg.reg_multiple_pandas(Y, X_total)

if autoreg == 1:
    print_n(20)
    print("Rolls regression:")
    linreg.autocorr_linreg(spread_days_clean, 12)
    print_n(5)
    print("Log-ILLIQ regression:")
    linreg.autocorr_linreg(log_illiq_days_clean, 12)

if har == 1:
    print_n(20)
    print("Rolls regression:")
    HAR_model(spread_days_clean)
    print_n(15)
    print("Log-ILLIQ regression:")
    HAR_model(log_illiq_days_clean)


test_multilinreg = 0
if test_multilinreg == 1:
    x1 = np.arange(30)
    x2 = np.zeros(30) + np.random.uniform(-1, 1, 30)
    x3 = np.zeros(30) + np.random.uniform(-3, 3, 30)

    y = x1 + x2 + x3 + np.random.uniform(-1, 1, 30)
    X2 = np.zeros([30,2])
    X3 = np.zeros([30,3])
    j = 0
    for i in range(0, 30):
        X2[i, j] = x1[i]
        X3[i, j] = x1[i]
    j = 1
    for i in range(0, 30):
        X2[i, j] = x2[i]
        X3[i, j] = x2[i]
    j = 2
    for i in range(0, 30):
        X3[i, j] = x3[i]

    print_n(5)
    linreg.reg_multiple_pandas(y, x1)
    print_n(5)
    linreg.reg_multiple_pandas(y, X2)
    print_n(5)
    linreg.reg_multiple_pandas(y, X3)
