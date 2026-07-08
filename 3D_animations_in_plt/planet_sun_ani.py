import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

dt = 0.01
G = 100
M_sun = 10

pos = np.array([4.0, 0.0, 1.0])
vel = np.array([0.0, 14.0, 5.0])

fig = plt.figure()
ax = fig.add_subplot(projection='3d')

ax.set_xlim3d(-7,7)
ax.set_ylim3d(-7,7)
ax.set_zlim3d(-7,7)

fig.patch.set_facecolor('black')
ax.set_facecolor('black')
ax.xaxis.set_pane_color((0,0,0,0))
ax.yaxis.set_pane_color((0,0,0,0))
ax.zaxis.set_pane_color((0,0,0,0))
ax.tick_params(colors='white')

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

sun, = ax.plot([0], [0], [0],'o',  ms=20, color='yellow')
earth, = ax.plot([], [], [] ,'o',  ms=10, color='lightblue')
trail, = ax.plot([], [], [] ,'-', lw=1, color='red')

x_history, y_history, z_history = [], [], []

def update(frame):
    global pos, vel, x_history, y_history, z_history

    r_vector = -pos #
    r_mag = np.linalg.norm(r_vector)

    acc = (G * M_sun / (r_mag**3)) * r_vector

    vel += acc * dt
    pos += vel * dt

    x_history.append(pos[0])
    y_history.append(pos[1])
    z_history.append(pos[2])

    trail.set_data(x_history, y_history)
    trail.set_3d_properties(z_history)

    earth.set_data([pos[0]], [pos[1]])
    earth.set_3d_properties([pos[2]])

    return trail, earth

ani = FuncAnimation(fig, update, interval=4, blit=True, cache_frame_data=False)
plt.show()