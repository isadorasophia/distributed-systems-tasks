from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import numpy as np

## helpers
def harmonic(x):
    return len(x) / np.sum(1.0/x)

## fit a poly function of degree 3
def fit(x, y, space):
    # get our function
    fun = np.polyfit(x, y, 3)
    p = np.poly1d(fun)

    # plot it onto our space
    return p(space)

## data
# average
k2_avg = np.array([10.3, 11.0, 9.72, 16.04, 15.8])
k4_avg = np.array([17.6, 16.71, 19.43, 53.73, 72.0])
k8_avg = np.array([15.7, 42.85, 36.1, 85.09, 90.2])

# loss
k2_loss = np.array([38, 41, 50, 27, 18])
k4_loss = np.array([42, 42, 49, 19, 12])
k8_loss = np.array([49, 48, 47, 5, 1])

# loss
k2_info = np.array([1, 1, 994/1000., 3315.0/4000, 5174.0/8000])
k4_info = np.array([1, 1, 1, 3552.0/4000, 5200.0/8000])
k8_info = np.array([1, 1, 1, 839.0/4000, 1200.0/8000])

## x space
x = np.array([10, 100, 1000, 4000, 8000])
xp = np.linspace(10, 8000, 100)

## plot!
avg_plot2, = plt.plot(x, k2_info, 'r-', label='k=2', color='coral')
avg_plot4,  = plt.plot(x, k4_info, 'r-', label='k=4', color='teal')
avg_plot8,  = plt.plot(x, k8_info, 'r-', label='k=8', color='orange')

plt.legend(handles=[avg_plot8, avg_plot4, avg_plot2])

## pretty~
plt.title('Percentage of processes that received rumour')
plt.xlabel('N')
plt.xlim([10, 8000])
plt.xticks(x)
plt.ylabel('%')
plt.ylim([0, 1])
plt.show()
