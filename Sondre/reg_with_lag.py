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


os.chdir("/Users/sondre/Documents/GitHub/krypto")
exchanges, time_list_minutes, prices_minutes, volumes_minutes = di.get_lists(opening_hours="y", make_totals="n")
time_list_days_clean, time_list_removed, returns_days_clean, volumes_days_clean, log_volumes_days_clean, spread_days_clean, \
illiq_days_clean, log_illiq_days_clean, volatility_days_clean, log_volatility_days_clean = dis.clean_trans_2013(
    time_list_minutes, prices_minutes,
    volumes_minutes)

autoreg = 1
if autoreg == 1:
    print_n(20)
    print("Rolls regression:")
    linreg.autocorr_linreg(spread_days_clean, 12)
    print_n(5)
    print("Log-ILLIQ regression:")
    linreg.autocorr_linreg(log_illiq_days_clean, 12)

har = 1
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
