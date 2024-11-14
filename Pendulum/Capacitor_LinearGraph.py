import pandas as pd
from scipy.optimize import curve_fit
import numpy as np
from matplotlib import pyplot as plt
import os

# Default file path for the sample file included in the repository
file_path = 'Discharging a Capacitor.xlsx'

# Check if the sample file exists
if not os.path.isfile(file_path):
    print(f"Error: The file {file_path} is missing.")
    exit(1)

# Import the Excel file
charging_capacitor = pd.read_excel(file_path, 0, skiprows=0, names=['t1', 'v1', 't2', 'v2'])


# Find each of the average values across time and voltage
time_avg = charging_capacitor['t1'] + charging_capacitor['t2']
time_avg /= 2
voltage_avg = charging_capacitor['v1'] + charging_capacitor['v2']
voltage_avg /= 2

# This block of code sets all the parameters for the graphs
plt.rcParams['font.family'] = 'STIXGeneral'
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams["font.size"] = 12
plt.rcParams["font.weight"] = "normal"
f = plt.figure(figsize=(8, 10))

plt.minorticks_on()
plt.grid(which='major', linestyle='-')
plt.grid(which='minor', linestyle='--')

plt.xlabel(r'Time $t$ / s')
plt.ylabel(r'Voltage $V$ / V')
plt.title('A Graph of Voltage $V$/V vs Time $t$/s')

# Creates a scatter plot using the average values of time and voltage
plt.scatter(time_avg, voltage_avg)

# This variable is the given function that relates voltage, time, and time constant of the discharging capacitor
def trend(t, V0, T):
    return (V0 * np.exp(-t / T))

# Curve_fit estimates the best fit line for the function defined above
[popt, pcov] = curve_fit(trend, time_avg, voltage_avg, p0=(9,100))

# The first value obtained in the curve_fit function is the time constant
time_constant = popt[1]
# Error is calculated as the square root of the square covariance
uncertain_T = np.sqrt(pcov[1][1])
print(f'The Time Constant for this capacitor is {time_constant:.2f} s with an error of {uncertain_T:.2f} s')

# This variable stores the value of the trendline
fit_line = trend(time_avg, popt[0], popt[1])
plt.plot(time_avg, fit_line)

# Calculate the uncertainty for the measured values
standard_deviation_t = np.std([charging_capacitor['t1'], charging_capacitor['t2']], axis=0, ddof=1)
delta_t = 12.7 * standard_deviation_t / np.sqrt(2)
standard_deviation_v = np.std([charging_capacitor['v1'], charging_capacitor['v2']], axis=0, ddof=1)
delta_V = np.zeros(len(standard_deviation_v))

# Replace zero values in standard deviation with least count
for i in range (0, len(standard_deviation_v)):
    if standard_deviation_v[i] == 0.0:
        delta_V[i] = 0.01
    else:
        delta_V[i] = 12.7 * standard_deviation_v[i] / np.sqrt(2)

# Use the calculated uncertainty to plot error bars
plt.errorbar(time_avg, voltage_avg, xerr=0.3, yerr=delta_V, ls='none', fmt='b', capsize=5)

# Displays the scatter plot, trendline, and error bars on one graph
plt.show()
