import numpy as np
import matplotlib.pyplot as plt
import math

# Constants
g = 9.8             # Gravitational acceleration (m/s^2)
V0 = 700            # Initial velocity (m/s)
cd = 0.00004        # Drag coefficient
dt = 0.0001         # Time step (s)

# Angles in radians
theta = [np.radians(15), np.radians(30), np.radians(45), np.radians(60), np.radians(75)]

# Loop over each angle
for ang in theta:
    # Lists for trajectory with drag
    t_drag = [0]
    v_x_drag = [V0 * np.cos(ang)]
    v_y_drag = [V0 * np.sin(ang)]
    x_drag = [0]
    y_drag = [0]

    # Lists for trajectory without drag
    t_no_drag = [0]
    v_x_no_drag = [V0 * np.cos(ang)]
    v_y_no_drag = [V0 * np.sin(ang)]
    x_no_drag = [0]
    y_no_drag = [0]

    # Compute trajectory with drag
    i = 0
    while y_drag[i] >= 0:
        t_drag.append(t_drag[i] + dt)

        # Update velocities with drag
        drag_force = cd * (v_x_drag[i]**2 + v_y_drag[i]**2)
        ax_drag = -drag_force * (v_x_drag[i] / np.sqrt(v_x_drag[i]**2 + v_y_drag[i]**2))
        ay_drag = -g - drag_force * (v_y_drag[i] / np.sqrt(v_x_drag[i]**2 + v_y_drag[i]**2))

        v_x_drag.append(v_x_drag[i] + ax_drag * dt)
        v_y_drag.append(v_y_drag[i] + ay_drag * dt)

        # Update positions with drag
        x_drag.append(x_drag[i] + v_x_drag[i] * dt)
        y_drag.append(y_drag[i] + v_y_drag[i] * dt)

        i += 1

    # Compute trajectory without drag
    i = 0
    while y_no_drag[i] >= 0:
        t_no_drag.append(t_no_drag[i] + dt)

        # No drag, so only gravitational force acts in y-direction
        v_x_no_drag.append(v_x_no_drag[i])
        v_y_no_drag.append(v_y_no_drag[i] - g * dt)

        # Update positions without drag
        x_no_drag.append(x_no_drag[i] + v_x_no_drag[i] * dt)
        y_no_drag.append(y_no_drag[i] + v_y_no_drag[i] * dt)

        i += 1

    # Plot the trajectories for each angle
    angle_deg = round(np.degrees(ang), 1)
    plt.figure(1)
    plt.plot(x_drag, y_drag, label=f"{angle_deg}° (with drag)")
    
    plt.figure(2)
    plt.plot(x_no_drag, y_no_drag, label=f"{angle_deg}° (without drag)")

# Plot formatting for both figures
plt.figure(1)
plt.xlabel("Distance (m)")
plt.ylabel("Height (m)")
plt.title("Projectile Trajectory With Drag")
plt.legend()
plt.grid(True)

plt.figure(2)
plt.xlabel("Distance (m)")
plt.ylabel("Height (m)")
plt.title("Projectile Trajectory Without Drag")
plt.legend()
plt.grid(True)

# Show both figures
plt.show()
