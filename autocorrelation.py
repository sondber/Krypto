import numpy as np
import csv
import time
import jacob_csv_handling

def autocorrelation(array1, array2): #window in minutes, timestart is which minute you want to start in
    #print("Now we are in autocorrelation function(waiting 2 seconds)")
    #time.sleep(2)
    try:
        result = np.corrcoef(array1, array2)[1, 0] #finner korrelasjonen mellom de to arrays
    except RuntimeError:
        result = 0
    return result #finner korrelasjonen mellom de to arrays

def autocorrelation_rolling(returns, timestart, window, lag):
    rolling_autocorrelation = [0]*(len(returns))
    counter = timestart+window
    if timestart+window >= len(returns):
        print("No valid autocorrelations available")
    else:
        for i in range(timestart+lag, (len(returns)-window+1)):
            array1 = returns[i:i+window] #window is number of minutes back
            #print(array1)
            array2 = returns[(i-lag):(i+window-lag)]
            #print(array2)
            rolling_autocorrelation[counter] = autocorrelation(array1, array2)
            counter += 1
            if i%10000==0:
                print("We are currently on line",i,"of",(len(returns)-window+1),"corresponding to",round(i/(len(returns)-window+1)*100,2),"%")
        return rolling_autocorrelation

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

print("Now the logreturns have been loaded into the vector(waiting 5 seconds)")
time.sleep(5)
rolling_auto = autocorrelation_rolling(returns, 0, 30, 1)
#print(rolling_auto)


jacob_csv_handling.write_to_file(time_list, rolling_auto, "data/export_csv/first_order_autocorr_30_all.csv","First order autocorrelation 30")

