import pip
def install(package):
    pip.main(['install', package])

<<<<<<< HEAD
import numpy as np
import numpy as np
=======
install('numpy')
import matplotlib.pyplot as plt
import data_import as di

startdate = "201701"
enddate = "201709"
volumes=di.get_lists(1,1,startdate,enddate)[5]
spread=di.get_lists(1,1,startdate,enddate)[4]
#time=di.get_lists(1,1,startdate,enddate)[1]
time=np.zeros(len(spread))
for i in range(len(spread)):
    time[i]=i
def two_scales(ax1, time, data1, data2, c1, c2):

    ax2 = ax1.twinx()

    ax1.plot(time, data1, color=c1)
    ax1.set_xlabel('time (s)')
    ax1.set_ylabel('vol')

    ax2.plot(time, data2, color=c2)
    ax2.set_ylabel('spread')
    return ax1, ax2


# Create some mock data
t = time
s1 = volumes
s2 = spread

# Create axes
fig, ax = plt.subplots()
ax1, ax2 = two_scales(ax, t, s1, s2, 'r', 'b')


# Change color of each axis
def color_y_axis(ax, color):
    """Color your axes."""
    for t in ax.get_yticklabels():
        t.set_color(color)
    return None
color_y_axis(ax1, 'r')
color_y_axis(ax2, 'b')
plt.show()
