import numpy as np
from scipy import stats as sp
import data_import as di
import legacy
from Jacob import jacob_support as jake_supp


def compare_exchanges():
    exchanges, time_list, prices, volumes, total_price, total_volume = legacy.get_lists_legacy()

    bitstamp_price = prices[0, :]
    bitstamp_volume = volumes[0, :]
    bitstamp_returns = jake_supp.logreturn(bitstamp_price)
    btce_price = prices[1, :]
    btce_volume = volumes[1, :]
    btce_returns = jake_supp.logreturn(btce_price)
    combined_stats(bitstamp_returns, btce_returns, name1="Bitstamp", name2="List 2")


def stats_for_single_list(in_list, name, print_output=0):
    print()
    print("\033[32;0;0m%s: \033[0;0;0m" % name)
    #percs = [x for x in range(1,100) if x % 25 == 0]
    #for p in percs:
    #    perc = np.percentile(in_list, p)
    #    print("%ith percentile: %0.3f" % (p, perc))
    variance = np.var(in_list)
    std = variance ** 0.5
    mean = np.mean(in_list)
    minimum = min(in_list)
    maximum = max(in_list)
    skew = sp.stats.skew(in_list)
    kurt = sp.stats.kurtosis(in_list)

    if print_output == 1:
        print(" Min: %0.4f" % minimum)
        print(" Max: %0.4f" % maximum)
        print(" Mean: %0.4f" % mean)
        print(" Standard deviation : %0.4f" % std)
        print(" Kurtosis: %0.4f" % kurt)
        print(" Skewness: %0.4f" % skew)
        print(" Autocorrelation:")

    AC = []
    for t in [1, 10]:
        auto = np.corrcoef(np.array([in_list[0:len(in_list) - t], in_list[t:len(in_list)]]))[0, 1]
        if print_output == 1:
            print("  %i periods lag: %0.1f%%" % (t, auto*100))
        AC.append(auto)

    output = [name, minimum, maximum, mean, std, kurt, skew, AC[0], AC[1]]
    return output


def combined_stats(list1, list2, name1="List 1", name2="List 2"):
    list1 = np.array(list1)
    list2 = np.array(list2)
    print()
    print("\033[32;0;0mCombined statistics for %s and %s \033[0;0;0m" % (name1, name2))
    corr = np.corrcoef(list1, list2)[0, 1]
    print("Correlation coefficient: %0.1f%%" % (corr*100))

    # Does list1 precede list2?
    for t in [1, 3, 5, 10]:
        auto = np.corrcoef(np.array([list1[0:len(list1) - t], list2[t:len(list2)]]))[0, 1]
        print("Corr. where %s leads with %i periods: %0.1f%%" % (name1, t, auto*100))

    # Does list2 precede list1?
    for t in [1, 3, 5, 10]:
        auto = np.corrcoef(np.array([list2[0:len(list2) - t], list1[t:len(list1)]]))[0, 1]
        print("Corr. where %s leads with %i periods: %0.1f%%" % (name2, t, auto*100))
