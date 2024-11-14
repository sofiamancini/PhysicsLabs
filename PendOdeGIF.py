# Imports all necessary libraries
import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.animation import PillowWriter

# This block sets up all initial system conditions
g = 10
miu = 0.05
mass = 1
L = 1
y0 = [1.0, 3.0]
t = np.linspace(0, 25, 1000)
b = miu / mass
c = g / L

# This function is used to calculate theta1 and theta2 (named omega for clarity)
def pend(y, t, b, c):
    theta, omega = y
    dydt = [omega, -b*omega - c*np.sin(theta)]
    return dydt
# Solves the system of differential equations
sol = odeint(pend, y0, t, args=(b, c))

# This sets up a figure to change through the animation
fig, ax = plt.subplots()
line, = plt.plot([], [], 'ro-', animated=True)

# This sets up the pivot point on the graph
pivot = np.array([0.0, 0.0])
radius = 0.05

# This function sets the limits for which the pendulum can move
def init():
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.5, 1.0)
    return line,

# This sets up the frame at each point i and updates the position of the ball for each i
def update(i):
    x_i = L * np.sin(sol[i, 0])
    y_i = -L * np.cos(sol[i, 0])
    ball = pivot + np.array([x_i, y_i])
    line.set_data([pivot[0], ball[0]], [pivot[1], ball[1]])
    return line,

# Creates the animation
anim = FuncAnimation(fig, update, init_func=init, frames=200, interval=100, blit=True)
anim.save("Pendulum_ODE.gif", writer=PillowWriter(fps=20))

plt.show()