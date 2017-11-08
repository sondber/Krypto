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
# Bistamp only

exchanges, time_list_minutes, prices_minutes, volumes_minutes = di.get_lists(opening_hours="y", make_totals="n")
time_list_hours, prices_hours, volumes_hours = dis.convert_to_hour(time_list_minutes, prices_minutes, volumes_minutes)
time_list_daily, prices_daily, volumes_daily = dis.convert_to_day(time_list_minutes, prices_minutes, volumes_minutes)

daily_scatters = 1
if daily_scatters == 1:
    print("Generating scatters with daily data...")

    # Getting rolls estimator
    print("Number of days in set:", len(time_list_daily))

    spread_abs, spread_daily, time_list_rolls, count_value_error = rolls.rolls(prices_minutes[0, :], time_list_minutes, calc_basis=1, kill_output=1)
    print(" Spread_daily is given as percentage")
    volatility_day = ILLIQ.daily_Rv(time_list_minutes, prices_minutes[0, :])
    anlzd_volatility_day = np.multiply(volatility_day, 250 ** 0.5)
    print(" Volatility_daily is given as percentage")

    # Extracing BitstampUSD
    returns_daily = jake_supp.logreturn(prices_daily[0, :])  # <-- bistamp only
    print(" Returns_daily is given as percentage")
    volumes_daily = volumes_daily[0, :]  # bitstamp only
    illiq_daily = ILLIQ.ILLIQ_nyse_day(prices_hours[0, :], volumes_hours[0, :])  # bitstamp only
    print(" Illiq_daily is given as percentage")
    # --------------------

    spread_std_day = np.std(spread_daily)
    spread_mean_day = np.mean(spread_daily)
    volume_std_day = np.std(volumes_daily)
    volume_mean_day = np.mean(volumes_daily)
    returns_std_day = np.std(returns_daily)
    returns_mean_day = np.mean(returns_daily)
    illiq_std_day = np.std(illiq_daily)
    illiq_mean_day = np.mean(illiq_daily)

    # Vil her utelate dag 330-335 fordi de er helt trash
    anlzd_vol_excluding_extremes = anlzd_volatility_day[0:330]
    time_excl_extremes = time_list_daily[0:330]
    spread_excl_extremes = spread_daily[0:330]
    illiq_excl_extremes = illiq_daily[0:330]
    np.append(anlzd_vol_excluding_extremes, anlzd_volatility_day[336:len(anlzd_volatility_day)])
    np.append(time_excl_extremes, time_list_daily[336:len(volatility_day)])
    np.append(spread_excl_extremes, spread_daily[336:len(volatility_day)])
    np.append(illiq_excl_extremes, illiq_daily[336:len(volatility_day)])

    anlzd_volatility_std_excl_extremes = np.std(anlzd_vol_excluding_extremes)
    anlzd_volatility_mean_excl_extremes = np.mean(anlzd_vol_excluding_extremes)

    y_mean = spread_mean_day
    y_std = spread_std_day
    y_lims = [0, y_mean + y_std]

    fig_count = 1

    roll_v_return = 1
    roll_v_volumes = 0
    roll_v_volatility = 0
    return_v_volumes = 0
    amihud_v_volume = 0
    roll_v_return_w_volumes = 0
    amihud_v_return = 0
    roll_v_amihud = 1
    amihud_v_volatility = 0

    # removing outliers from amihud, rolls, return
    illiq_daily, spread_daily, returns_daily = supp.remove_list1_outliers_from_all_lists(illiq_daily, spread_daily, returns_daily)


    print()
    print()

    if roll_v_return == 1:
        # Rolls v Returns
        plt.figure(fig_count)
        x_mean = returns_mean_day
        x_std = returns_std_day
        x_lims = [x_mean - x_std, x_mean + x_std]
        plt.title("Bid/ask spread vs. Daily returns")
        plot.scatters(returns_daily, spread_daily, show_plot=0, xtitle="Returns daily", ytitle="Spread daily",
                      ylims=y_lims, xlims=x_lims, perc1=1, perc2=1)

        # Regression lines
        slope, intercept, r_value, p_value, stderr = linreg.linreg_coeffs(returns_daily, spread_daily)
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
        x_lims = [0, x_mean + x_std]
        plt.title("Bid/ask spread vs. daily traded volumes")
        plot.scatters(volumes_daily, spread_daily, show_plot=0, xtitle="Volumes daily [BTC]", ytitle="Spread daily",
                      ylims=y_lims, xlims=x_lims, perc1=0, perc2=1)

        # Regression lines
        slope, intercept, r_value, p_value, stderr = linreg.linreg_coeffs(volumes_daily, spread_daily)
        plot.regression_line(intercept, slope, xlims=x_lims)
        print("Roll - Volume:")
        linreg.stats(slope, intercept, r_value, p_value)

        fig_count += 1

    if roll_v_volatility == 1:
        # Rolls v Volatility
        plt.figure(fig_count)

        x_mean = anlzd_volatility_mean_excl_extremes
        x_std = anlzd_volatility_std_excl_extremes
        # x_lims = [0, x_mean + x_std]
        x_lims = [0, 0.0079]
        plt.title("Bid/ask spread vs. daily volatility")
        plot.scatters(volatility_day, spread_daily, show_plot=0, xtitle="Volatillity daily, annualized", ytitle="Spread daily",
                      ylims=y_lims, xlims=x_lims, perc1=1, perc2=1)

        # Regression lines
        slope, intercept, r_value, p_value, stderr = linreg.linreg_coeffs(anlzd_volatility_day, spread_daily)
        plot.regression_line(intercept, slope, xlims=x_lims)
        print("Roll - Volatility:")
        linreg.stats(slope, intercept, r_value, p_value)

        # Without extreme volatitlity values
        slope, intercept, r_value, p_value, stderr = linreg.linreg_coeffs(anlzd_vol_excluding_extremes, spread_excl_extremes)
        plot.regression_line(intercept, slope, xlims=x_lims)
        print("Roll - Volatility (excl. extreme volatitlty):")
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
        x_lims = [0, x_mean + x_std]
        plt.title("Daily returns vs. Daily traded volumes")
        plot.scatters(volumes_daily, returns_daily, show_plot=0, xtitle="Volumes daily [BTC]", ytitle="Returns daily (%)",
                      ylims=y_lims, xlims=x_lims, perc1=0, perc2=1)

        # Regression lines
        slope, intercept, r_value, p_value, stderr = linreg.linreg_coeffs(volumes_daily, returns_daily)
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
        plot.scatters(returns_daily, spread_daily, show_plot=0, xtitle="Returns daily (%)", ytitle="Spread daily (%)",
                      ylims=y_lims, xlims=x_lims, areas=volumes_daily, label="Bubble size = traded volume", perc1=1, perc2=1)

        # Regression lines
        slope, intercept, r_value, p_value, stderr = linreg.linreg_coeffs(returns_daily, spread_daily)
        plot.regression_line(intercept, slope, xlims=x_lims)
        plot.plot_y_zero(x_lims)

        fig_count += 1

    if roll_v_amihud == 1:
        # Rolls v Amihud (ILLIQ)
        plt.figure(fig_count)

        x_mean = np.mean(illiq_daily)
        x_std = np.std(illiq_daily)
        # x_lims = [0, x_mean + x_std]
        x_lims = [0, 0.0003]

        plt.title("Rolls vs. Amihud - Daily")
        plot.scatters(illiq_daily, spread_daily, show_plot=0, xtitle="Amihud daily (%)", ytitle="Spread daily (%)",
                      ylims=y_lims, xlims=x_lims, perc1=1, perc2=1)

        # Regression lines
        slope, intercept, r_value, p_value, stderr = linreg.linreg_coeffs(illiq_daily, spread_daily)
        plot.regression_line(intercept, slope, xlims=x_lims)
        print("Roll - Amihud:")
        linreg.stats(slope, intercept, r_value, p_value)

        fig_count += 1

    if amihud_v_return == 1:
        # Amihud v returns
        plt.figure(fig_count)
        y_mean = illiq_mean_day
        y_std = illiq_std_day
        #y_lims = [0, y_mean + y_std]
        y_lims = [0, 0.0003]
        x_mean = returns_mean_day
        x_std = returns_std_day
        x_lims = [x_mean - x_std, x_mean + x_std]
        plt.title("Amihud vs. Daily returns")
        plot.scatters(returns_daily, illiq_daily, show_plot=0, xtitle="Returns daily (%)", ytitle="Amihud daily (%)",
                      ylims=y_lims, xlims=x_lims, perc1=1, perc2=1)
        # Regression lines
        slope, intercept, r_value, p_value, stderr = linreg.linreg_coeffs(returns_daily, illiq_daily)
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
        x_lims = [0, x_mean + x_std]
        plt.title("Amihud vs. daily traded volumes")
        plot.scatters(volumes_daily, illiq_daily, show_plot=0, xtitle="Volumes daily (BTC)", ytitle="Amihud daily (%)",
                      ylims=y_lims, xlims=x_lims, perc1=0, perc2=1)
        # Regression lines
        slope, intercept, r_value, p_value, stderr = linreg.linreg_coeffs(volumes_daily, illiq_daily)
        plot.regression_line(intercept, slope, xlims=x_lims)
        print("Amihud - Volume:")
        linreg.stats(slope, intercept, r_value, p_value)

        fig_count += 1

    if amihud_v_volatility == 1:
        # Amihud v Voatility
        plt.figure(fig_count)

        x_mean = anlzd_volatility_mean_excl_extremes
        x_std = anlzd_volatility_std_excl_extremes
        # x_lims = [0, x_mean + x_std]
        x_lims = [0, 0.0079]
        plt.title("Amihud vs. daily volatiltiy")
        plot.scatters(anlzd_volatility_day, illiq_daily, show_plot=0, xtitle="Volatility daily, annualized", ytitle="Amihud daily",
                      ylims=y_lims, xlims=x_lims, perc1=1, perc2=1)
        # Regression lines
        slope, intercept, r_value, p_value, stderr = linreg.linreg_coeffs(anlzd_volatility_day, illiq_daily)
        plot.regression_line(intercept, slope, xlims=x_lims)
        print("Amihud - Volatility:")
        linreg.stats(slope, intercept, r_value, p_value)

        # Without extreme volatitlity values
        slope, intercept, r_value, p_value, stderr = linreg.linreg_coeffs(anlzd_vol_excluding_extremes, illiq_excl_extremes)
        plot.regression_line(intercept, slope, xlims=x_lims, color="red")
        print("Amihud - Volatility (excl. extreme volatitlty):")
        linreg.stats(slope, intercept, r_value, p_value)

        fig_count += 1

