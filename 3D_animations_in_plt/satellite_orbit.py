import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

dt = 0.01
G = 100
M_planet = 10

pos = np.array([2.0, 2.0, 2.0])
vel = np.array([0.0, 0.0, 15.81])

fig = plt.figure()
ax = fig.add_subplot(projection='3d')

ax.set_xlim3d([-5, 5])
ax.set_ylim3d([-5, 5])
ax.set_zlim3d([-5, 5])

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

fig.patch.set_facecolor('black')
ax.set_facecolor('black')
ax.xaxis.set_pane_color((0, 0, 0, 0))
ax.yaxis.set_pane_color((0, 0, 0, 0))
ax.zaxis.set_pane_color((0, 0, 0, 0))
ax.tick_params(colors='lime')

planet, = ax.plot([0], [0], [0], 'o', ms=25, color='green')
trail, = ax.plot([], [], [], '-', lw=1.5, color='cyan', alpha=0.5)
satellite, = ax.plot([], [], [], 'o', ms=8, color='cyan')

x_history, y_history, z_history = [], [], []

def update(frame):
    global pos, vel, x_history, y_history, z_history

    r_vector = -pos
    r_mag = np.linalg.norm(r_vector)

    acc = (G * M_planet / (r_mag**3)) * r_vector

    vel += acc * dt
    pos += vel * dt

    x_history.append(pos[0])
    y_history.append(pos[1])
    z_history.append(pos[2])

    trail.set_data(x_history, y_history)
    trail.set_3d_properties(z_history)

    satellite.set_data([pos[0]], [pos[1]])
    satellite.set_3d_properties([pos[2]])

    return trail, satellite

ani = FuncAnimation(fig, update, interval=4, blit=True, cache_frame_data=False)
plt.show()