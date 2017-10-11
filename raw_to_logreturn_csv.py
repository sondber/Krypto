import jacob_support
import jacob_csv_handling

print("######### Writing from raw data to return vector ############")
file_name = input("From what file do you want to load data? (raw data with time, price and volume) ")
to_file = input("Name the output file: ")
time_list = []
prices = []
volume = []

data = jacob_csv_handling.read_single_csv(file_name, time_list, prices, volume)
returns = jacob_support.logreturn(data[1])

jacob_csv_handling.write_to_file(data[0], returns, to_file,"Log_return")

