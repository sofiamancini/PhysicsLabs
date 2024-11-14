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

# Calculates the logarithm of voltage
log_voltage = np.log(voltage_avg)

# This block of code sets all the parameters for the graphs
plt.rcParams['font.family'] = 'STIXGeneral'
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams["font.size"] = 12
plt.rcParams["font.weight"] = "normal"
f = plt.figure(figsize=(8, 10))

plt.xlabel(r'Time $t$ / s')
plt.ylabel(r' Log of Voltage ln($V$) / V')
plt.title('A Graph of the Log of Voltage ln($V$) / V vs Time $t$ / s')

plt.minorticks_on()
plt.grid(which='major', linestyle='-')
plt.grid(which='minor', linestyle='--')

# Creates a scatter plot using the average values of time and logarithm of voltage
plt.scatter(time_avg, log_voltage)

# Finds the trendline for a linear graph
coeffs = np.polyfit(time_avg, log_voltage, 1)
poly_function = np.poly1d(coeffs)
trendline = poly_function(time_avg)
plt.plot(time_avg, trendline)

# Uses the trendline to determine the gradient, intercept, and correlation
coeffs, V = np.polyfit(time_avg, log_voltage, 1, cov=True)
gradient = coeffs[0]
intercept = coeffs[1]
correlation = np.corrcoef(time_avg, log_voltage)[0, 1]

# Computes the gradient and intercept error
gradient_error = np.sqrt(V[0][0])
intercept_error = np.sqrt(V[1][1])


# Calculates the value for the Time constant and it's resulting error values
time_constant = -(1/gradient)
uncertain_T = time_constant * np.sqrt((gradient_error/gradient)**2)
print(f'The Time Constant for this capacitor is {time_constant:.2f} s with an error of {uncertain_T:.2f} s')

# Calculate the uncertainty for the measured values
standard_deviation_t = np.std([charging_capacitor['t1'], charging_capacitor['t2']], axis = 0, ddof=1)
delta_t = 12.7 * standard_deviation_t / np.sqrt(2)
standard_deviation_v = np.std([charging_capacitor['v1'], charging_capacitor['v2']], axis=0, ddof=1)
delta_V=np.zeros(len(standard_deviation_v))

# Replace zero values in standard deviation with least count
for i in range (0, len(standard_deviation_v)):
    if standard_deviation_v[i] == 0.0:
        delta_V[i] = 0.01
    else:
        delta_V[i] = 12.7 * standard_deviation_v[i] / np.sqrt(2)

log_deltaV = np.log(delta_V)

# Use the calculated uncertainty to plot error bars
plt.errorbar(time_avg, log_voltage, xerr=0.3, yerr=delta_V, ls='none', fmt='b', capsize=5)

calculated_graph = list(zip(time_avg, voltage_avg, log_voltage, delta_V, log_deltaV ))

df = pd.DataFrame(data=calculated_graph, columns=['Average Time', 'Average Voltage', 'Log Voltage', 'Delta V','Delta_Log_V'])

df.to_excel('calculated_graph.xlsx', index=False, header=True)

plt.show()
