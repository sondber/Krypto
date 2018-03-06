import numpy as np


def remove_list1_outliers_from_all_lists(list1, list2=[], list3=[], list4=[], threshold=2):
    # threshold is in number of standard deviations
    # only chekcs for positive deviations
    t_list2 = False
    t_list3 = False
    t_list4 = False
    if len(list2) > 1:
        t_list2 = True
    if len(list3) > 1:
        t_list3 = True
    if len(list4) > 1:
        t_list4 = True

    n_in = len(list1)
    std = np.std(list1)
    mean = np.mean(list1)
    list1_min = mean - threshold * std
    list1_max = mean + threshold * std
    out_list1 = []
    if t_list2:
        out_list2 = []
    if t_list3:
        out_list3 = []
    if t_list4:
        out_list4 = []
    for i in range(0, n_in):
        if list1[i] < list1_max:
            out_list1.append(list1[i])
            if t_list2:
                out_list2.append(list2[i])
            if t_list3:
                out_list3.append(list3[i])
            if t_list4:
                out_list4.append(list4[i])
    if t_list4:
        return out_list1, out_list2, out_list3, out_list4
    elif t_list3:
        return out_list1, out_list2, out_list3
    elif t_list2:
        return out_list1, out_list2
    else:
        return out_list1