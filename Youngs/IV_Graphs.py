# Import libraries
import numpy as np
from matplotlib import pyplot as plt
import pandas as pd
import os


# Import data
# Default file path for the sample file included in the repository
file_path = 'youngs.xlsx'

# Check if the sample file exists
if not os.path.isfile(file_path):
    print(f"Error: The file {file_path} is missing.")
    exit(1)

# Import the Excel file
data = pd.read_excel(file_path, 0, skiprows=1, names=['Volts', '1', '2', '3', '4'])

delta_V = 0.06
bulb_volts = np.asarray(data['Volts'].iloc[0:11], dtype=float)
b_avg = np.asarray(data['1'].iloc[0:11] + data['2'].iloc[0:11] + data['3'].iloc[0:11] + data['4'].iloc[0:11], dtype=float)
b_avg /= 4
std_bulb = np.std([data['1'].iloc[0:11], data['2'].iloc[0:11], data['3'].iloc[0:11], data['4'].iloc[0:11]], dtype=float, axis=0, ddof=1)
delta_bulb = 3.18 * std_bulb / np.sqrt(4)
for i in range (0, len(std_bulb)):
    if std_bulb[i] == 0.0:
        delta_bulb[i] = 0.05
    else:
        delta_bulb[i] = delta_bulb[i]
coeffs, V = np.polyfit(bulb_volts, b_avg, 2, cov=True)
poly_function = np.poly1d(coeffs)
trendline_bulb = poly_function(bulb_volts)
gradient_bulb = coeffs[0]
gradientb_error = np.sqrt(V[0][0])


LDR_volts = np.asarray(data['Volts'].iloc[12:23], dtype=float)
LDR_darkavg = np.asarray(data['1'].iloc[12:23] + data['2'].iloc[12:23], dtype=float)
LDR_darkavg /= 2
std_dLDR = np.std([data['1'].iloc[12:23], data['2'].iloc[12:23]], dtype=float, axis=0, ddof=1)
delta_dLDR = 12.7 * std_dLDR / np.sqrt(2)
for i in range (0, len(std_dLDR)):
    if std_dLDR[i] == 0.0:
        delta_dLDR[i] = 0.05
    else:
        delta_dLDR[i] = delta_dLDR[i]
coeffs, V = np.polyfit(LDR_volts, LDR_darkavg, 1, cov=True)
poly_function = np.poly1d(coeffs)
trendline_dLDR = poly_function(LDR_volts)
gradient_dLDR = coeffs[0]
gradientdL_error = np.sqrt(V[0][0])

LDR_lightavg = np.asarray(data['3'].iloc[12:23] + data['4'].iloc[12:23], dtype=float)
LDR_lightavg /= 2
std_lLDR = np.std([data['3'].iloc[12:23], data['4'].iloc[12:23]], dtype=float, axis=0, ddof=1)
delta_lLDR = 12.7 * std_lLDR / np.sqrt(2)
for i in range (0, len(std_lLDR)):
    if std_lLDR[i] == 0.0:
        delta_lLDR[i] = 0.05
    else:
        delta_lLDR[i] = delta_lLDR[i]
coeffs, V = np.polyfit(LDR_volts, LDR_lightavg, 1, cov=True)
poly_function = np.poly1d(coeffs)
trendline_lLDR = poly_function(LDR_volts)
gradient_lLDR = coeffs[0]
gradientlL_error = np.sqrt(V[0][0])

resis_volts = np.asarray(data['Volts'].iloc[24:35], dtype=float)
resis_avg = np.asarray(data['1'].iloc[24:35] + data['2'].iloc[24:35] + data['3'].iloc[24:35] + data['4'].iloc[24:35], dtype=float)
resis_avg /= 4
std_resis = np.std([data['1'].iloc[24:35], data['2'].iloc[24:35], data['3'].iloc[24:35], data['4'].iloc[24:35]], dtype=float, axis=0, ddof=1)
delta_resis = 3.18 * std_resis / np.sqrt(4)
for i in range (0, len(std_resis)):
    if std_resis[i] == 0.0:
        delta_resis[i] = 0.05
    else:
        delta_resis[i] = delta_resis[i]
coeffs, V = np.polyfit(resis_volts, resis_avg, 1, cov=True)
poly_function = np.poly1d(coeffs)
trendline_resis = poly_function(resis_volts)
gradient_resis = coeffs[0]
gradientr_error = np.sqrt(V[0][0])

