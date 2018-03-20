from Sondre import sondre_support_formulas as supp
import data_import_support as dis
import data_import as di
import numpy as np

full_list_excel_time = dis.make_excel_stamp_list(startstamp="01.09.2013 00:00", endstamp="31.12.2017 23:59")

n = len(full_list_excel_time)
price=np.zeros(n)
volume=np.zeros(n)