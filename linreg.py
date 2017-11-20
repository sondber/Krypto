import scipy.stats as scistat
from sklearn import linear_model
import pandas as pd
import numpy as np
from Sondre import sondre_support_formulas as supp
import statsmodels.api as sm


def reg_multiple_x(Y, X):
    # X is a n x m matrix, where n is number of observations, m is number of explanatory variables
    # Y is a n x 1 matrix
    regr = linear_model.LinearRegression()
    regr.fit(X, Y)
    slopes = regr.coef_
    r_squared = regr.score(X, Y)
    intercept = regr.intercept_
    return slopes, intercept, r_squared


def reg_multiple_pandas(Y, X):
    X = sm.add_constant(X)
    reg_model = sm.OLS(Y, X).fit()
    print(reg_model.summary())


def linreg_coeffs(x, y):  # input is equal length one-dim arrays of measurements
    parameters = scistat.linregress(x, y)
    slope = parameters[0]  # slope of the regression line
    intercept = parameters[1]  # intercept of the regression line
    r_value = parameters[2]  # correlation coefficient, remember to square for R-squared
    p_value = parameters[3]  # two-sided p-value for a hypothesis test whose null hyp is slope zero
    stderr = parameters[4]  # standard error of the estimate
    return slope, intercept, r_value, p_value, stderr


def stats(slope: float, intercept: float, r_value: float, p_value: float):
    print("Intercept %0.4f:" % intercept)
    print("Slope: %0.4f" % slope)
    print("R-squared: %0.4f" % r_value ** 2)
    print("P-value: %0.4f" % p_value)
    print()


def autocorr_linreg(in_list, n_lags):
    n_entries = len(in_list) - n_lags
    X = np.zeros([n_entries, n_lags])
    for lag in range(0, n_lags):
        for i in range(0, n_entries):
            X[i, lag] = in_list[i + lag + 1]
    Y = in_list[0: len(in_list) - n_lags]
    reg_multiple_pandas(Y, X)

