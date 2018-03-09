from Sondre import sondre_support_formulas as supp
import time
# Illiq as described in Amihud.
# Cuts any volumes less than "volume_limit". If all minutes in a window is zero, the window is omitted, resulting in a time-gap in the return-vector.


def illiq(timestamps, minute_returns, minute_volumes, hourly_or_daily="d",
          kill_output=1, threshold=0.05):
    year, month, day, hour, minute = supp.fix_time_list(timestamps)
    illiq = []
    time_list_illiq = []
    value_errors = 0
    zero_count_window = 0

    n_entries = len(timestamps)
    if hourly_or_daily == "d":
        start_hour = hour[0]
        start_minute = start_hour * 60 + minute[0]
    elif hourly_or_daily =="h":
        start_hour = hour[0]
        start_minute = 0

    hours_in_day = 24
    day_desc = "full day"

    if hourly_or_daily == "d":
        window = int(hours_in_day * 60)
        freq_desc = "daily"
    elif hourly_or_daily == "h":
        window = int(60)
        freq_desc = "hourly"

    if kill_output == 0:
        print("Calculating ILLIQ on a/an", freq_desc, "basis using", day_desc, "data")

    partsum = 0

    """
    if hourly_or_daily == 0 and hours_in_day == 6.5:  # seperate loop to take care of half hours
        pos = 0  # position in price diff vector
        half = 1  # indicates that one half hour must be accounted for
        tod = 0  # tod to keep track of when to reset half
        half_hour = 30
        while pos < len(minute_returns):  # looping through hours of day using the pos-var
            half_hour_adjusted = half_hour
            window_adjusted = window
            if half == 1:
                for i in range(pos, pos + half_hour):
                    # print("We are in the IF %d pos and %d i", pos, i)
                    if minute_volumes[i] <= threshold:
                        value_errors += 1
                        partsum += 0
                        window_adjusted -= 1
                    else:
                        partsum += abs(minute_returns[i]) / minute_volumes[i]
                if half_hour_adjusted != 0:
                    window_illiq = partsum / window_adjusted
                    illiq.append(window_illiq)
                    time_list.append(timestamps[pos])
                else:
                    zero_count_window += 1

                half = 0
                pos += 30
                partsum = 0
            else:
                for i in range(pos, pos + window):
                    # print("We are in the ELSE  %d pos and %d i", pos, i)
                    if minute_volumes[i] < threshold:
                        value_errors += 1
                        partsum += 0
                        window_adjusted -= 1
                    else:
                        partsum += abs(minute_returns[i]) / minute_volumes[i]
                if window_adjusted != 0:
                    window_illiq = partsum/window_adjusted
                    illiq.append(window_illiq)
                    time_list.append(timestamps[pos])
                else:
                    zero_count_window += 1

                partsum = 0

                if tod == 5:
                    tod = 0
                    half = 1
                    pos += 60
                else:
                    tod += 1
                    pos += 60
    """

    if hourly_or_daily == "d":
        window_adjusted = window - start_minute
        for j in range(0, window_adjusted):  # looping through minutes in window
            if minute_volumes[j] <= threshold:
                value_errors += 1
                partsum += 0
                window_adjusted -= 1
            else:
                partsum += abs(minute_returns[j]) / minute_volumes[j]
        if window_adjusted > 0:
            window_illiq = partsum / window_adjusted
            illiq.append(window_illiq)
            time_list_illiq.append(timestamps[0])
        else:
            zero_count_window += 1
        partsum = 0

    if hourly_or_daily == "d":
        second_iteration_start = window - start_minute
    else:
        second_iteration_start = 0

    for i in range(second_iteration_start, min(n_entries, n_entries-start_minute), window):  # looping through windows
        # if i in range(8000, 10000):
        #     print(" i =", i)
        #     print("  time[i] =", timestamps[i])
        #     print("  time[end] =", timestamps[min(i + window, n_entries)-1])
        #     print("  j from %i to %i" % (i, min(i + window, n_entries)))
        #     print("  volumes in this period", sum(minute_volumes[i:min(i + window, n_entries)]))

        window_adjusted = window
        for j in range(i, min(i + window, n_entries)):  # looping through minutes in window. min to ensure it does not exceed size of list
            if minute_volumes[j] <= threshold:
                value_errors += 1
                partsum += 0
                window_adjusted -= 1
            else:
                partsum += abs(minute_returns[j]) / minute_volumes[j]

        if window_adjusted > 0:
            window_illiq = partsum / window_adjusted
            illiq.append(window_illiq)
            time_list_illiq.append(timestamps[i])
            #print("  timestamp added:", timestamps[i])
        else:
            zero_count_window += 1
        partsum = 0

    if kill_output == 0:
        print("ILLIQ-calculation is finished")
        print("The length of the ILLIQ-vector is", len(illiq))
        print("The length of the time-vector is", len(time_list_illiq))
        print("Number of value errors:", value_errors)
        print("Number of zero-count windows", zero_count_window)

    return time_list_illiq, illiq
