import numpy as np
import csv
import jacob_csv_handling
import matplotlib.pyplot as plt

def varians(returns,units_rolling): #takes in the list of logreturns and minutes rolling required
    var = np.zeros(len(returns)/units_rolling)#to be returned
    for i in range(0, len(returns)-units_rolling+1, units_rolling):
        j = units_rolling+i-1
        var[j] = np.var(returns[i:(i+units_rolling)]) # are we confident on this var-calculation, ref is set observed or real?
        if i%100000==0:
            print("Progress in calculation:", round(i/(len(returns)-units_rolling+1)*100, 2), "%")
    return var


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

variance = varians(returns, 60) #one hour variances

plt.plot(variance)
plt.show()

print("The variances are calculated")
jacob_csv_handling.write_to_file(time_list, variance, "data/export_csv/rolling_variance_all.csv","Variance")