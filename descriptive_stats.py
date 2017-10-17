import numpy as np
from scipy import stats as sp


def stats_for_single_list(in_list, name):
    print()
    print("\033[32;0;0mFor %s \033[0;0;0m" % name)
    percs = [x for x in range(1,100) if x % 25 == 0]
    for p in percs:
        perc = np.percentile(in_list, p)
        print("%ith percentile: %0.3f" % (p, perc))
    variance = np.var(in_list)
    std = variance ** 0.5
    print("Variance: %0.2f" % variance)
    print("Standard deviation : %0.2f" % std)
    skew = sp.stats.skew(in_list)
    print("Skewness: %0.2f" % skew)
    kurt = sp.stats.kurtosis(in_list)
    print("Kurtosis: %0.2f" % kurt)
    for t in range(1, 24):
        auto = np.corrcoef(np.array([in_list[0:len(in_list) - t], in_list[t:len(in_list)]]))[0, 1]
        print("Autocorr. with %i periods lag: %0.3f" % (t, auto))


def combined_stats(list1, list2, name1="List 1", name2="List 2"):
    stats_for_single_list(list1, name1)
    stats_for_single_list(list2, name2)
    print()
    print("\033[32;0;0mCombined statistics \033[0;0;0m")
    corr = np.corrcoef(list1, list2)[0, 1]
    print("Correlation coefficient: %0.3f" % corr)

    # Does list1 precede list2?
    t = 1
    auto = np.corrcoef(np.array([list1[0:len(list1) - t], list2[t:len(list2)]]))[0, 1]
    print("Corr. where %s leads with %i periods: %0.3f" % (name1, t, auto))
    t = 2
    auto = np.corrcoef(np.array([list1[0:len(list1) - t], list2[t:len(list2)]]))[0, 1]
    print("Corr. where %s leads with %i periods: %0.3f" % (name1, t, auto))

    # Does list2 precede list1?
    t = 1
    auto = np.corrcoef(np.array([list2[0:len(list2) - t], list1[t:len(list1)]]))[0, 1]
    print("Corr. where %s leads with %i periods: %0.3f" % (name2, t, auto))
    t = 2
    auto = np.corrcoef(np.array([list2[0:len(list2) - t], list1[t:len(list1)]]))[0, 1]
    print("Corr. where %s leads with %i periods: %0.3f" % (name2, t, auto))
