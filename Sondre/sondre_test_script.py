import numpy as np
import data_import as di
import plot
from Jacob import jacob_support as jake_supp
from Sondre import sondre_support_formulas as supp
import descriptive_stats as desc
import data_import_support as dis
import os
from matplotlib import pyplot as plt

os.chdir("/Users/sondre/Documents/GitHub/krypto")

exchanges, time_list, prices, volumes = di.get_lists(opening_hours="n", make_totals="n")
