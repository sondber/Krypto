from Sondre import sondre_support_formulas as supp
import time
import numpy as np


def illiq_new(timestamps, minute_returns, minute_volumes, day_or_hour=1,
              kill_output=1):  # day=1 indicates daily measure, day_or_hour=0 indicates hourly measure
    year, month, day, hour, minute = supp.fix_time_list(timestamps)
    illiq = []
    time_list = []
    value_errors = 0

    # determine trading day yes/no
    if hour[0] == 0:  # this indicates that full day is being investigated
        hours_in_day = 24
        day_desc = "full day"
    else:
        hours_in_day = 6.5
        day_desc = "trading day"

    if day_or_hour == 1:
        window = int(hours_in_day * 60)
        freq_desc = "daily"
    else:
        window = int(60)
        freq_desc = "hourly"

    if kill_output == 0:
        print("Calculating ILLIQ on a/an", freq_desc, "basis using", day_desc, "data")

    partsum = 0

    if day_or_hour == 0 and hours_in_day == 6.5:  # seperate loop to take care of half hours
        half_hour = 30
        pos = 0  # position in price diff vector
        half = 1  # indicates that one half hour must be accounted for
        tod = 0  # tod to keep track of when to reset half
        while pos < len(minute_returns):  # looping through hours of day using the pos-var
            if half == 1:
                for i in range(pos, pos + half_hour):
                    #print("We are in the IF %d pos and %d i", pos, i)
                    try:
                        partsum += abs(minute_returns[i])/minute_volumes[i]
                    except ValueError:
                        value_errors += 1
                        partsum += 0
                window_illiq = partsum / half_hour
                illiq.append(window_illiq)
                time_list.append(timestamps[pos])

                half = 0
                pos += 30
                partsum = 0
            else:
                for i in range(pos, pos + window):
                    #print("We are in the ELSE  %d pos and %d i", pos, i)
                    try:
                        partsum += abs(minute_returns[i]), minute_volumes[i]
                    except ValueError:
                        value_errors += 1
                        partsum += 0
                window_illiq = partsum / window
                illiq.append(window_illiq)
                time_list.append(timestamps[pos])
                partsum = 0
                if tod == 5:
                    tod = 0
                    half = 1
                    pos += 60
                else:
                    tod += 1
                    pos += 60
    else:
        for i in range(0, len(minute_returns), window):  # looping through windows
            for j in range(i, i + window):  # looping through minutes in window
                #print("We are in the %d i and %d j",i,j)
                try:
                    partsum += abs(minute_returns[j])/minute_volumes[j]
                except ValueError:
                    value_errors += 1
                    partsum += 0
            window_illiq = partsum / window
            illiq.append(window_illiq)
            time_list.append(timestamps[i])

            partsum = 0

    if kill_output == 0:
        print("ILLIQ-calculation is finished")
        print("The length of the ILLIQ-vector is", len(illiq))
        print("The length of the time-vector is", len(time_list))
        print("Number of value errors:",value_errors)

    return time_list, illiq
