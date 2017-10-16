import csv
import math

import matplotlib.pyplot as plt

from Jacob import jacob_csv_handling
from Sondre import sondre_support_formulas as supp

file_name =  "data/export_csv/first_order_autocorr_60_all.csv"
autocorr = []
variance = []
time_list = []

rolls = [0]

with open(file_name, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=';', quotechar='|')
        #i = 0
        next(reader)
        for row in reader:
                time_list.append(row[0]) # Her leser den første kolonne og lagrer det
                autocorr.append(float(row[1])) # Her leser den andre kolonne og lagrer det som float
                #i = i + 1
print("Autocorrelations loaded")

file_name = "data/export_csv/rolling_variance_all.csv"

with open(file_name, newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=';', quotechar='|')
    #i = 0
    next(reader)
    for row in reader:
        variance.append(float(row[1]))
        #i = i+1

print("Variances loaded")
for i in range(1, len(autocorr)):
    covar_calc = autocorr[i]*(math.sqrt(variance[i])*math.sqrt(variance[i-1]))
    try:
        roll_calc = 2*math.sqrt(-covar_calc)
    except ValueError:
        roll_calc = 0 #sets rolls estimator to zero if covariance is positive. See Corwin(2014)[15] for assumptions and other methods
    rolls.append(roll_calc)




x, ticks = supp.get_ticks(time_list, 5)



plt.plot(rolls, label = "rolls")
plt.xticks(x, ticks)
plt.legend()
plt.show()


jacob_csv_handling.write_to_file(time_list, rolls, "data/export_csv/rolls_all_60.csv", "Rolls estimator")