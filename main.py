import data_import_support as dis
from Sondre import sondre_support_formulas as sup
from Sondre.sondre_support_formulas import unix_to_timestamp
import data_import as di
import matplotlib.pyplot as plt
import numpy as np

tidsliste,volum= di.get_global_volume()

def plot(time_list, data, title, ylims=[], perc=0, logy=0, ndigits=2, ylab=""):
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
    plt.figure(figsize=(8, 2), dpi=300)
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
        if perc == 0:
            vals = ax.get_yticks()
            frmt = '{:3.'+str(ndigits)+'f}'
            ax.set_yticklabels([frmt.format(x) for x in vals])
    if perc == 1:
        ax = plt.gca()
        vals = ax.get_yticks()
        frmt = '{:3.'+str(ndigits)+'f}%'
        ax.set_yticklabels([frmt.format(x * 100) for x in vals])

    if len(ylab)>0:
        plt.ylabel(ylab)
    title = title.lower()
    location = "figures/variables_over_time/" + title + ".png"
    plt.savefig(location)


plot(tidsliste,volum,'Daily volume')