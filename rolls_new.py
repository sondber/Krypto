import math
from Jacob import jacob_csv_handling, jacob_support
import matplotlib.pyplot as plt

#The following estimation of Rolls estimator is based on the formula in Haugom, Molnar (2014)


def rolls_new(price_differences, time_list_minute, window):
    calculation_inside = 0
    spread = [0]
    time_list_hour = []
    time_list_hour.append(time_list_minute[0])
    count_value_error = 0
    for i in range(0, len(price_differences)-window, window):
        # print("Outer loop: ", i)
        time_list_hour.append(time_list_minute[i])
        for y in range(i+1,i+window+1):
            # print("Inner loop: ",y)
            calculation_inside = calculation_inside + (price_differences[y]*price_differences[y-1])
        try:
            ba_calc = 2*math.sqrt(-calculation_inside/(window-1))
        except ValueError:
            count_value_error += 1
            ba_calc = 0
        spread.append(ba_calc)
    return spread, time_list_hour, count_value_error


load_price_differences = int(input("Do you want to calculate price differences?"))
if load_price_differences:
    file_name = input("From what file do you want to load data? (raw data with time, price and volume) ")
    to_file = input("Name the output file: ") # should be named price differences something
    time_list = []
    prices = []
    volume = []
    data = jacob_csv_handling.read_single_csv(file_name, time_list, prices, volume)
    price_differences = jacob_support.first_price_differences(data[1]) # calculates price differences
    time_list = data[0]
    jacob_csv_handling.write_to_file(data[0], price_differences, to_file, "Price_differences")
else:
    file_name = input("From what file do you want to load price differences? ")
    time_list = []
    price_differences = []
    volume = []
    data = jacob_csv_handling.read_single_csv(file_name, time_list, price_differences) #price diffs now stored in data[1]
    price_differences = data[1]
    time_list = data[0]

window1 = 60 # calculate spread for this period of minutes
window2 = 60*8

print("The length of the price_diff: ", len(price_differences))

print("Calculates BA-spread:")

spread1, time_list_hour1, count_value_error_1 = rolls_new(price_differences, time_list, window1)
spread2, time_list_hour2, count_value_error_2 = rolls_new(price_differences, time_list, window2)

print(len(spread1))
print(len(spread2))

print("The following is the BAs with window",window1)
print(time_list_hour1)
print(spread1)
print("With",window1,"window,",count_value_error_1,"value errors were counted")

print("The following is the BAs with window",window2)
print(time_list_hour2)
print(spread2)
print("With",window2,"window,",count_value_error_2,"value errors were counted")

plt.plot(spread1)
plt.show()


