# Import libraries
import numpy as np
from matplotlib import pyplot as plt
import pandas as pd
from scipy.optimize import curve_fit
import os

# Default file path for the sample file included in the repository
file_path = 'Q4.csv'

# Check if the sample file exists
if not os.path.isfile(file_path):
    print(f"Error: The file {file_path} is missing.")
    exit(1)

# Import the Excel file
data = pd.read_csv(file_path, names=['z', 'n', 't/s', 'A'])

data = data[1: -1]

# Separate the list by isotope
chunk = 20
list_chunked = [data[i: i + chunk] for i in range(0, len(data), chunk)]

# Determine a fit line for a single isotope of calcium
CA = [list_chunked[325]]

x = np.array(list(list_chunked[325].iloc[:, 2]), dtype=float)
y = np.array(list(list_chunked[325].iloc[:, 3]), dtype=float)

def model(t, alpha, beta):
    return alpha * np.exp(-beta * t)

popt, pcov = curve_fit(model,x, y, p0=(100, 12))

A0 = popt[0]
lam = popt[1]
t_half = np.log(2) / lam
print(A0, lam, t_half)
fit_line = model(x, A0, lam)

plt.figure(figsize= (8,6))
plt.scatter(x, y)
plt.plot(x, fit_line)
plt.title('Decay of CA-35')
plt.xlabel(r'Time $t$ / s')
plt.ylabel(r'Percentage of Population')
plt.minorticks_on()
plt.grid(which='major', linestyle='-')
plt.grid(which='minor', linestyle='--')
plt.rcParams['font.family'] = 'STIXGeneral'
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams["font.size"] = 12
plt.rcParams["font.weight"] = "normal"
plt.show()
