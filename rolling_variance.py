import numpy as np
import csv
import csvwriter

def varians2(returns,days_rolling): #takes in the list of logreturns and days rolling required
    var=np.zeros(len(returns)) #to be returned
    for i in range(len(returns)-days_rolling+1):
        j = days_rolling+i-1
        var[j] = np.var(returns[i:(i+days_rolling)])
        if i%100000==0:
            print("Progress in calculation:", round(i/(len(returns)-days_rolling+1)*100, 2), "%")
    return var

file_name =  "data/export_csv/test_data.csv"
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

variance = varians2(returns, 30)

print("The variances are calculated")
csvwriter.write_to_file(time_list, variance, "data/export_csv/rolling_variance_all.csv")