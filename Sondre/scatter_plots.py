import numpy as np
import data_import as di
import plot
import data_import_support as dis
from matplotlib import pyplot as plt
import linreg

# Opening hours only
exchanges, time_list_minutes, prices_minutes, volumes_minutes = di.get_lists_legacy(opening_hours="y", make_totals="n")
# Removes all days with no volume, volatility or spread
time_list_days_clean, time_list_removed, returns_days_clean, volumes_days_clean, log_volumes_days_clean, spread_days_clean, \
illiq_days_clean, log_illiq_days_clean, volatility_days_clean, log_volatility_days_clean = dis.clean_series_days(
    time_list_minutes, prices_minutes,
    volumes_minutes)


# Getting stds and means for parameters:
spread_std_day = np.std(spread_days_clean)
spread_mean_day = np.mean(spread_days_clean)
log_volume_std_day = np.std(log_volumes_days_clean)
log_volume_mean_day = np.mean(log_volumes_days_clean)
returns_std_day = np.std(returns_days_clean)
returns_mean_day = np.mean(returns_days_clean)
log_illiq_std_day = np.std(illiq_days_clean)
log_illiq_mean_day = np.mean(illiq_days_clean)
log_volatility_std = np.std(log_volatility_days_clean)
log_volatility_mean = np.mean(log_volatility_days_clean)

# Whether to run plots
roll_v_return = 0
roll_v_volumes = 0
roll_v_volatility = 0
return_v_volumes = 0
illiq_v_volume = 0
illiq_v_return = 0
roll_v_illiq = 0
illiq_v_volatility = 0

print()

y_data = spread_days_clean
y_lims = [min(y_data), max(y_data)]

x_data = volatility_days_clean
x_lims = [min(x_data), max(x_data)]
plot.scatters(x_data, y_data, x_log=1, x_perc=1, y_perc=1, show_plot=0, xlims=x_lims, ylims=y_lims, title="spread_vol")
plot.plt.ylabel("Spread")
plot.plt.xlabel("Annualized Volatility")
linreg.univariate_with_print(y_data, x_data, x_lims=x_lims)

x_data = returns_days_clean
x_lims = [min(x_data), max(x_data)]
plot.scatters(x_data, y_data, x_log=0, x_perc=1, y_perc=1, show_plot=0, xlims=x_lims, ylims=y_lims, title="spread_returns")
plot.plt.ylabel("Spread")
plot.plt.xlabel("Returns")
linreg.univariate_with_print(y_data, x_data, x_lims=x_lims)

x_data = log_volumes_days_clean
x_lims = [min(x_data), max(x_data)]
plot.scatters(x_data, y_data, x_log=0, x_perc=0, y_perc=1, show_plot=0, xlims=x_lims, ylims=y_lims, title="spread_volume")
plot.plt.ylabel("Spread")
plot.plt.xlabel("Normalized Volumes")
linreg.univariate_with_print(y_data, x_data, x_lims=x_lims)


y_data = illiq_days_clean
y_lims = [min(y_data), max(y_data)]

x_data = volatility_days_clean
x_lims = [min(x_data), max(x_data)]
plot.scatters(x_data, y_data, x_log=1, x_perc=1, y_log=1, y_perc=1, show_plot=0, xlims=x_lims, ylims=y_lims, title="illiq_vol")
plot.plt.ylabel("ILLIQ")
plot.plt.xlabel("Annualized Volatility")
linreg.univariate_with_print(y_data, x_data, x_lims=x_lims)

x_data = returns_days_clean
x_lims = [min(x_data), max(x_data)]
plot.scatters(x_data, y_data, x_log=0, x_perc=1, y_log=1,  y_perc=1, show_plot=0, xlims=x_lims, ylims=y_lims, title="illiq_returns")
plot.plt.ylabel("ILLIQ")
plot.plt.xlabel("Returns")
linreg.univariate_with_print(y_data, x_data, x_lims=x_lims)

x_data = log_volumes_days_clean
x_lims = [min(x_data), max(x_data)]
plot.scatters(x_data, y_data, x_log=0, x_perc=0,  y_log=1, y_perc=1, show_plot=0, xlims=x_lims, ylims=y_lims, title="illiq_volumes")
plot.plt.ylabel("ILLIQ")
plot.plt.xlabel("Normalized Volumes")
linreg.univariate_with_print(y_data, x_data, x_lims=x_lims)

if roll_v_return == 1:
    x_mean = returns_mean_day
    x_std = returns_std_day
    x_lims = [x_mean - x_std, x_mean + x_std]
    plot.scatters(returns_days_clean, spread_days_clean, show_plot=0, xtitle="Returns daily", ytitle="Spread daily",
                  ylims=y_lims, xlims=x_lims, x_perc=1, y_perc=1)

    # Regression lines
    slope, intercept, r_value, p_value, stderr = linreg.linreg_coeffs(returns_days_clean, spread_days_clean)
    plot.regression_line(intercept, slope, xlims=x_lims)
    reg_text = "R^2: " + str(r_value ** 2) + "  P-value: " + str(p_value)
    print("Roll - Return:")
    linreg.stats(slope, intercept, r_value, p_value)

    plot.plot_x_zero(x_lims)


