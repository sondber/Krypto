import pip
def install(package):
    pip.main(['install', package])

import numpy as np
import numpy as np
import matplotlib.pyplot as plt
import sondre_master
import data_import as di

#rs(groups='jaja')
startdate = "201701"
enddate = "201709"
volumes=di.get_lists(1,1,startdate,enddate)[5]
spread=di.get_lists(1,1,startdate,enddate)[4]
#time=di.get_lists(1,1,startdate,enddate)[1]


def two_axis_plot(data1,data2):#not using dates on x-axis yet

    time=np.zeros(len(data1))
    for i in range(len(data1)):
        time[i]=i
    # Create axes
    fig, ax = plt.subplots()
    ax1, ax2 = two_axis_plot(ax, time, data1, data2, 'r', 'b')

    ax2 = ax1.twinx()
    c1='tab:olive' #color change doesnt work.
    c2='red'

    ax1.plot(time, data1, color=c1)
    ax1.set_xlabel('time (min)')
    ax1.set_ylabel('vol')

    ax2.plot(time, data2, color=c2)
    ax2.set_ylabel('spread')

    plt.show()

    return 0

two_axis_plot(volumes,spread)






