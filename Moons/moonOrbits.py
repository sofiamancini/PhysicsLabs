# Import libraries
import numpy as np
from matplotlib import pyplot as plt
import pandas as pd
from scipy.optimize import curve_fit
import os

# Default file path for the sample file included in the repository
file_path = 'moon.csv'

# Check if the sample file exists
if not os.path.isfile(file_path):
    print(f"Error: The file {file_path} is missing.")
    exit(1)

# Import the Excel file
data = pd.read_csv(file_path, names=['Julian Date Io', 'Io','Julian Date Europa', 'Europa', 'Julian Date Ganymede', 'Ganymede','Julian Date Callisto', 'Callisto'])

data = data[1: -1]
G = 6.6743 * 10**-11

Io = np.asarray(data['Io'], dtype=float)
Io_date = np.asarray(data['Julian Date Io'], dtype=float)
Europa = np.asarray(data['Europa'], dtype=float)
Europa_date = np.asarray(data['Julian Date Europa'], dtype=float)
Ganymede = np.asarray(data['Ganymede'], dtype=float)
Ganymede_date = np.asarray(data['Julian Date Ganymede'], dtype=float)
Callisto = np.asarray(data['Callisto'], dtype=float)
Callisto_date = np.asarray(data['Julian Date Callisto'], dtype=float)

def model(t, amp, freq):
    return amp * np.cos(((2 * np.pi) * freq) * t)

popt_Io, pcov_Io = curve_fit(model,Io_date, Io, p0=(3, 1/1.75))
Io_amp = popt_Io[0]
Io_freq = popt_Io[1]
fit_line_Io = model(Io_date, Io_amp, Io_freq)

popt_Europa, pcov_Europa = curve_fit(model,Europa_date, Europa, p0=(5, 1/3.56))
Europa_amp = popt_Europa[0]
Europa_freq = popt_Europa[1]
fit_line_Europa = model(Europa_date, Europa_amp, Europa_freq)

popt_Ganymede, pcov_Ganymede = curve_fit(model,Ganymede_date, Ganymede, p0=(7.5, 1/7.15))
Ganymede_amp = popt_Ganymede[0]
Ganymede_freq = popt_Ganymede[1]
fit_line_Ganymede = model(Ganymede_date, Ganymede_amp, Ganymede_freq)

popt_Callisto, pcov_Callisto = curve_fit(model,Callisto_date, Callisto, p0=(13, 1/17))
Callisto_amp = popt_Callisto[0]
Callisto_freq = popt_Callisto[1]
fit_line_Callisto = model(Callisto_date, Callisto_amp, Callisto_freq)

amp = [np.abs(Io_amp), Europa_amp, Ganymede_amp, Callisto_amp]
r = np.asarray([i * 139820000 for i in amp], dtype=float)

freq = [Io_freq, Europa_freq, Ganymede_freq, Callisto_freq]
T = [1 / i for i in freq]
T = np.asarray([i * 86400 for i in T], dtype=float)

coeffs, V = np.polyfit(r**3, T**2, 1, cov=True)
poly_function = np.poly1d(coeffs)
trendline = poly_function(r**3)
gradient = coeffs[0]
intercept = coeffs[1]
correlation = np.corrcoef(r**3, T**2)

MJ = (4 * np.pi**2) / (G * gradient)
print(MJ)

plt.figure(figsize=(6,8))
plt.scatter(r**3, T**2)
plt.plot(r**3, trendline)
plt.minorticks_on()
plt.grid(which='major', linestyle='-')
plt.grid(which='minor', linestyle='--')
plt.title('Linear Graph of Radius and Amplitude')
plt.xlabel(r'Radius ($r**3$) / m')
plt.ylabel(r'Period ($T**2$) / s')

plt.figure(figsize=(8,5))
plt.axhline(0, color='black', linestyle='--')
plt.scatter(Io_date, Io, label = "Io")
plt.scatter(Europa_date, Europa, label = "Europa")
plt.scatter(Ganymede_date, Ganymede, label = "Ganymede")
plt.scatter(Callisto_date, Callisto, label = "Callisto")

plt.plot(Io_date, fit_line_Io)
plt.plot(Europa_date, fit_line_Europa)
plt.plot(Ganymede_date, fit_line_Ganymede)
plt.plot(Callisto_date, fit_line_Callisto)
plt.title('Orbital Paths of Jupiters Moons')
plt.xlabel(r'Time')
plt.ylabel(r'Location')

plt.legend()
plt.show()