# Import libraries
import numpy as np
import operator
from matplotlib import pyplot as plt
import pandas as pd
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import os

# Default file path for the sample file included in the repository
file_path = 'HR.csv'

# Check if the sample file exists
if not os.path.isfile(file_path):
    print(f"Error: The file {file_path} is missing.")
    exit(1)

# Import the Excel file
data = pd.read_csv(file_path, names=['Temp', 'Luminosity', 'Radius', 'Mag', 'Type', 'Color', 'Class'])

d = dict(tuple(data.groupby('Type'))) # Groups the data by star type

# Separates the data by star type
brown_dwarf = d['1']
white_dwarf = d['2']
main = d['3']
supergiant = d['4']
hypergiant = d['5']


# Sets up the x-variable as the log of Temperature
x1 = brown_dwarf['Temp']
x1 = [float(i) for i in x1]
x1 = np.array([np.log(i) for i in x1])

# Sets up the y variable as the log of Luminosity
y1 = brown_dwarf['Luminosity']
y1 = [float(i) for i in y1]
y1 = np.array([np.log(i) for i in y1])

x2 = white_dwarf['Temp']
x2 = [float(i) for i in x2]
x2 = np.array([np.log(i) for i in x2])

y2 = white_dwarf['Luminosity']
y2 = [float(i) for i in y2]
y2 = np.array([np.log(i) for i in y2])

x3 = main['Temp']
x3 = [float(i) for i in x3]
x3 = np.array([np.log(i) for i in x3])

y3 = main['Luminosity']
y3 = [float(i) for i in y3]
y3 = np.array([np.log(i) for i in y3])

x4 = supergiant['Temp']
x4 = [float(i) for i in x4]
x4 = np.array([np.log(i) for i in x4])

y4 = supergiant['Luminosity']
y4 = [float(i) for i in y4]
y4 = np.array([np.log(i) for i in y4])

x5 = hypergiant['Temp']
x5 = [float(i) for i in x5]
x5 = np.array([np.log(i) for i in x5])

y5 = np.array(hypergiant['Luminosity'])
y5 = [float(i) for i in y5]
y5 = [np.log(i) for i in y5]

# Resizes x and y to fit into the poly function
x3_new = np.reshape(x3, (80, -1))
y3_new = np.reshape(y3, (80, -1))

# Transforms the x values to an array with three values relating to 2 degrees of freedom
poly = PolynomialFeatures(degree=2)
transformx3 = poly.fit_transform(x3_new)

# Creates a variable to map a linear regression
model = LinearRegression()
model.fit(transformx3, y3_new)
y_poly_pred = model.predict(transformx3)
rmse = np.sqrt(mean_squared_error(y3_new, y_poly_pred)) # Calculates the root mean square value for data
sort_axis = operator.itemgetter(0)
sorted_zip = sorted(zip(x3_new, y_poly_pred), key=sort_axis)
x3_new, y_poly_pred = zip(*sorted_zip)
print(rmse)
# Plots the data
plt.figure(figsize= (6,8))
plt.title('Hertzsprung-Russell Diagram')
plt.xlabel(r'Temperature')
plt.ylabel(r'Luminosity')
plt.plot(x3_new, y_poly_pred)
plt.scatter(x1,y1, label='Brown Dwarf')
plt.scatter(x2,y2, label='White Dwarf')
plt.scatter(x3,y3, label='Main Sequence')
plt.scatter(x4,y4, label='Supergiant')
plt.scatter(x5,y5, label='Hypergiant')
plt.legend()
plt.show()