therm_volts = np.asarray(data['Volts'].iloc[36:47], dtype=float)
therm_avg = np.asarray(data['1'].iloc[36:47] + data['2'].iloc[36:47] + data['3'].iloc[36:47] + data['4'].iloc[36:47], dtype=float)
therm_avg /= 4
std_therm = np.std([data['1'].iloc[36:47], data['2'].iloc[36:47], data['3'].iloc[36:47], data['4'].iloc[36:47]], dtype=float, axis=0, ddof=1)
delta_therm = 3.18 * std_therm / np.sqrt(4)
for i in range (0, len(std_therm)):
    if std_therm[i] == 0.0:
        delta_therm[i] = 0.05
    else:
        delta_therm[i] = delta_therm[i]
coeffs, V = np.polyfit(therm_volts, therm_avg, 1, cov=True)
poly_function = np.poly1d(coeffs)
trendline_therm = poly_function(therm_volts)
gradient_therm= coeffs[0]
gradientt_error = np.sqrt(V[0][0])


plt.figure(figsize= (6,8))
plt.minorticks_on()
plt.grid(which='major', linestyle='-')
plt.grid(which='minor', linestyle='--')
plt.rcParams['font.family'] = 'STIXGeneral'
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams["font.size"] = 12
plt.rcParams["font.weight"] = "normal"

plt.scatter(bulb_volts, b_avg)
plt.plot(bulb_volts, trendline_bulb)
plt.errorbar(bulb_volts, b_avg, xerr=delta_bulb, yerr=delta_V, ls='none', fmt='b', capsize=5)
plt.title('Voltage and Current in a Lightbulb')
plt.xlabel(r'Voltage ($V$) / V')
plt.ylabel(r'Current ($I$) / A')
plt.show()

plt.figure(figsize= (6,8))
plt.minorticks_on()
plt.grid(which='major', linestyle='-')
plt.grid(which='minor', linestyle='--')
plt.rcParams['font.family'] = 'STIXGeneral'
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams["font.size"] = 12
plt.rcParams["font.weight"] = "normal"

plt.scatter(LDR_volts, LDR_darkavg)
plt.plot(LDR_volts, trendline_dLDR)
plt.errorbar(LDR_volts, LDR_darkavg, xerr=delta_dLDR, yerr=delta_V, ls='none', fmt='b', capsize=5)
plt.title('Voltage and Current in an LDR Without Light')
plt.xlabel(r'Voltage ($V$) / V')
plt.ylabel(r'Current ($I$) / A')
plt.show()


plt.figure(figsize= (6,8))
plt.minorticks_on()
plt.grid(which='major', linestyle='-')
plt.grid(which='minor', linestyle='--')
plt.rcParams['font.family'] = 'STIXGeneral'
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams["font.size"] = 12
plt.rcParams["font.weight"] = "normal"

plt.scatter(LDR_volts, LDR_lightavg)
plt.plot(LDR_volts, trendline_lLDR)
plt.errorbar(LDR_volts, LDR_lightavg, xerr=delta_lLDR, yerr=delta_V, ls='none', fmt='b', capsize=5)
plt.title('Voltage and Current in an LDR')
plt.xlabel(r'Voltage ($V$) / V')
plt.ylabel(r'Current ($I$) / A')
plt.show()

plt.figure(figsize= (6,8))
plt.minorticks_on()
plt.grid(which='major', linestyle='-')
plt.grid(which='minor', linestyle='--')
plt.rcParams['font.family'] = 'STIXGeneral'
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams["font.size"] = 12
plt.rcParams["font.weight"] = "normal"

plt.scatter(resis_volts, resis_avg)
plt.plot(resis_volts, trendline_resis)
plt.errorbar(resis_volts, resis_avg, xerr=delta_resis, yerr=delta_V, ls='none', fmt='b', capsize=5)
plt.title('Voltage and Current in a Resistor')
plt.xlabel(r'Voltage ($V$) / V')
plt.ylabel(r'Current ($I$) / A')
plt.show()

plt.figure(figsize= (6,8))
plt.minorticks_on()
plt.grid(which='major', linestyle='-')
plt.grid(which='minor', linestyle='--')
plt.rcParams['font.family'] = 'STIXGeneral'
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams["font.size"] = 12
plt.rcParams["font.weight"] = "normal"

plt.scatter(therm_volts, therm_avg)
plt.plot(therm_volts, trendline_therm)
plt.errorbar(therm_volts, therm_avg, xerr=delta_therm, yerr=delta_V, ls='none', fmt='b', capsize=5)
plt.title('Voltage and Current in a Thermistor')
plt.xlabel(r'Voltage ($V$) / V')
plt.ylabel(r'Current ($I$) / A')
plt.show()
