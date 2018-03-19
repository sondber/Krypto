import numpy as np
from sklearn.decomposition import PCA
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import scale
import data_import as di
from Jacob import jacob_support as js
from Sondre import sondre_support_formulas as supp

# Load data set
exchanges, time_list, prices, volumes, total_price, total_volume, currency = di.get_lists_legacy("h")
returns = js.logreturn(total_price)
year, month, day, hour, minute = supp.fix_time_list(time_list)
data = [returns, total_price, total_volume, year, month, day, hour, minute]

# convert it to numpy arrays
X = np.transpose(data)
# Scaling the values
X = scale(X)

pca = PCA(n_components=7)

pca.fit(X)

# The amount of variance that each PC explains
var= pca.explained_variance_ratio_

# Cumulative Variance explains
var1 = np.cumsum(np.round(pca.explained_variance_ratio_, decimals=4)*100)
print(var1)
plt.plot(var1)
plt.show()