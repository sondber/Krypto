import csv

def write_to_file(time, returns, fname):
    filename = fname
    n_rows = len(time)
    n_cols = 2
    print("Exporting data to "+filename+ " ...")
    with open(filename, 'w', newline='') as csvfile:
        header = ["Time", "Log_return"]
        write = csv.writer(csvfile, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        write.writerow(header)
        for i in range(0, n_rows):
            rowdata = [" "]
            rowdata[0] = time[i]
            rowdata.append(returns[i])
            write.writerow(rowdata)