import pip

def install(package):
    pip.main(['install', package])

install('numpy')


import numpy as np
import numpy as np
import matplotlib.pyplot as plt

volumes=[100,80,90,110,150]
spread=[0.2,0.23,0.19,0.24,0.25]
time=[0,1,2,3,4]

def two_scales(ax1, time, data1, data2, c1, c2):
    """

    Parameters
    ----------
    ax : axis
        Axis to put two scales on

    time : array-like
        x-axis values for both datasets

    data1: array-like
        Data for left hand scale

    data2 : array-like
        Data for right hand scale

    c1 : color
        Color for line 1

    c2 : color
        Color for line 2

    Returns
    -------
    ax : axis
        Original axis
    ax2 : axis
        New twin axis
    """
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
