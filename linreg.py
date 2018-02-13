import scipy.stats as scistat
import numpy as np
import statsmodels.api as sm
import statsmodels.formula.api as smf


def print_n(n):
    for i in range(n+1):
        print()


def reg_multiple(Y, X, intercept=1):
    if intercept ==1:
        X = sm.add_constant(X)
    reg_model = sm.OLS(Y, X).fit(cov_type="HC0")
    print(reg_model.summary())
    print(reg_model.params)
    print(reg_model.tvalues)
    print(reg_model.rsquared_adj)
    print(reg_model.aic)
    print(reg_model.pvalues) 
    print(reg_model.bse) #standard errors of the parameter estimates
    print_n(13)



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


def univariate_with_print(y, x, x_lims=[]):
    slope, intercept, r_value, p_value, stderr = linreg_coeffs(x, y)
    stats(slope, intercept, r_value, p_value)
