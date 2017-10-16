import pip
def install(package):
    pip.main(['install', package])

import numpy as np
import matplotlib.pyplot as plt
#import sondre_master
import data_import as di

#volumes=di.get_lists(1,1,startdate,enddate)[5]
#spread=di.get_lists(1,1,startdate,enddate)[4]
#time=di.get_lists(1,1,startdate,enddate)[1]
'''
volumes=np.zeros(100)
spread=np.zeros(100)
for i in range(100):
    volumes[i]=i*i-0.002*i*i*i
    spread[i]=10*i-0.055*i*i
    '''
from Sondre import sondre_support_formulas as supp
time_list, rolls = supp.get_rolls()
print(rolls)

def two_scales(ax1, time, data1, data2, c1, c2):
    #brukes til å sette de to aksene riktig skalert
    ax2 = ax1.twinx()
    ax1.bar(time, data1, color=c1)#bar her gir søyler
    ax1.set_xlabel('time (min)')
    ax1.set_ylabel('vol')
    ax2.plot(time, data2, color=c2)#plot her gir en kontinuerlig graf
    ax2.set_ylabel('spread')
    return ax1, ax2


def two_axis(data1,data2):
    #denne gir et 2-akset system for de to datasettene
    #husk å stille bar vs plot i two_scales
    time = np.zeros(len(data1))
    for i in range(len(data1)):
        time[i] = i
    # Create axes
    fig, ax = plt.subplots()
    ax1, ax2 = two_scales(ax, time, data1, data2, 'r', 'b')
    plt.show()
    return None


two_axis(volumes,spread)
#print(np.corrcoef(volumes,spread))

