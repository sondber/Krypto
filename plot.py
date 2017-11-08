import matplotlib.pyplot as plt
import numpy as np
from Sondre import sondre_support_formulas as supp, user_interface as ui
import pandas

def user_plots(exchanges, time_list, prices, volumes, total_prices, total_volume):
    number_of_ticks = 5
    n_exc = len(exchanges)
    fig_count = 1  # Ensures that each graph has its own unique figure
    x, myticks = supp.get_ticks(time_list, number_of_ticks)
    volumeplots, priceplots, varplots, dataplots = ui.plots()

    number_of_ticks = 5
    x, myticks = supp.get_ticks(time_list, number_of_ticks)

    if volumeplots or priceplots or varplots or dataplots:
        print("\nPLOTS")
        print("---------------------------------------------------------------------------------\n")

    if volumeplots:
        print("Drawing volume plots...")
        plt.figure(fig_count)
        fig_count = fig_count + 1
        volume_plots(total_volume, volumes, exchanges)

    if priceplots:
        print("Drawing price plots...")
        plt.figure(fig_count)
        fig_count = fig_count + 1
        plt.xticks(x, myticks)
        price_plots(total_prices, prices, exchanges)

    if varplots:
        plt.figure(fig_count)
        fig_count = fig_count + 1
        plt.xticks(x, myticks)
        var_plots(prices, exchanges, "Minute-to-minute variance of prices")

    if dataplots:
        print("Drawing histograms... \n")
        plt.figure(fig_count)
        fig_count = fig_count + 1
        hist_plot(total_volume, "Total volume distribution")

        if n_exc > 1:
            inp = input("\033[33;0;0mWould you like distribution plots for each individual exchange?\
    [1=Yes, 0=No]: \033[0;0;0m\n")
            if inp == 1 or inp == 'y' or inp == 'yes':
                individual_plots = True
            else:
                individual_plots = False
            if individual_plots is True:
                for i in range(0, n_exc):
                    plt.figure(fig_count)
                    fig_count = fig_count + 1
                    description = "Distribution of volume for " + exchanges[i]
                    hist_plot(volumes[i, :], description)
                    avg_min = supp.average_at_time_of_day(volumes[i, :])

    plt.show()  # Denne må stå etter alle plots for at de skal vises sammen


def hist_plot(in_list, description):
    n_bins = 20
    print("max is " + str(max(in_list)))
    my_bins = np.zeros(n_bins)
    for i in range(0, n_bins):
        max_bin = max(in_list)
        min_bin = 0
        my_bins[i] = i / n_bins * (max_bin - min_bin) + min_bin
    n, bins, patches = plt.hist(in_list, bins=my_bins, normed=1, facecolor='blue', alpha=0.75)
    plt.xlabel('Outcome')
    plt.ylabel('Probability')
    plt.title(description)
    plt.grid(False)


def time_of_day(in_list):
    time_list = range(0, 24 * 60)
    daycount = 0
    mincount = 0
    days = len(in_list) / (60 * 24)

    while daycount < days:
        day_list = in_list[mincount:(mincount + 24 * 60)]
        plt.plot(time_list, day_list)
        daycount = daycount + 1
        mincount = daycount * 60 * 24
    avg_per_min = supp.average_at_time_of_day(in_list)
    plt.plot(time_list, avg_per_min, linewidth=2, color='black')
    plt.xlabel("UTC time")
    plt.legend()


def plot_for_exchanges(matrix, exchanges):
    try:  # Skal bare sjekke om dette er bitstamp eller om det er for alle exchangene
        n_cols = np.size(matrix, 1)
    except IndexError:
        n_cols = 1

    if n_cols > 1:
        for i in range(0, np.size(matrix, 0)):
            per_day = supp.average_at_time_of_day(matrix[i, :])
            plt.plot(per_day, label=exchanges[i])
    else:
        per_day = supp.average_at_time_of_day(matrix)
        plt.plot(per_day, label=exchanges[0])

    labels = ["00:00\n20:00\n09:00", "06:00\n02:00\n15:00", "12:00\n08:00\n21:00", "18:00\n14:00\n03:00",
              "23:59\n19:59\n08:59"]
    plt.xticks(np.arange(0, 1441, 6 * 60), labels)
    plt.title("Average volume over the course of a day")
    plt.ylabel("Number of bitcoins traded per minute")
    plt.figtext(0.01, 0.068, "London")
    plt.figtext(0.01, 0.036, "New York")
    plt.figtext(0.01, 0.005, "Tokyo")
    plt.legend()


def volume_plots(total_volume, volumes, exchanges):
    total_day = supp.average_at_time_of_day(total_volume)
    plt.plot(total_day, label='Total volume')
    plot_for_exchanges(volumes, exchanges)


