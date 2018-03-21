import numpy as np
import statsmodels.api as sm


def print_n(n):
    for i in range(n+1):
        print()


def reg_multiple(Y, X, intercept=1, prints=0):
    if intercept ==1:
        X = sm.add_constant(X)
    reg_model = sm.OLS(Y, X).fit(cov_type="HC0")

    if prints == 1:
        print(reg_model.summary())
    coeffs = reg_model.params
    tvalues = reg_model.tvalues
    rsquared=reg_model.rsquared_adj
    aic=reg_model.aic
    p_values = reg_model.pvalues
    std_errs = reg_model.bse
    n_obs = reg_model.nobs
    return coeffs, tvalues, rsquared, aic, p_values, std_errs, n_obs


def stats(slope: float, intercept: float, r_value: float, p_value: float):
    print("Intercept %0.4f:" % intercept)
    print("Slope: %0.4f" % slope)
    print("R-squared: %0.4f" % r_value ** 2)
    print("P-value: %0.4f" % p_value)
    print()


def autocorr_linreg(in_list, n_lags, max_lag=0):
    if max_lag == 0:
        adj = 0
    else:
        adj = max_lag - n_lags
    n_entries = len(in_list) - n_lags - adj
    X = np.zeros([n_entries, n_lags])
    for lag in range(0, n_lags):
        for i in range(0, n_entries):
            X[i, lag] = in_list[i + lag + 1]
    Y = in_list[0: n_entries]
    reg_multiple(Y, X)


