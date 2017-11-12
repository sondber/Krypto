import numpy as np
import data_import as di
import plot
import rolls
from Jacob import jacob_support as jake_supp
from Sondre import sondre_support_formulas as supp
import data_import_support as dis
from matplotlib import pyplot as plt
import ILLIQ
import linreg

# Opening hours only
exchanges, time_list_minutes, prices_minutes, volumes_minutes = di.get_lists(opening_hours="y", make_totals="n")
# Removes all days with no volume, volatility or spread
time_list_days_clean, time_list_removed, returns_days_clean, volumes_days_clean, log_volumes_days_clean, spread_days_clean, \
illiq_days_clean, log_illiq_days_clean, volatility_days_clean, log_volatility_days_clean = dis.clean_trans_2013(
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
roll_v_return = 1
roll_v_volumes = 1
roll_v_volatility = 1
return_v_volumes = 1
amihud_v_volume = 1
roll_v_return_w_volumes = 0
amihud_v_return = 1
roll_v_amihud = 1
amihud_v_volatility = 1

y_mean = spread_mean_day
y_std = spread_std_day
y_lims = [0, y_mean + y_std]
fig_count = 1

if roll_v_return == 1:
    # Rolls v Returns
    plt.figure(fig_count)
    x_mean = returns_mean_day
    x_std = returns_std_day
    x_lims = [x_mean - x_std, x_mean + x_std]
    plt.title("Bid/ask spread vs. Daily returns")
    plot.scatters(returns_days_clean, spread_days_clean, show_plot=0, xtitle="Returns daily", ytitle="Spread daily",
                  ylims=y_lims, xlims=x_lims, perc1=1, perc2=1)

    # Regression lines
    slope, intercept, r_value, p_value, stderr = linreg.linreg_coeffs(returns_days_clean, spread_days_clean)
    plot.regression_line(intercept, slope, xlims=x_lims)
    reg_text = "R^2: " + str(r_value ** 2) + "  P-value: " + str(p_value)
    print("Roll - Return:")
    linreg.stats(slope, intercept, r_value, p_value)

    plot.plot_y_zero(x_lims)

    fig_count += 1

if roll_v_volumes == 1:
    # Rolls v log-volumes
    plt.figure(fig_count)

    x_lims = [min(log_volumes_days_clean), max(log_volumes_days_clean)]
    plt.title("Bid/ask spread vs. daily traded volumes")
    plot.scatters(log_volumes_days_clean, spread_days_clean, show_plot=0, xtitle="Volumes daily (transformed)",
                  ytitle="Spread daily",
                  ylims=y_lims, xlims=x_lims, log1=1, perc2=1)

    # Regression lines
    slope, intercept, r_value, p_value, stderr = linreg.linreg_coeffs(log_volumes_days_clean, spread_days_clean)
    plot.regression_line(intercept, slope, xlims=x_lims)
    print("Roll - Volume (transformed):")
    linreg.stats(slope, intercept, r_value, p_value)

    fig_count += 1

if roll_v_volatility == 1:
    # Rolls v Volatility

    plt.figure(fig_count)
    x_lims = [min(log_volatility_days_clean), max(log_volatility_days_clean)]
    plt.title("Bid/ask spread vs. log volatility")
    plot.scatters(log_volatility_days_clean, spread_days_clean, show_plot=0, xtitle="Log volatility, annualized",
                  ytitle="Spread daily",
                  ylims=y_lims, xlims=x_lims, log1=1, perc2=1)

    # Regression lines
    slope, intercept, r_value, p_value, stderr = linreg.linreg_coeffs(log_volatility_days_clean, spread_days_clean)
    plot.regression_line(intercept, slope, xlims=x_lims)
    print("Roll - Log volatility:")
    linreg.stats(slope, intercept, r_value, p_value)

    fig_count += 1

if return_v_volumes == 1:
    # Returns v Volumes
    plt.figure(fig_count)

    y_mean = returns_mean_day
    y_std = returns_std_day
    y_lims = [y_mean - y_std, y_mean + y_std]
    x_lims = [min(log_volumes_days_clean), max(log_volumes_days_clean)]
    plt.title("Daily returns vs. Volumes (transformed)")
    plot.scatters(log_volumes_days_clean, returns_days_clean, show_plot=0, xtitle="Volumes daily (transformed)",
                  ytitle="Returns daily",
                  ylims=y_lims, xlims=x_lims, log1=1, perc2=1)

    # Regression lines
    slope, intercept, r_value, p_value, stderr = linreg.linreg_coeffs(log_volumes_days_clean, returns_days_clean)
    plot.regression_line(intercept, slope, xlims=x_lims)

    print("Return - Volume (transformed):")
    linreg.stats(slope, intercept, r_value, p_value)
    plot.plot_x_zero(x_lims)

    fig_count += 1

if roll_v_amihud == 1:
    # Rolls v Amihud (ILLIQ)
    plt.figure(fig_count)

    x_lims = [min(log_illiq_days_clean), max(log_illiq_days_clean)]
    y_mean = spread_mean_day
    y_std = spread_std_day
    y_lims = [0, y_mean + y_std]
    plt.title("Spread vs. log ILLIQ")
    plot.scatters(log_illiq_days_clean, spread_days_clean, show_plot=0, xtitle="Log ILLIQ", ytitle="Spread daily",
                  ylims=y_lims, xlims=x_lims, log1=1, perc2=1)

    # Regression lines
    slope, intercept, r_value, p_value, stderr = linreg.linreg_coeffs(log_illiq_days_clean, spread_days_clean)
    plot.regression_line(intercept, slope, xlims=x_lims)
    print("Spread - log ILLIQ:")
    linreg.stats(slope, intercept, r_value, p_value)

    fig_count += 1

if amihud_v_return == 1:
    # Amihud v returns
    plt.figure(fig_count)
    y_lims = [min(log_illiq_days_clean), max(log_illiq_days_clean)]
    x_mean = returns_mean_day
    x_std = returns_std_day
    x_lims = [x_mean - x_std, x_mean + x_std]
    plt.title("Log ILLIQ vs. Daily returns")
    plot.scatters(returns_days_clean, log_illiq_days_clean, show_plot=0, xtitle="Returns daily", ytitle="Log ILLIQ",
                  ylims=y_lims, xlims=x_lims, perc1=1, log2=1)
    # Regression lines
    slope, intercept, r_value, p_value, stderr = linreg.linreg_coeffs(returns_days_clean, log_illiq_days_clean)
    plot.regression_line(intercept, slope, xlims=x_lims)
    print("log ILLIQ - Return:")
    linreg.stats(slope, intercept, r_value, p_value)

    plot.plot_y_zero(x_lims)

    fig_count += 1

if amihud_v_volume == 1:
    # Amihud v Volumes
    plt.figure(fig_count)

    x_lims = [min(log_volumes_days_clean), max(log_volumes_days_clean)]
    plt.title("Log ILLIQ vs. log traded volumes")
    plot.scatters(log_volumes_days_clean, log_illiq_days_clean, show_plot=0, xtitle="Log volumes", ytitle="Log ILLIQ",
                  ylims=y_lims, xlims=x_lims, log1=1, log2=1)
    # Regression lines
    slope, intercept, r_value, p_value, stderr = linreg.linreg_coeffs(log_volumes_days_clean, log_illiq_days_clean)
    plot.regression_line(intercept, slope, xlims=x_lims)
    print("Log ILLIQ - Log Volume:")
    linreg.stats(slope, intercept, r_value, p_value)
    fig_count += 1

if amihud_v_volatility == 1:
    # Amihud v Voatility
    plt.figure(fig_count)

    x_lims = [min(log_volatility_days_clean), max(log_volatility_days_clean)]
    plt.title("Log ILLIQ vs. Log volatiltiy")
    plot.scatters(log_volatility_days_clean, log_illiq_days_clean, show_plot=0, xtitle="Log volatility annualized",
                  ytitle="Log ILLIQ",
                  ylims=y_lims, xlims=x_lims, log1=1, log2=1)
    # Regression lines
    slope, intercept, r_value, p_value, stderr = linreg.linreg_coeffs(log_volatility_days_clean, log_illiq_days_clean)
    plot.regression_line(intercept, slope, xlims=x_lims)
    print("Log ILLIQ - Log volatility:")
    linreg.stats(slope, intercept, r_value, p_value)
    fig_count += 1

plt.show()
