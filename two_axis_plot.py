import pip
def install(package):
    pip.main(['install', package])

import numpy as np
import matplotlib.pyplot as plt
import data_import as di

volumes = di.get_lists(1, 1)[5]
prices = di.get_lists(1, 1)[4]


def two_scales(ax1, time, data1, data2,title1,title2,title_x, color1, color2,type1,type2,scale1,scale2):
    #brukes til å sette de to aksene riktig skalert
    print('running two_scales')
    ax2 = ax1.twinx()
    if (type1=='plot'):
        ax1.plot(time, data1, color=color1)
    elif (type1=='bar'):
        ax1.bar(time, data1, color=color1)

    if (type2 == 'plot'):
        ax2.plot(time, data2, color=color2)
    elif (type2 == 'bar'):
        ax2.bar(time, data2, color=color2)
    print(type1)

    if (scale2=='plot_over_bar' or scale1=='plot_over_bar'):
        print("plot over bar")
        ax1.set_ylim([min(data1) - 0.2 * (max(data1) - min(data1)), max(data1)])
        ax2.set_ylim([min(data2),max(data2)])
    else:
        if (scale1=='auto'):
            print('scale1 auto')
        elif (scale1=='custom'):
            print("min(data1): ",min(data1))
            print("max(data1): ",max(data1))
            minimum=input('set new min: ')
            maximum=input('set new max: ')
            ax1.set_ylim([int(minimum),int(maximum)])
        ax1.set_xlabel(title_x)
        ax1.set_ylabel(title1)
        if (scale2=='auto'):
            print('scale2 auto')
        elif (scale2=='custom'):
            print("min(data2): ",min(data2))
            print("max(data2): ",max(data2))
            minimum=input('set new min: ')
            maximum=input('set new max: ')
            ax2.set_ylim([int(minimum),int(maximum)])



    ax2.set_ylabel(title2)
    return ax1, ax2


def two_axis(data1,data2, title1="data1",title2="data2",title_x='time (hours)',color1='r',color2='b',
             type1='plot',type2='bar',scale1='auto',scale2='auto'):
    #denne gir et 2-akset system for de to datasettene
    print('running two_axis')
    time = np.zeros(len(data1))
    for i in range(len(data1)):
        time[i] = i
    # Create axes
    fig, ax = plt.subplots()
    ax1, ax2 = two_scales(ax, time, data1, data2,title1,title2,title_x,color1,color2,type1,type2,scale1,scale2)
    plt.show()
    print("picture finished")
    return None

#print(np.corrcoef(volumes[40000:41495],rolls[40000:41495]))

two_axis(prices,volumes, scale1='plot_over_bar')


