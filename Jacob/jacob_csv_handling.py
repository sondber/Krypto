import csv

def read_single_csv(file_name, time_list, price, volume):
    with open(file_name, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=';', quotechar='|')
        i = 0
        next(reader)
        next(reader)
        next(reader)
        for row in reader:
                time_list.append(row[0]) # Her leser den første kolonne og lagrer det
                price.append(float(row[1])) # Her leser den andre kolonne og lagrer det som float
                volume.append(float(row[2])) # Her leser den tredje kolonne og lagrer det som float
                i = i + 1
        return time_list, price, volume


def write_to_file(time, returns, fname, header_second_col):
    filename = fname
    n_rows = len(time)
    n_cols = 2
    print("Exporting data to "+filename+ " ...")
    with open(filename, 'w', newline='') as csvfile:
        header = ["Time", header_second_col]
        write = csv.writer(csvfile, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        write.writerow(header)
        for i in range(0, n_rows):
            rowdata = [" "]
            rowdata[0] = time[i]
            rowdata.append(returns[i])
            write.writerow(rowdata)
    print("The writing to file is done")


def read_currency_csv(file_name, timestamp, xrate): #timestamp, xrate are empty lists
    with open(file_name, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=';', quotechar='|')
        print("\033[0;32;0m Reading file '%s'...\033[0;0;0m" % file_name)
        i = 0
        next(reader)
        for row in reader:
            try:
                timestamp.append(str(row[0]))
                xrate.append(float(row[1]))
            except ValueError:
                print("\033[0;31;0m There was an error on row %i in '%s'\033[0;0;0m" % (i+1, file_name))
            i = i + 1
        return timestamp, xrate


