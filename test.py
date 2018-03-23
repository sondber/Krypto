import numpy as np
import data_import as di
import matplotlib.pyplot as plt
import plot
from Jacob import jacob_support as jake_supp
from Sondre import sondre_support_formulas as supp
import data_import_support as dis
import os
import rolls
import scipy.stats as st
import ILLIQ
import realized_volatility
import math

spread_row = [1, 2]
spread_row = np.matrix(spread_row)
print(spread_row)
spread_master = spread_row
print(spread_master)

spread_row = [3, 4]
spread_row = np.matrix(spread_row)

print(spread_row)
spread_master = np.append(spread_master, spread_row, axis=0)

print(spread_master)


print("testing")

test_arr = [1, 2, 3, 4, 5]
print(test_arr)
remove = [1,3]
test_arr = np.delete(test_arr, remove)
print(test_arr)