def price_plots(total_prices, prices, exchanges):
    n_exc = len(exchanges)
    if n_exc > 1:
        for i in range(0, n_exc):
            plt.plot(prices[i, :], label=exchanges[i])
    else:
        plt.plot(prices, label=exchanges[0])
    plt.title("Price chart")
    plt.ylabel("USD/BTC")
    if n_exc > 1:
        plt.plot(total_prices, label="Volume weighted average price, USD/BTC", linewidth=0.5, color="black")
    plt.legend()


def var_plots(prices, exchanges,
              title):  # Denne må skrives om så den tar inn en liste med varianse og plotter det i stedet
    n_exc = len(exchanges)
    mins = [1]
    mins[0] = int(input("How many mintues rolling average would you like? "))
    print("Working on variance plots, this may take some time...")
    for m in mins:
        for i in range(0, n_exc):
            if n_exc > 1:
                mov_var = supp.moving_variance(prices[i, :], m)
            else:
                mov_var = supp.moving_variance(prices, m)
            exc = exchanges[i]
            if m > 60:
                interval = " " + str(m / 60) + " hours"
            else:
                interval = " " + str(m) + " minutes"
            plot_label = exc + interval + " moving average " + title
            plt.plot(mov_var, label=plot_label)

    plt.legend()
    plt.title(title)


def easy_plot(y, label="My plot", show_plot=1):
    label = str(label)
    plt.plot(y, label=label)
    plt.legend()
    if show_plot == 1:
        plt.show()


def scatters(x, y, color="blue", areas=[], label="", show_plot=1, xlims=[], ylims=[], xtitle="", ytitle="", perc1=0, perc2=0):
    if not xlims:
        xlims = [min(x), max(x)]
    if not ylims:
        ylims = [min(y), max(y)]
    n = len(x)
    if len(areas) == 0:
        areas_scaled = np.ones(n)
    else:
        scaling_factor = 50
        max_area = max(areas)
        for i in range(len(areas)):
            if areas[i] == 0:
                areas[i] += 1
        areas_scaled = np.zeros(len(areas))
        for i in range(len(areas)):
            areas_scaled[i] = scaling_factor * areas[i]/ max_area
    plt.scatter(x, y, s=areas_scaled, c=color, alpha=0.5, label=label, color="black")
    plt.xlim(xlims)
    plt.ylim(ylims)
    if perc1 == 1:
        ax = plt.gca()
        vals = ax.get_xticks()
        ax.set_xticklabels(['{:3.2f}%'.format(x * 100) for x in vals])

    if perc2 == 1:
        ax = plt.gca()
        vals = ax.get_yticks()
        ax.set_yticklabels(['{:3.2f}%'.format(x * 100) for x in vals])

    if xtitle:
        plt.xlabel(xtitle)
    if ytitle:
        plt.ylabel(ytitle)
    if label:
        plt.legend()
    if show_plot == 1:
        plt.show()


def two_scales(ax1, time_list, data1, data2, title1, title2, title_x, color1, color2, type1, type2, scale1, scale2):
    # brukes til å sette de to aksene riktig skalert
    print(' Running two_scales...')
    ax2 = ax1.twinx()
    if type1 == 'plot':
        ax1.plot(time_list, data1, color=color1, linewidth=0.5, label=title1)
    elif type1 == 'bar':
        ax1.bar(time_list, data1, color=color1, label=title1)

    if type2 == 'plot':
        ax2.plot(time_list, data2, color=color2, linewidth=0.5, label=title2)
    elif type2 == 'bar':
        ax2.bar(time_list, data2, color=color2, label=title2)
    print("  Type of plot: ", type1)

    if scale2 == 'plot_over_bar' or scale1 == 'plot_over_bar':
        print("  plot over bar")
        ax1.set_ylim([min(data1) - 0.2 * (max(data1) - min(data1)), max(data1)])
        ax2.set_ylim([min(data2), max(data2)])
    else:
        if scale1 == 'auto':
            print('  Scale1: auto')
        else:
            print("  min(%s): %0.4f" % (title1, min(data1)))
            print("  max(%s): %0.4f" % (title1, max(data1)))
            minimum = input('   Set new min: ')
            maximum = input('   Set new max: ')
            ax1.set_ylim([float(minimum), float(maximum)])
        ax1.set_xlabel(title_x)
        ax1.set_ylabel(title1)
        if scale2 == 'auto':
            print('  Scale2: auto')
        else:
            print("  min(%s): %0.4f" % (title2, min(data2)))
            print("  max(%s): %0.4f" % (title2, max(data2)))
            minimum = input('   Set new min: ')
            maximum = input('   Set new max: ')
            ax2.set_ylim([float(minimum), float(maximum)])

    ax2.set_ylabel(title2)
    return ax1, ax2


