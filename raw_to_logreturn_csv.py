import logreturn
import csvreader
import csvwriter

print("######### Writing from raw data to return vector ############")
file_name = input("From what file do you want to load data? (raw data with time, price and volume) ")
to_file = input("Name the output file: ")
time_list = []
prices = []
volume = []

data = csvreader.read_single_csv(file_name, time_list, prices, volume)
returns = logreturn.logreturn(data[1])

csvwriter.write_to_file(data[0], returns, to_file)

