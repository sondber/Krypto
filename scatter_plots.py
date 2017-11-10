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
time_list_hours, prices_hours, volumes_hours = dis.convert_to_hour(time_list_minutes, prices_minutes, volumes_minutes)
time_list_days, prices_days, volumes_days = dis.convert_to_day(time_list_minutes, prices_minutes, volumes_minutes)


mean_volume_2012 = np.mean(volumes_days[0, 0:261])

n_days = len(time_list_days)
n_hours = len(time_list_hours)
n_mins = len(time_list_minutes)
cutoff_day = 261
cutoff_hour = cutoff_day * 7
cutoff_min = cutoff_day * 390
print("Only including days after", time_list_days[cutoff_day])
print("Only including days after", time_list_hours[cutoff_hour])
print("Only including days after", time_list_minutes[cutoff_min])

# Bistamp only, cutoff day
prices_minutes = prices_minutes[0, cutoff_min:n_mins]
volumes_minutes = volumes_minutes[0, cutoff_min:n_mins]
prices_hours = prices_hours[0, cutoff_hour:n_hours]
volumes_hours = volumes_hours[0, cutoff_hour:n_hours]
prices_days = prices_days[0, cutoff_day:n_days]
volumes_days = volumes_days[0, cutoff_day:n_days]
time_list_days = time_list_days[cutoff_day:n_days]


