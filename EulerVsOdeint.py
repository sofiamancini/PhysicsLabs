# Imports all necessary libraries
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint


# This block sets up all initial system conditions
g = 10
miu = 0.05
mass = 1
L = 1
y0 = [1.0, 3.0]
theta = y0[0]
omega = y0[1]
t = np.linspace(0, 25, 100000)
b = miu / mass
c = g / L

# This function is used to calculate the differentials of theta1 and theta2 (named omega for clarity)
def pend(y, t, b, c):
    theta, omega = y
    dydt = [omega, -b*omega - c*np.sin(theta)]
    return dydt

# A function to perform one step of the Euler method
def step_euler(y, dt, pend):
    dydt = pend(y, t, b, c)
    return [y[i] + dt*dydt[i] for i in range(len(y0))]

# Solve the system of differential equations using the Euler method
y = np.zeros((len(t), len(y0)))
y[0] = y0
dt = 0.00025
for i in range(len(t)-1):
    y[i+1] = step_euler(y[i], dt, pend)

# This solves the differential equation using odeint from scipy
sol = odeint(pend,y0, t, args=(b, c))

final1 = sol[:,0] - y[:,0] # Delta theta 1
final2 = sol[:,1] - y[:,1] # Delta theta 2

# Creates a graph of the values of theta and omega as a function of time

fig, ax = plt.subplots(figsize = (10, 5))
ax2 = ax.twinx()
ax.plot(t, final1, 'b', label='Euler')
ax2.plot(t, final2, 'g', label='ODEint')
fig.legend(bbox_to_anchor=(0.25, 0.95))
ax2.set_ylim(-0.3, 0.3)
ax.set_ylim(-0.3, 0.3)
ax.set_xlabel('$t$ / s')
ax.set_ylabel(r'$\theta$ / rad s$^{-1}$')
ax2.set_ylabel(r'$\omega$ / rad s$^{-2}$')
plt.tight_layout()
plt.grid()
plt.minorticks_on()
plt.grid(which='major', linestyle='-')
plt.grid(which='minor', linestyle='--')
plt.title('A Graph of the Difference in Odeint and Euler Equations')

plt.show()
