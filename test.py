
import numpy as np
import math
import matplotlib.pyplot as plt
from Sondre import sondre_support_formulas as supp
import scipy
from scipy.optimize import curve_fit
import data_import as di
import data_import_support as dis
import os
import datetime as dt

import math
import numpy as np
import ILLIQ_old
exchanges, time_list, prices, volumes = di.get_lists(make_totals="no")
time_list_day, prices_day, volumes_day = dis.convert_to_day(time_list, prices, volumes)
year_list, month,day,hour, minute=supp.fix_time_list(time_list_day)

for i in range(400000,410000):
    print(i, time_list[i])


"""
def count(year_list,year):
    count = 0
    for i in range(len(year_list)):
        if year_list[i]==year:
            count=count+1
    return count
<<<<<<< HEAD
"""

=======

fig_count = 1
>>>>>>> f813c21a7ee4136e909adaf8aa01f53e4d2c3976
# print(sum(1 if year[x]==2012 else 0 for x in year))
#print(ILLIQ.ILLIQ_nyse_year(prices_day[0,:],volumes_day[0,:]))
#plt.plot([year_list[0],year_list[261],year_list[261*2],year_list[261*3],year_list[261*4],year_list[261*5]],ILLIQ.ILLIQ_nyse_year(prices_day[0,:],volumes_day[0,:]))
plt.figure(fig_count)
#plt.plot(ILLIQ.ILLIQ_nyse_window(prices_day[0,:],volumes_day[0,:],30))

#fig_count += 1
#plt.figure(fig_count)
plt.plot(ILLIQ_old.ILLIQ_nyse_window(prices_day[0, :], volumes_day[0, :], 7, remove_outliers="yes"))
plt.xlabel("week")
plt.ylabel("ILLIQ")
plt.ylim([0,0.00010])

plt.show()


#plt.plot(ILLIQ.ILLIQ_nyse_day(prices_day[0,:],volumes_day[0,:]))