daily_scatters = 1
if daily_scatters == 1:
    print("Generating scatters with daily data...")

    # Rolls
    spread_abs, spread_days, time_list_rolls, count_value_error = rolls.rolls(prices_minutes, time_list_minutes, calc_basis=1, kill_output=1)
    # Realized volatility
    volatility_days = ILLIQ.daily_Rv(time_list_minutes, prices_minutes)
    # Annualize the volatility
    anlzd_volatility_days = np.multiply(volatility_days, 252 ** 0.5)
    # Returns
    returns_days = jake_supp.logreturn(prices_days)
    # Amihud's ILLIQ
    illiq_days = ILLIQ.ILLIQ_nyse_day(prices_hours, volumes_hours)
    # --------------------------------------------

    n_initial = len(time_list_days)
    print("Total number of days:", n_initial)
    # Removing all days where Volume is zero
    volumes_days_no_zero, spread_days_no_zero, returns_days_no_zero, illiq_days_no_zero = \
        supp.remove_list1_zeros_from_all_lists(volumes_days, spread_days, returns_days, illiq_days)
    volumes_days_no_zero, time_list_days_no_zero, anlzd_volatility_days_no_zero = \
        supp.remove_list1_zeros_from_all_lists(volumes_days, time_list_days, anlzd_volatility_days)

    n_no_zerovolume = len(time_list_days_no_zero)
    print("Total number of days:", n_no_zerovolume)

    # Removing all days where ROll is zero
    spread_days_no_zero, volumes_days_no_zero, returns_days_no_zero, illiq_days_no_zero = \
        supp.remove_list1_zeros_from_all_lists(spread_days_no_zero, volumes_days_no_zero, returns_days_no_zero, illiq_days_no_zero)
    spread_days_no_zero, time_list_days_no_zero, anlzd_volatility_days_no_zero = \
        supp.remove_list1_zeros_from_all_lists(spread_days_no_zero, time_list_days_no_zero, anlzd_volatility_days_no_zero)

    n_no_zeroroll = len(time_list_days_no_zero)
    print("Total number of days:", n_no_zeroroll)

    # Removing all days where Volatility is zero from the lists where Roll=0 has already been removed
    anlzd_volatility_days_no_zero, volumes_days_no_zero, returns_days_no_zero, illiq_days_no_zero = \
        supp.remove_list1_zeros_from_all_lists(anlzd_volatility_days_no_zero, volumes_days_no_zero, returns_days_no_zero, illiq_days_no_zero)
    anlzd_volatility_days_no_zero, spread_days_no_zero, time_list_days_no_zero = \
        supp.remove_list1_zeros_from_all_lists(anlzd_volatility_days_no_zero, spread_days_no_zero, time_list_days_no_zero)

    n_no_zerorvol = len(time_list_days_no_zero)
    print("Total number of days:", n_no_zerorvol)

    # Turning ILLIQ, Volume and RVol into log
    illiq_days_no_zero = np.log(illiq_days_no_zero)
    anlzd_volatility_days_no_zero = np.log(anlzd_volatility_days_no_zero)
    volumes_days_no_zero = dis.volume_transformation(volumes_days_no_zero, mean_volume_2012)

    plt.plot(volumes_days_no_zero)

    # Getting stds and means for parameters:
    spread_std_day = np.std(spread_days_no_zero)
    spread_mean_day = np.mean(spread_days_no_zero)
    volume_std_day = np.std(volumes_days_no_zero)
    volume_mean_day = np.mean(volumes_days_no_zero)
    returns_std_day = np.std(returns_days_no_zero)
    returns_mean_day = np.mean(returns_days_no_zero)
    illiq_std_day = np.std(illiq_days_no_zero)
    illiq_mean_day = np.mean(illiq_days_no_zero)
    anlzd_volatility_std = np.std(anlzd_volatility_days_no_zero)
    anlzd_volatility_mean = np.mean(anlzd_volatility_days_no_zero)

    # Whether to run plots
    roll_v_return = 0
    roll_v_volumes = 1
    roll_v_volatility = 0
    return_v_volumes = 0
    amihud_v_volume = 0
    roll_v_return_w_volumes = 0
    amihud_v_return = 0
    roll_v_amihud = 0
    amihud_v_volatility = 0

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
        plot.scatters(returns_days_no_zero, spread_days_no_zero, show_plot=0, xtitle="Returns daily", ytitle="Spread daily",
                      ylims=y_lims, xlims=x_lims, perc1=1, perc2=1)

        # Regression lines
        slope, intercept, r_value, p_value, stderr = linreg.linreg_coeffs(returns_days_no_zero, spread_days_no_zero)
        plot.regression_line(intercept, slope, xlims=x_lims)
        print("Roll - Return:")
        linreg.stats(slope, intercept, r_value, p_value)

        plot.plot_y_zero(x_lims)

        fig_count += 1

    if roll_v_volumes == 1:
        # Rolls v Volumes
        plt.figure(fig_count)

        x_mean = volume_mean_day
        x_std = volume_std_day
        x_lims = [min(volumes_days_no_zero), max(volumes_days_no_zero)]
        plt.title("Bid/ask spread vs. daily traded volumes")
        plot.scatters(volumes_days_no_zero, spread_days_no_zero, show_plot=0, xtitle="Volumes daily (transformed)", ytitle="Spread daily",
                      ylims=y_lims, xlims=x_lims, perc1=0, perc2=1)

        # Regression lines
        slope, intercept, r_value, p_value, stderr = linreg.linreg_coeffs(volumes_days_no_zero, spread_days_no_zero)
        plot.regression_line(intercept, slope, xlims=x_lims)
        print("Roll - Volume:")
        linreg.stats(slope, intercept, r_value, p_value)

        fig_count += 1

    if roll_v_volatility == 1:
        # Rolls v Volatility

        plt.figure(fig_count)
        x_mean = anlzd_volatility_mean
        x_std = anlzd_volatility_std
        #x_lims = [x_mean - x_std, x_mean + x_std]
        x_lims = [min(anlzd_volatility_days_no_zero), max(anlzd_volatility_days_no_zero)]
        plt.title("Bid/ask spread vs. log volatility")
        plot.scatters(anlzd_volatility_days_no_zero, spread_days_no_zero, show_plot=0, xtitle="Log volatility, annualized", ytitle="Spread daily",
                      ylims=y_lims, xlims=x_lims, perc1=0, perc2=1)

        # Regression lines
        slope, intercept, r_value, p_value, stderr = linreg.linreg_coeffs(anlzd_volatility_days_no_zero, spread_days_no_zero)
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
        x_mean = volume_mean_day
        x_std = volume_std_day
        x_lims = [min(volumes_days_no_zero), max(volumes_days_no_zero)]
        plt.title("Daily returns vs. Daily traded volumes")
        plot.scatters(volumes_days_no_zero, returns_days_no_zero, show_plot=0, xtitle="Volumes daily [BTC]", ytitle="Returns daily",
                      ylims=y_lims, xlims=x_lims, perc1=0, perc2=1)

        # Regression lines
        slope, intercept, r_value, p_value, stderr = linreg.linreg_coeffs(volumes_days_no_zero, returns_days_no_zero)
        plot.regression_line(intercept, slope, xlims=x_lims)

        print("Return - Volume:")
        linreg.stats(slope, intercept, r_value, p_value)
        plot.plot_x_zero(x_lims)

        fig_count += 1

    if roll_v_return_w_volumes == 1:
        # Rolls v Returns w/ volume as size
        plt.figure(fig_count)

        x_mean = returns_mean_day
        x_std = returns_std_day
        x_lims = [x_mean - x_std, x_mean + x_std]

        y_mean = spread_mean_day
        y_std = spread_std_day
        y_lims = [0, y_mean + y_std]

        plt.title("Bid/ask spread vs. Daily returns")
        plot.scatters(returns_days_no_zero, spread_days_no_zero, show_plot=0, xtitle="Returns daily (%)", ytitle="Spread daily (%)",
                      ylims=y_lims, xlims=x_lims, areas=volumes_days_no_zero, label="Bubble size = traded volume", perc1=1, perc2=1)

        # Regression lines
        slope, intercept, r_value, p_value, stderr = linreg.linreg_coeffs(returns_days_no_zero, spread_days_no_zero)
        plot.regression_line(intercept, slope, xlims=x_lims)
        plot.plot_y_zero(x_lims)

        fig_count += 1

    if roll_v_amihud == 1:
        # Rolls v Amihud (ILLIQ)
        plt.figure(fig_count)

        x_mean = illiq_mean_day
        x_std = illiq_std_day
        #x_lims = [x_mean - x_std, x_mean + x_std]
        x_lims = [min(illiq_days_no_zero), max(illiq_days_no_zero)]
        plt.title("Rolls vs. log ILLIQ")
        plot.scatters(illiq_days_no_zero, spread_days_no_zero, show_plot=0, xtitle="Log ILLIQ", ytitle="Spread daily",
                      ylims=y_lims, xlims=x_lims, perc1=0, perc2=1)

        # Regression lines
        slope, intercept, r_value, p_value, stderr = linreg.linreg_coeffs(illiq_days_no_zero, spread_days_no_zero)
        plot.regression_line(intercept, slope, xlims=x_lims)
        print("Roll - Amihud:")
        linreg.stats(slope, intercept, r_value, p_value)

        fig_count += 1

    if amihud_v_return == 1:
        # Amihud v returns
        plt.figure(fig_count)
        y_mean = illiq_mean_day
        y_std = illiq_std_day
        #y_lims = [y_mean - y_std, y_mean + y_std]
        y_lims = [min(illiq_days_no_zero), max(illiq_days_no_zero)]
        x_mean = returns_mean_day
        x_std = returns_std_day
        x_lims = [x_mean - x_std, x_mean + x_std]
        plt.title("Log ILLIQ vs. Daily returns")
        plot.scatters(returns_days_no_zero, illiq_days_no_zero, show_plot=0, xtitle="Returns daily", ytitle="Log ILLIQ",
                      ylims=y_lims, xlims=x_lims, perc1=1, perc2=0)
        # Regression lines
        slope, intercept, r_value, p_value, stderr = linreg.linreg_coeffs(returns_days_no_zero, illiq_days_no_zero)
        plot.regression_line(intercept, slope, xlims=x_lims)
        print("Amihud - Return:")
        linreg.stats(slope, intercept, r_value, p_value)

        plot.plot_y_zero(x_lims)

        fig_count += 1

    if amihud_v_volume == 1:
        # Amihud v Volumes
        plt.figure(fig_count)

        x_mean = volume_mean_day
        x_std = volume_std_day
        x_lims = [min(volumes_days_no_zero), max(volumes_days_no_zero)]
        plt.title("Log ILLIQ vs. daily traded volumes")
        plot.scatters(volumes_days_no_zero, illiq_days_no_zero, show_plot=0, xtitle="Volumes daily (BTC)", ytitle="Log ILLIQ",
                      ylims=y_lims, xlims=x_lims, perc1=0, perc2=0)
        # Regression lines
        slope, intercept, r_value, p_value, stderr = linreg.linreg_coeffs(volumes_days_no_zero, illiq_days_no_zero)
        plot.regression_line(intercept, slope, xlims=x_lims)
        print("Log ILLIQ - Volume:")
        linreg.stats(slope, intercept, r_value, p_value)

        fig_count += 1

    if amihud_v_volatility == 1:
        # Amihud v Voatility
        plt.figure(fig_count)

        x_mean = anlzd_volatility_mean
        x_std = anlzd_volatility_std
        #x_lims = [x_mean - x_std, x_mean + x_std]
        x_lims = [min(anlzd_volatility_days_no_zero), max(anlzd_volatility_days_no_zero)]
        plt.title("Log ILLIQ vs. Log volatiltiy")
        plot.scatters(anlzd_volatility_days_no_zero, illiq_days_no_zero, show_plot=0, xtitle="Log volatility annualized", ytitle="Log ILLIQ",
                      ylims=y_lims, xlims=x_lims, perc1=0, perc2=0)
        # Regression lines
        slope, intercept, r_value, p_value, stderr = linreg.linreg_coeffs(anlzd_volatility_days_no_zero, illiq_days_no_zero)
        plot.regression_line(intercept, slope, xlims=x_lims)
        print("Log ILLIQ - Log volatility:")
        linreg.stats(slope, intercept, r_value, p_value)

        fig_count += 1

plt.show()
