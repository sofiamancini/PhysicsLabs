import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
import math


# Set up constants
g = 10
L = 10
C = 3/np.sqrt(g/L)
theta_0 = 0.1
omega_0 = 0 # initial angular velocity
t = np.linspace(0, 10, 1000)

# Set up the differential equation
def damped_pendulum(y, t, C):
    theta, omega = y
    dydt = [omega, -C*omega - g/L*math.sin(theta)]
    return dydt

# Solve the differential equation
y0 = [theta_0, omega_0]
sol = odeint(damped_pendulum, y0, t, args=(C,))
theta = sol[:, 0]

# Plot the solution
plt.plot(t, theta)
plt.xlabel('Time ($s$)')
plt.ylabel(r'$\theta$' + ' ($rad$)')
plt.title('Damped Pendulum - Numerical Solution')
plt.grid()
plt.minorticks_on() 
plt.grid(which='major', linestyle='-')
plt.grid(which='minor', linestyle='--')
plt.show()

# Proof using equations
beta = 3/2 * np.sqrt(g/L)
omega_2 = np.sqrt((5*g)/(4*L))
A1 = (theta_0*(beta + omega_2)/(2*omega_2))
A2 = theta_0 * (omega_2 - beta)/(2*omega_2)

theta_t = np.exp(-beta*t)*(A1*np.exp(omega_2*t) + A2*np.exp(-omega_2*t))

plt.plot(t, theta_t)
plt.xlabel('Time ($s$)')
plt.ylabel(r'$\theta$' + ' ($rad$)')
plt.title('Damped Pendulum - Analytical Solution')
plt.grid()
plt.minorticks_on() 
plt.grid(which='major', linestyle='-')
plt.grid(which='minor', linestyle='--')
plt.show()