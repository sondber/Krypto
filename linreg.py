import scipy.stats as scistat


def linreg_coeffs(arr1, arr2):  # input is equal length one-dim arrays of measurements
    parameters = scistat.linregress(arr1, arr2)
    slope = parameters[0]  # slope of the regression line
    intercept = parameters[1]  # intercept of the regression line
    r_value = parameters[2]  # correlation coefficient, remember to square for R-squared
    p_value = parameters[3]  # two-sided p-value for a hypothesis test whose null hyp is slope zero
    stderr = parameters[4]  # standard error of the estimate
    return slope, intercept, r_value, p_value, stderr


def stats(slope, intercept, r_value, p_value):
    print("Intercept %0.4f:" % intercept)
    print("Slope %0.4f:" % slope)
    print("R-squared: %0.4f" % r_value ** 2)
    print("P-value: %0.4f" % p_value)
    print()
