import pip
import numpy as np
import matplotlib.pyplot as plt
import data_import as di


"""
def install(package):
    pip.main(['install', package])
"""


def two_scales(ax1, time, data1, data2, title1, title2, title_x, color1, color2, type1, type2, scale1, scale2):
    # brukes til å sette de to aksene riktig skalert
    print(' Running two_scales...')
    ax2 = ax1.twinx()
    if type1=='plot':
        ax1.plot(time, data1, color=color1, linewidth=0.5)
    elif type1=='bar':
        ax1.bar(time, data1, color=color1)

    if type2 == 'plot':
        ax2.plot(time, data2, color=color2, linewidth=0.5)
    elif type2 == 'bar':
        ax2.bar(time, data2, color=color2)
    print("  Type of plot: ", type1)

    if scale2 == 'plot_over_bar' or scale1 == 'plot_over_bar':
        print("  plot over bar")
        ax1.set_ylim([min(data1) - 0.2 * (max(data1) - min(data1)), max(data1)])
        ax2.set_ylim([min(data2), max(data2)])
    else:
        if scale1 == 'auto':
            print('  Scale1: auto')
        elif scale1 == 'custom':
            print("  min(%s): %0.1f" % (title1, min(data1)))
            print("  max(%s): %0.1f" % (title1, max(data1)))
            minimum = input('   Set new min: ')
            maximum = input('   Set new max: ')
            ax1.set_ylim([float(minimum),float(maximum)])
        ax1.set_xlabel(title_x)
        ax1.set_ylabel(title1)
        if scale2 == 'auto':
            print('  Scale2: auto')
        elif scale2 == 'custom':
            print("  min(%s): %0.1f" % (title2, min(data2)))
            print("  max(%s): %0.1f" % (title2, max(data2)))
            minimum = input('   Set new min: ')
            maximum = input('   Set new max: ')
            ax2.set_ylim([float(minimum), float(maximum)])

    ax2.set_ylabel(title2)
    return ax1, ax2


def two_axis(data1, data2, title1="data1", title2="data2", title_x='time (hours)', color1='r', color2='b',
             type1='plot', type2='bar', scale1='auto', scale2='auto'):
    # denne gir et 2-akset system for de to datasettene
    print("Running two_axis... \033[31;00;0m(even though the plural of axis is 'axes'....Markus....)\033[00;00;0m")
    time = np.zeros(len(data1))
    for i in range(len(data1)):
        time[i] = i
    # Create axes
    fig, ax = plt.subplots()
    ax1, ax2 = two_scales(ax, time, data1, data2, title1, title2, title_x, color1, color2, type1, type2, scale1, scale2)
    plt.show()
    print("Finished graphing")
    return None


