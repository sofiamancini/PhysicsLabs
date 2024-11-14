import numpy as np
from matplotlib import pyplot as plt
import pandas as pd
import os

# Default file path for the sample file included in the repository
file_path = 'JFET_data.xlsx'

# Check if the sample file exists
if not os.path.isfile(file_path):
    print(f"Error: The file {file_path} is missing.")
    exit(1)

# Import the Excel file
data = pd.read_excel(file_path, 0,  skiprows=1, names=['resistance', 'trial1' ,'trial2', 'trial3', 'trial4'])
deltaR = 5

avg_V = data['trial1'] + data['trial2'] + data['trial3'] + data['trial4']
avg_V /= 4

# Calculate error for voltage & replace zeros with least count
standard_deviationV = np.std([data['trial1'], data['trial2'], data['trial3'], data['trial4']], axis = 0, ddof=1)
delta_V = 3.18 * standard_deviationV / np.sqrt(4)
for i in range (0, len(standard_deviationV)):
    if standard_deviationV[i] == 0.0:
        delta_V[i] = 0.01
    else:
        delta_V[i] = delta_V[i]

I = avg_V / data['resistance']
deltaI = I * np.sqrt(np.square(delta_V/avg_V)+np.square(deltaR/data['resistance']))

coeffs = np.polyfit(I, avg_V, 3)
poly_function = np.poly1d(coeffs)
trendline = poly_function(I)
vt = poly_function(0)
print(vt)

# Creates x-variable for log graph
V = vt - avg_V

logI = np.log(I)
logV = np.log(V)

delta_logI = (deltaI/np.abs(I))
delta_logV = (delta_V/np.abs(V))

# Plots trendline for log graph
coeffs = np.polyfit(logV, logI, 1)
poly_function = np.poly1d(coeffs)
trendline = poly_function(logV)


# Uses the trendline to determine the gradient, intercept, and correlation
coeffs, V = np.polyfit(logV, logI, 1, cov=True)
gradient = coeffs[0]
intercept = coeffs[1]
correlation = np.corrcoef(logV, logI)[0, 1]
gradient_error = np.sqrt(V[0][0])

print(gradient)
print(gradient_error)

f = plt.figure(figsize=(8,10))
plt.scatter(logV, logI)
plt.plot(logV, trendline)

# Plots error bars
plt.errorbar(logV, logI, xerr=delta_logV, yerr=delta_logI, ls='none', fmt='b', capsize=5)


plt.minorticks_on()
plt.grid(which='major', linestyle='-')
plt.grid(which='minor', linestyle='--')
plt.rcParams['font.family'] = 'STIXGeneral'
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams["font.size"] = 12
plt.rcParams["font.weight"] = "normal"
plt.xlabel(r'ln($V_T - V_S$)')
plt.ylabel(r'ln($I$)')
plt.title('A Linear Graph of The Change in Voltage and Current in a JFET')

plt.show()
