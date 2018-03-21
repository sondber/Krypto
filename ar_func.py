import numpy as np


def AR_matrix(Y, order=1):
    n = len(Y)

    ar_len = n - order

    if order == 1:
        X_AR = Y[0:ar_len]
    else:
        X_AR = np.zeros([order, ar_len])
        for i in range(0, order):
            X_AR[i] = Y[order - i - 1:n - (i + 1)]
    return X_AR

Y = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
order = 3
print("#########")
print("Original list:", Y)
print("#########")
print("Order:", order)
print("#########")


test = AR_matrix(Y, order)

for i in range(len(test)):
    print(i,"th line")
    print(test[:,i])

print("#########")
print("Full matrix:")
print(test)