if roll_v_volumes == 1:
    x_lims = [min(log_volumes_days_clean), max(log_volumes_days_clean)]
    plot.scatters(log_volumes_days_clean, spread_days_clean, show_plot=0, xtitle="Volumes daily (transformed)",
                  ytitle="Spread daily",
                  ylims=y_lims, xlims=x_lims, x_log=0, y_perc=1)

    # Regression lines
    slope, intercept, r_value, p_value, stderr = linreg.linreg_coeffs(log_volumes_days_clean, spread_days_clean)
    plot.regression_line(intercept, slope, xlims=x_lims)
    print("Roll - Volume (transformed):")
    linreg.stats(slope, intercept, r_value, p_value)

if roll_v_volatility == 1:
    x_lims = [min(volatility_days_clean), max(volatility_days_clean)]
    plot.scatters(volatility_days_clean, spread_days_clean, show_plot=0, xtitle="Log volatility, annualized",
                  ytitle="Spread daily",
                  ylims=y_lims, xlims=x_lims, x_log=1, x_perc=1, y_perc=1)

    # Regression lines
    slope, intercept, r_value, p_value, stderr = linreg.linreg_coeffs(log_volatility_days_clean, spread_days_clean)
    #plot.regression_line(intercept, slope, xlims=x_lims)
    print("Roll - Log volatility:")
    linreg.stats(slope, intercept, r_value, p_value)


if roll_v_illiq == 1:

    x_lims = [min(illiq_days_clean), max(illiq_days_clean)]
    y_mean = spread_mean_day
    y_std = spread_std_day
    y_lims = [0, y_mean + y_std]
    plot.scatters(illiq_days_clean, spread_days_clean, show_plot=0, xtitle="Log ILLIQ", ytitle="Spread daily",
                  ylims=y_lims, xlims=x_lims, x_log=1, x_perc=1, y_perc=1)

    # Regression lines
    slope, intercept, r_value, p_value, stderr = linreg.linreg_coeffs(log_illiq_days_clean, spread_days_clean)
    plot.regression_line(intercept, slope, xlims=x_lims)
    print("Spread - log ILLIQ:")
    linreg.stats(slope, intercept, r_value, p_value)

if illiq_v_return == 1:
    y_lims = [min(illiq_days_clean), max(illiq_days_clean)]
    x_mean = returns_mean_day
    x_std = returns_std_day
    x_lims = [x_mean - x_std, x_mean + x_std]
    plot.scatters(returns_days_clean, illiq_days_clean, show_plot=0, xtitle="Returns daily", ytitle="Log ILLIQ",
                  ylims=y_lims, xlims=x_lims, x_perc=1, y_log=1, y_perc=1)
    # Regression lines
    slope, intercept, r_value, p_value, stderr = linreg.linreg_coeffs(returns_days_clean, log_illiq_days_clean)
    plot.regression_line(intercept, slope, xlims=x_lims)
    print("log ILLIQ - Return:")
    linreg.stats(slope, intercept, r_value, p_value)

    plot.plot_x_zero(x_lims)

if illiq_v_volume == 1:

    x_lims = [min(log_volumes_days_clean), max(log_volumes_days_clean)]
    plot.scatters(log_volumes_days_clean, illiq_days_clean, show_plot=0, xtitle="Log volumes", ytitle="Log ILLIQ",
                  ylims=y_lims, xlims=x_lims, x_log=0, y_log=1, y_perc=1)
    # Regression lines
    slope, intercept, r_value, p_value, stderr = linreg.linreg_coeffs(log_volumes_days_clean, log_illiq_days_clean)
    plot.regression_line(intercept, slope, xlims=x_lims)
    print("Log ILLIQ - Log Volume:")
    linreg.stats(slope, intercept, r_value, p_value)

if illiq_v_volatility == 1:

    x_lims = [min(volatility_days_clean), max(volatility_days_clean)]
    plot.scatters(volatility_days_clean, illiq_days_clean, show_plot=0, xtitle="Log volatility annualized",
                  ytitle="Log ILLIQ",
                  ylims=y_lims, xlims=x_lims, x_log=1, x_perc=1, y_log=1, y_perc=1)
    # Regression lines
    slope, intercept, r_value, p_value, stderr = linreg.linreg_coeffs(log_volatility_days_clean, log_illiq_days_clean)
    plot.regression_line(intercept, slope, xlims=x_lims)
    print("Log ILLIQ - Log volatility:")
    linreg.stats(slope, intercept, r_value, p_value)

plt.show()
