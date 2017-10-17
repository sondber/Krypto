import csv
import math
import numpy as np
import two_axis_plot as tap
import matplotlib.pyplot as plt
import data_import as di
import descriptive_stats as desc
from Jacob import jacob_csv_handling
from Sondre import sondre_support_formulas as supp


file_name =  "data/export_csv/first_order_autocorr_59_all.csv"
autocorr = []
variance = []
time_list = []

rolls = []

with open(file_name, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=';', quotechar='|')
        #i = 0
        next(reader)
        for row in reader:
                time_list.append(row[0]) # Her leser den første kolonne og lagrer det
                autocorr.append(float(row[1])) # Her leser den andre kolonne og lagrer det som float
                #i = i + 1
print("Autocorrelations loaded")

file_name = "data/export_csv/rolling_variance_all_59.csv"

with open(file_name, newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=';', quotechar='|')
    #i = 0
    next(reader)
    for row in reader:
        variance.append(float(row[1]))
        #i = i+1

print("Variances loaded")
j = 0
for i in range(0, len(autocorr)):
    covar_calc = autocorr[i]*(math.sqrt(variance[j])*math.sqrt(variance[j+1]))
    j += 2
    try:
        roll_calc = 2*math.sqrt(-covar_calc)
    except ValueError:
        roll_calc = 0 #sets rolls estimator to zero if covariance is positive. See Corwin(2014)[15] for assumptions and other methods
    rolls.append(roll_calc)


rolls_daily_mean = []

for i in range(0, len(rolls), 24):
    rolls_daily_mean.append(np.mean(rolls[i:i+24]))

print(rolls_daily_mean)

x, ticks = supp.get_ticks(time_list, 5)



plt.plot(rolls, label = "rolls")
plt.xticks(x, ticks)
plt.legend()
plt.show()

jacob_csv_handling.write_to_file(time_list, rolls, "data/export_csv/rolls_all_59.csv", "Rolls estimator")

volumes = di.get_lists(0,1)[5]
print(len(volumes))
print(len(rolls_daily_mean))

desc.combined_stats(volumes,rolls_daily_mean[0:1728],"Volumes","Rolls")

#tap.two_axis(volumes[15000:41495],rolls[15000:41495])



