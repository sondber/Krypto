
import numpy as np
import math
import matplotlib.pyplot as pltt
from Sondre import sondre_support_formulas as supp
import scipy
from scipy.optimize import curve_fit
import data_import as di
import data_import_support as dis
import os
import datetime as dt

import math
import numpy as np
import ILLIQ
exchanges, time_list, prices, volumes=di.get_lists(make_totals="no")
time_list_hour, prices_hour, volumes_hour = dis.convert_to_hour(time_list, prices, volumes)

#print(ILLIQ.ILLIQ_nyse_day(prices_hour[0,:],volumes_hour[0,:]))
print(prices_hour[0,0:14])

