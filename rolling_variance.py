import csv

import matplotlib.pyplot as plt
import numpy as np

from Jacob import jacob_csv_handling
from Sondre import sondre_support_formulas as supp

#This function calculates variances to be used in the calculation of Rolls
#The input is a list of logreturns and the corresponding time-list
#The "units_rolling" input should be given as a number of minutes the variances should be calced on
#If units_rolling = 60, the variance of minutes with index 0-58 and 1-59 will be calculated.
#Then, the code jumps to index 60-69, and the variance of 60-68 and 61-69 will be calculated and stored.
#The lenght of the output will be 2 * (len(returnsH)/unit_rolling), and the time-stamp will be the start of the window
#Be aware that the returnsH[0] is set to 0 for completeness of vector lengths

def variance(returns, time_list, units_rolling): # takes in the list of logreturns and minutes rolling required
    var = np.zeros(int(2*(len(returns)/units_rolling))) # to be returned
    j = 0
    hourlist = []
    for i in range(0, len(returns)-units_rolling+1, units_rolling):
        var[j] = np.var(returns[i:(i+units_rolling-1)]) # takes the first units_rolling-1 minutes (0-58)
        var[j+1] = np.var(returns[(i+1):(i+units_rolling)]) # takes the latter part (1-59)
        hourlist.append(time_list[i]) #timestamps variance calc with start of window
        hourlist.append(time_list[i])  # timestamps variance calc with start of window
        j += 2
        if i%100000==0:
            print("Progress in calculation:", round(i/(len(returns)-units_rolling+1)*100, 2), "%")
    return var, hourlist


file_name =  "data/export_csv/logreturns_all_minute.csv"
returns = []
time_list = []

with open(file_name, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=';', quotechar='|')
        i = 0
        next(reader)
        for row in reader:
                time_list.append(row[0]) # Her leser den første kolonne og lagrer det
                returns.append(float(row[1])) # Her leser den andre kolonne og lagrer det som float
                i = i + 1
print("The data is loaded")


variance, hourlist = variance(returns, time_list, 60) #one hour variances


x, ticks = supp.get_ticks(hourlist,5)
plt.plot(variance)
plt.xticks(x,ticks)
plt.ylim(0, 0.001)
plt.show()

print("The variances are calculated")
jacob_csv_handling.write_to_file(hourlist, variance, "data/export_csv/rolling_variance_all_59.csv", "One-hour variance")