plt.show()
hourly_scatters = 0
if hourly_scatters == 1:
    spread_abs_hour, spread_hourly, time_list_rolls_hourly, count_value_error = rolls.rolls(prices_minutes[0, :], time_list_minutes, calc_basis=0, kill_output=1)
    time_list_hours, prices_hourly, volumes_hourly = dis.convert_to_hour(time_list_minutes, prices_minutes, volumes_minutes)
    returns_hourly = jake_supp.logreturn(prices_hourly[0, :])
    volumes_hourly = volumes_hourly[0, :] # Kun bitstamp

    y_mean = np.mean(spread_hourly)
    y_std = np.std(spread_hourly)
    y_lims = [0, y_mean + y_std]

    fig_count = 1

    # Rolls v Returns
    plt.figure(fig_count)

    x_mean = np.mean(returns_hourly)
    x_std = np.std(returns_hourly)
    x_lims = [x_mean-x_std, x_mean + x_std]
    plt.title("Bid/ask spread vs. Hourly returns")
    plot.scatters(returns_hourly, spread_hourly, show_plot=0, xtitle="Returns hourly", ytitle="Spread hourly", ylims=y_lims, xlims=x_lims)

    fig_count += 1
    # Rolls v Volumes
    plt.figure(fig_count)

    x_mean = np.mean(volumes_hourly)
    x_std = np.std(volumes_hourly)
    x_lims = [0, x_mean + x_std]
    plt.title("Bid/ask spread vs. Hourly traded volumes")
    plot.scatters(volumes_hourly, spread_hourly, show_plot=0, xtitle="Volumes hourly [BTC]", ytitle="Spread hourly", ylims=y_lims, xlims=x_lims)

    fig_count += 1
    # Returns v Volumes
    plt.figure(fig_count)

    y_mean = np.mean(returns_hourly)
    y_std = np.std(returns_hourly)
    y_lims = [y_mean - y_std, y_mean + y_std]
    x_mean = np.mean(volumes_hourly)
    x_std = np.std(volumes_hourly)
    x_lims = [0, x_mean + x_std]
    plt.title("Hourly returns vs. Hourly traded volumes")
    plot.scatters(volumes_hourly, returns_hourly, show_plot=0, xtitle="Volumes hourly [BTC]",
                  ytitle="Returns hourly", ylims=y_lims, xlims=x_lims)

    fig_count += 1

    # Rolls v Returns w/ volume as size
    plt.figure(fig_count)

    x_mean = np.mean(returns_hourly)
    x_std = np.std(returns_hourly)
    x_lims = [x_mean - x_std, x_mean + x_std]

    y_mean = np.mean(spread_hourly)
    y_std = np.std(spread_hourly)
    y_lims = [0, y_mean + y_std]

    plt.title("Bid/ask spread vs. Daily returns")
    plot.scatters(returns_hourly, spread_hourly, show_plot=1, xtitle="Returns hourly", ytitle="Spread hourly",
                  label="Bubble size = traded volume", ylims=y_lims, xlims=x_lims, areas=volumes_hourly)