# Import libraries
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.colors import LogNorm
import pandas as pd
from scipy.optimize import curve_fit
import seaborn as sns
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

# Create an empty list to store half-life values
half_life = []

# Use curvefit to find half-life values for every unstable isotope
for i in range(len(list_chunked)):
    last_value = float(list_chunked[i].iloc[-1, 3])
    if last_value <= 80: # Determine if isotope is stable or unstable
        x = np.array(list(list_chunked[i].iloc[:, 2]), dtype=float)
        y = np.array(list(list_chunked[i].iloc[:, 3]), dtype=float)


        def model(t, alpha, beta):
            return alpha * np.exp(-beta * t)

        popt, pcov = curve_fit(model, x, y, p0=(100, 20))

        A0 = popt[0]
        lam = popt[1]
        t_half = np.log(2) / lam

        half_life.append(t_half)

        fit_line = model(x, A0, lam)

    elif last_value > 80: # Fill in half-life values for stable isotopes with given value
        half_life.append(1e33)

# Create a new dataframe with Z, N, and half-life
Z = [item.iloc[0,0] for item in list_chunked]
N = [item.iloc[0,1] for item in list_chunked]
Z = np.asarray(Z, dtype=float)
N = np.asarray(N, dtype=float)
half_life = np.asarray(half_life, dtype=float)

# Organize data for plotting
list_update = np.transpose([Z, N, half_life])
list_update_df = pd.DataFrame(list_update,columns=['Z', 'N', 'Half Life/s'])

plot_data = list_update_df.pivot(index='Z', columns='N', values='Half Life/s')
plot_data = pd.DataFrame(plot_data)

# Create heatmap
plt.figure(figsize=(10,6))
ax = sns.heatmap(plot_data, square=True, xticklabels=10, yticklabels=10, norm=LogNorm(),cmap='viridis', cbar_kws={'label': 'Half-life (s)'})
ax.invert_yaxis()
ax.set_title("Half-life of isotopes")
ax.set_xlabel("N")
ax.set_ylabel("Z")
plt.plot([0, 177], [0, 177])
plt.show()