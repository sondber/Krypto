import data_import as di
import realized_volatility as rv
from matplotlib import pyplot as plt
import numpy as np

v = []

m = [1, 2, 3, 4]
v.append(m)
n = [4, 5, 6, 7]

v.append(n)


timelist = [1, 2, 3, 4]

print(v)
print(v[0])

plt.plot(timelist, v[0])
plt.plot(timelist, v[1])
plt.show()