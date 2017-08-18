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
# sequential
seq = np.array([707, 737, 705, 704, 707, 730])

# multiprocess
mp_k2 = np.array([455, 456, 452, 454, 454, 454])
mp_k4 = np.array([412, 408, 409, 407, 412, 407])
mp_k8 = np.array([410, 412, 451, 419, 409, 412])

# multithread
mt_k2 = np.array([271, 264, 270, 270, 269, 271])
mt_k4 = np.array([236, 235, 235, 237, 237, 236])
mt_k8 = np.array([236, 233, 236, 237, 246, 236])

## x space
x = np.array([2, 4, 8])
xp = np.linspace(2, 8, 100)

## y space
seq_y = [harmonic(seq)] * len(x)
mp_y = [harmonic(mp_k2), harmonic(mp_k4), harmonic(mp_k8)]
mt_y = [harmonic(mt_k2), harmonic(mt_k4), harmonic(mt_k8)]

## plot!
seq_plot, = plt.plot(xp, fit(x, seq_y, xp), 'r-', label='Sequential', color='coral')
mp_plot,  = plt.plot(xp, fit(x, mp_y, xp), 'r-', label='Multiprocess', color='teal')
mt_plot,  = plt.plot(xp, fit(x, mt_y, xp), 'r-', label='Multithread', color='orange')
plt.legend(handles=[seq_plot, mp_plot, mt_plot])

## pretty~
plt.title('Execution time by each application')
plt.xlabel('K')
plt.xlim([2, 8])
plt.ylabel('t (ms)')
plt.ylim([0, 800])
plt.show()
