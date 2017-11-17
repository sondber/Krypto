import matplotlib.pyplot as plt
import numpy as np
from Sondre import sondre_support_formulas as supp, user_interface as ui
import pandas
from matplotlib.ticker import FormatStrFormatter


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


def scatters(x, y, color="black", areas=[], label="", show_plot=0, xlims=[], ylims=[], xtitle="", ytitle="", x_perc=0, y_perc=0, x_log=0, y_log=0):
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
    plt.scatter(x, y, s=areas_scaled, c=color, alpha=0.5, label=label)
    plt.xlim(xlims)
    plt.ylim(ylims)

    if x_log == 1:
        plt.xscale("log", basex=np.exp(1))

    if y_log == 1:
        plt.yscale("log", basey=np.exp(1))

    if x_perc == 1:
        ax = plt.gca()
        vals = ax.get_xticks()
        ax.set_xticklabels(['{:3.2f}%'.format(x * 100) for x in vals])

    if y_perc == 1:
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


def sondre_two_axes(y1, y2, x=[], show_plot=1, y1_label="y1", y2_label="y2", x_label="x", title="", y1lims=[], y2lims=[], perc1=0, perc2=0, log1=0, log2=0):
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
    if log1 == 1:
        vals = ax1.get_yticks()
        ax1.set_yticklabels(['{:3.2f}%'.format(10 ** x) for x in vals])
    if log2 == 1:
        vals = ax1.get_yticks()
        ax1.set_yticklabels(['{:3.2f}%'.format(10 ** x) for x in vals])


    plt.xlim([0, len(y1)])

    if title:
        plt.title(title)
    fig.tight_layout()
    if show_plot == 1:
        plt.show()


def time_series_single(time_list, data, title, ylims=[], perc=0, logy=0):
    n_labels = 5
    labels = []
    len_x = len(time_list)
    for i in range(0, n_labels):
        if i == n_labels - 1:
            index = len_x - 1
        else:
            index = i * (len_x / (n_labels - 1))
        index = int(index)
        labels.append(time_list[index][0:11])
    plt.figure(figsize=(6, 4))
    plt.xticks(np.arange(0, len(time_list) + 1, len(time_list) / (n_labels - 1)), labels)
    plt.plot(data, linewidth=0.5, color="black")
    if ylims:
        ymin = ylims[0]
        ymax = ylims[1]
    else:
        ymin = min(data)
        ymax = max(data) * 1.01
    plt.ylim([ymin, ymax])
    plt.xlim([0, len(time_list)])

    if logy == 1:
        ax = plt.gca()
        plt.yscale("log", basey=np.exp(1))
        plt.ylim([0, ymax])
    if perc == 1:
        ax = plt.gca()
        vals = ax.get_yticks()
        ax.set_yticklabels(['{:3.2f}%'.format(x * 100) for x in vals])
    ax = plt.gca()
    title = title.lower()
    location = "figures/variables_over_time/" + title + ".png"
    plt.savefig(location)


def regression_line(alpha, beta, xlims=[], color="black"):
    if xlims:
        x_min = xlims[0]
        x_max = xlims[1]
    else:
        print("No xlims")
        return
    y_vals = [alpha + beta*(x_min) , alpha + beta*(x_max)]
    plt.plot(xlims, y_vals, linestyle="--", color=color)


def plot_y_zero(y_lims):
    x_min = y_lims[0]
    x_max = y_lims[1]
    plt.plot([x_min, x_max], [0, 0], linewidth=0.2, color="black")


def plot_x_zero(x_lims):
    y_min = x_lims[0]
    y_max = x_lims[1]
    plt.plot([0, 10**(-10)], [y_min, y_max], linewidth=0.2, color="black")


def hour_of_day_ticks():
    labels = ["00:00\n19:00", "06:00\n01:00", "12:00\n07:00", "18:00\n13:00",
              "23:59\n18:59"]
    plt.xticks(np.arange(0, 25, 6), labels)
    plt.figtext(0.005, 0.055, "London", fontsize=10)
    plt.figtext(0.005, 0.010, "NYC", fontsize=10)
    plt.xlim([0, 24])


def plot_for_day(average, low, high, title="no_title", perc=0):
    plt.figure(figsize=[6, 2])
    plt.plot(average, label=title, color="black")
    plt.plot(low, label="95% confidence interval", color="black", linestyle='--', linewidth=0.5)
    plt.plot(high, color="black", linestyle='--', linewidth=0.5)

    if perc == 1:
        ax = plt.gca()
        vals = ax.get_yticks()
        ax.set_yticklabels(['{:3.2f}%'.format(x * 100) for x in vals])

    ax = plt.gca()
    #ax.margins(x=0.5, y=1, tight=False)
    hour_of_day_ticks()
    plt.legend()
    title=title.lower()
    location = "figures/seasonality/day/" + title + ".png"
    plt.savefig(location)


def plot_for_week(average, low, high, title="no_title", perc=0, logy=0, weekends=1):
    plt.figure()
    plt.plot(average, label=title, color="black")
    plt.plot(low, label="95% confidence interval", color="black", linestyle='--', linewidth=0.5)
    plt.plot(high, color="black", linestyle='--', linewidth=0.5)

    if weekends == 1:
        labels = ["Mon", "Tue", "Wed", "Thur", "Fri", "Sat", "Sun"]
        plt.xticks(np.arange(0, 7, 1), labels)
        plt.xlim([0, 6])
    else:
        labels = ["Mon", "Tue", "Wed", "Thur", "Fri"]
        plt.xticks(np.arange(0, 5, 1), labels)
        plt.xlim([0, 4])
    if logy == 1:
        ax = plt.gca()
        plt.yscale("log", basey=np.exp(1))
    if perc == 1:
        ax = plt.gca()
        vals = ax.get_yticks()
        ax.set_yticklabels(['{:3.2f}%'.format(x * 100) for x in vals])
    title = title.lower()
    plt.legend()
    location = "figures/seasonality/week/" + title + ".png"
    plt.savefig(location)
