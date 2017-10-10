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