def two_axis(data1, data2, title1="data1", title2="data2", title_x='time (hours)', color1='r', color2='b',
             type1='plot', type2='bar', scale1='auto', scale2='auto'):
    # denne gir et 2-akset system for de to datasettene
    print("Running two_axis... \033[31;00;0m(even though the plural of axis is 'axes'....Markus....)\033[00;00;0m")
    time_list = np.zeros(len(data1))
    for i in range(len(data1)):
        time_list[i] = i
    # Create axes
    fig, ax = plt.subplots()
    ax1, ax2 = two_scales(ax, time_list, data1, data2, title1, title2, title_x, color1, color2, type1, type2, scale1, scale2)
    plt.legend()
    plt.show()
    print("Finished graphing")
    return None


def sondre_two_axes(y1, y2, x=[], show_plot=1, y1_label="y1", y2_label="y2", x_label="x", title="", y1lims=[], y2lims=[], perc1=0, perc2=0):
    fig, ax1 = plt.subplots()

    n_entries = len(y1)

    t = np.arange(0, n_entries, 1)

    ax1.plot(t, y1, linewidth=0.5, linestyle="-", color="black", label=y1_label)
    ax1.set_ylabel(y1_label)
    ax1.tick_params('y')
    ax1.set_xlabel(x_label)
    ax1.legend(bbox_to_anchor=(1, 0.93))

    ax2 = ax1.twinx()
    ax2.plot(t, y2, linewidth=0.5, linestyle="-", color="blue", label=y2_label)
    ax2.set_ylabel(y2_label)
    ax2.tick_params('y')

    ax2.legend(bbox_to_anchor=(1, 1))
    plt.legend()

    if not y1lims:
        y1lims =[min(y1), max(y1)]
    if not y2lims:
        y2lims = [min(y2), max(y2)]
    ax1.set_ylim(y1lims)
    ax2.set_ylim(y2lims)

    if x:
        n_labels = 5
        labels = []
        len_x = len(x)
        for i in range(0, n_labels):
            if i == n_labels - 1:
                index = len_x - 1
            else:
                index = i * (len_x / (n_labels + 1))
            index = int(index)
            labels.append(x[index][0:11])
        plt.xticks(np.arange(0, len(x) + 1, len(x)/(n_labels-1)), labels)

    if perc1 == 1:
        vals = ax1.get_yticks()
        ax1.set_yticklabels(['{:3.2f}%'.format(x * 100) for x in vals])
    if perc2 == 1:
        vals = ax2.get_yticks()
        ax2.set_yticklabels(['{:3.2f}%'.format(x * 100) for x in vals])

    plt.xlim([0, len(y1)])

    if title:
        plt.title(title)
    fig.tight_layout()
    if show_plot == 1:
        plt.show()


def single_time_series_plot(day_list, data_daily, title, ylims=[], perc=0):
    n_labels = 5
    labels = []
    len_x = len(day_list)
    for i in range(0, n_labels):
        if i == n_labels - 1:
            index = len_x - 1
        else:
            index = i * (len_x / (n_labels - 1))
        index = int(index)
        labels.append(day_list[index][0:11])
    plt.xticks(np.arange(0, len(day_list) + 1, len(day_list) / (n_labels - 1)), labels)
    plt.plot(data_daily, linewidth=0.5, color="black")
    if ylims:
        ymin = ylims[0]
        ymax = ylims[1]
    else:
        ymin = min(data_daily)
        ymax = max(data_daily)*1.01
    plt.ylim([ymin, ymax])
    plt.xlim([0, len(day_list)])
    plt.title(title)
    if perc == 1:
        ax = plt.gca()
        vals = ax.get_yticks()
        ax.set_yticklabels(['{:3.2f}%'.format(x * 100) for x in vals])


def regression_line(alpha, beta, xlims=[], color="black"):
    if xlims:
        x_min = xlims[0]
        x_max = xlims[1]
    else:
        print("No xlims")
        return
    y_vals = [alpha + beta*(x_min) , alpha + beta*(x_max)]
    plt.plot(xlims, y_vals, linestyle="--", color=color)


def plot_x_zero(y_lims):
    x_min = y_lims[0]
    x_max = y_lims[1]
    plt.plot([x_min, x_max], [0, 0], linewidth=0.2, color="black")


def plot_y_zero(x_lims):
    y_min = x_lims[0]
    y_max = x_lims[1]
    plt.plot([0, 10**(-10)], [y_min, y_max], linewidth=0.2, color="black")
