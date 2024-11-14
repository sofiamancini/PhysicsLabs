import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter

# System parameters
g = 10
miu = 0.05
mass = 1
L = 1
y0 = [1.0, 3.0]  # Initial theta and omega
b = miu / mass
c = g / L
t = np.linspace(0, 25, 2000)  # Fewer time steps for faster computation
dt = t[1] - t[0]  # New dt based on reduced time steps

# Euler method to solve the differential equation
y = np.zeros((len(t), len(y0)))
y[0] = y0
for i in range(len(t) - 1):
    theta, omega = y[i]
    dydt = [omega, -b * omega - c * np.sin(theta)]
    y[i + 1] = [y[i][j] + dt * dydt[j] for j in range(len(y0))]

# Animation setup
fig, ax = plt.subplots()
line, = plt.plot([], [], 'ro-', animated=True)
pivot = np.array([0.0, 0.0])

def init():
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.5, 1.0)
    return line,

def update(i):
    x_i = L * np.sin(y[i, 0])
    y_i = -L * np.cos(y[i, 0])
    ball = pivot + np.array([x_i, y_i])
    line.set_data([pivot[0], ball[0]], [pivot[1], ball[1]])
    return line,

# Create the animation
anim = FuncAnimation(fig, update, init_func=init, frames=len(t), interval=10, blit=True)
anim.save("Pendulum_Euler.gif", writer=PillowWriter(fps=20))

plt.show()
