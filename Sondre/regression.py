import linreg
import data_import_support as dis
import data_import as di
import numpy as np
from Sondre import sondre_support_formulas as supp
import os


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


def univariate_with_print(y, x):
    slope, intercept, r_value, p_value, stderr = linreg.linreg_coeffs(x, y)
    linreg.stats(slope, intercept, r_value, p_value)


os.chdir("/Users/sondre/Documents/GitHub/krypto")
exchanges, time_list_minutes, prices_minutes, volumes_minutes = di.get_lists(opening_hours="y", make_totals="n")
time_list_days_clean, time_list_removed, returns_days_clean, volumes_days_clean, log_volumes_days_clean, spread_days_clean, \
illiq_days_clean, log_illiq_days_clean, volatility_days_clean, log_volatility_days_clean = dis.clean_trans_2013(
    time_list_minutes, prices_minutes,
    volumes_minutes)

univariate_regs = 1
if univariate_regs == 1:
    max_lag = 44  # Locked at 44! <-------------------
    Y = spread_days_clean[max_lag: len(spread_days_clean)]
    n_entries = len(Y)
    start_index = len(x) - n_entries
    total length = lenx
    lags = [1, 5, 44]
    n_lags = len(lags)
    for j in range(n_lags):
        x = supp.mean_for_n_entries(spread_days_clean, lags[j])
        x = x[len(x) - n_entries: len(x)]
        print("Spread - Average spread for last %i days" % lags[j])
        univariate_with_print(Y, x)

    x = returns_days_clean[len(returns_days_clean) - n_entries]


autoreg = 0
if autoreg == 1:
    print_n(20)
    print("Rolls regression:")
    linreg.autocorr_linreg(spread_days_clean, 12)
    print_n(5)
    print("Log-ILLIQ regression:")
    linreg.autocorr_linreg(log_illiq_days_clean, 12)

har = 0
if har == 1:
    print_n(20)
    print("Rolls regression:")
    HAR_model(spread_days_clean)
    print_n(15)
    print("Log-ILLIQ regression:")
    HAR_model(log_illiq_days_clean)


rolls_reg = 0
if rolls_reg == 1:
    lags = [1, 5, 44]
    max_lag = 44  # Locked at 44! <-------------------

    Y = spread_days_clean[max_lag: len(spread_days_clean)]
    print_n(20)
    n_entries = len(Y)
    n_lags = len(lags)
    n_others = 6
    n_explanatory = n_lags + n_others
    X = np.zeros([n_entries, n_explanatory])
    print("--------------EXPLANATORY VARIABLES--------------")
    for j in range(n_lags):
        print("x%i: Rolls with %i days lag" % (j + 1, lags[j]))
        x = supp.mean_for_n_entries(spread_days_clean, lags[j])
        x = x[len(x) - n_entries: len(x)]
        for i in range(0, n_entries):
            X[i, j] = x[i]

    j = n_lags
    print("x%i: Returns" % (j+1))
    for i in range(0, n_entries):
        X[i, j] = returns_days_clean[i]

    j += 1
    print("x%i: Returns with 1 lag" % (j+1))
    for i in range(0, n_entries):
        X[i, j] = returns_days_clean[i - 1]

    j += 1
    print("x%i: Log Volumes (normalized)" % (j+1))
    for i in range(0, n_entries):
        X[i, j] = log_volumes_days_clean[i]

    j += 1
    print("x%i: Log Volumes (normalized) with 1 lag" % (j + 1))
    for i in range(0, n_entries):
        X[i, j] = log_volumes_days_clean[i]

    j += 1
    print("x%i: Log Realized Volatility" % (j+1))
    for i in range(0, n_entries):
        X[i, j] = log_volatility_days_clean[i]

    j += 1
    print("x%i: Log Realized Volatility with 1 lag" % (j + 1))
    for i in range(0, n_entries):
        X[i, j] = log_volatility_days_clean[i - 1]


    print()
    linreg.reg_multiple_pandas(Y, X)

illiq_reg = 0
if illiq_reg == 1:
    lags = [1, 5, 44]
    max_lag = 44  # Locked at 44! <-------------------

    Y = log_illiq_days_clean[max_lag: len(log_illiq_days_clean)]
    print_n(20)
    n_entries = len(Y)
    n_lags = len(lags)
    n_others = 6
    n_explanatory = n_lags + n_others
    X = np.zeros([n_entries, n_explanatory])
    print("--------------EXPLANATORY VARIABLES--------------")
    for j in range(n_lags):
        print("x%i: Log ILLIQ with %i days lag" % (j + 1, lags[j]))
        x = supp.mean_for_n_entries(log_illiq_days_clean, lags[j])
        x = x[len(x) - n_entries: len(x)]
        for i in range(0, n_entries):
            X[i, j] = x[i]

    j = n_lags
    print("x%i: Returns" % (j+1))
    for i in range(0, n_entries):
        X[i, j] = returns_days_clean[i]

    j += 1
    print("x%i: Returns with 1 lag" % (j+1))
    for i in range(0, n_entries):
        X[i, j] = returns_days_clean[i - 1]

    j += 1
    print("x%i: Log Volumes (normalized)" % (j+1))
    for i in range(0, n_entries):
        X[i, j] = log_volumes_days_clean[i]

    j += 1
    print("x%i: Log Volumes (normalized) with 1 lag" % (j + 1))
    for i in range(0, n_entries):
        X[i, j] = log_volumes_days_clean[i]

    j += 1
    print("x%i: Log Realized Volatility" % (j+1))
    for i in range(0, n_entries):
        X[i, j] = log_volatility_days_clean[i]

    j += 1
    print("x%i: Log Realized Volatility with 1 lag" % (j + 1))
    for i in range(0, n_entries):
        X[i, j] = log_volatility_days_clean[i - 1]

    print()
    linreg.reg_multiple_pandas(Y, X)


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
