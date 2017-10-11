import numpy as np
import matplotlib.pyplot as plt
import sondre_support_formulas as supp
import time
import user_interface as ui


def user_plots(exchanges, time_list, prices, volumes, total_prices, total_volume, currency):
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
        price_plots(total_prices, prices, exchanges, currency)

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
    days = len(in_list)/(60*24)

    while daycount < days:

        day_list = in_list[mincount:(mincount+24*60)]
        plt.plot(time, day_list)
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


def price_plots(total_prices, prices, exchanges, currency):
    n_exc = len(exchanges)
    if n_exc > 1:
        for i in range(0, n_exc):
            plt.plot(prices[i, :], label=exchanges[i])
    else:
        plt.plot(prices, label=exchanges[0])
    if currency:
        plt.title("Prices converted to USD")
        plt.ylabel("USD/BTC")
    else:
        plt.title("Prices in original currencies")

    if n_exc > 1:
        plt.plot(total_prices, label="Volume weighted average price, USD/BTC", linewidth=0.5, color="black")

    plt.legend()


def var_plots(prices, exchanges, title):  # Denne må skrives om så den tar inn en liste med varianse og plotter det i stedet
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
                interval = " " + str(m/60) + " hours"
            else:
                interval = " " + str(m) + " minutes"
            plot_label = exc + interval + " moving average " + title
            plt.plot(mov_var, label=plot_label)

    plt.legend()
    plt.title(title)


def easy_plot(y, label, show_plot):
    label = str(label)
    if len(label) > 1:
        plt.plot(y, label=label)
        plt.legend()
    else:
        plt.plot(y)
    if show_plot == 1:
        plt.show()


def scatters(x, y, groups=[], areas=[]):
    n = len(x)
    if groups:
        colors = groups
    else:
        colors = np.zeros(n)
    if not areas:
        areas = 1 * np.ones(n)

    plt.scatter(x, y, s=areas, c=colors, alpha=0.5)
