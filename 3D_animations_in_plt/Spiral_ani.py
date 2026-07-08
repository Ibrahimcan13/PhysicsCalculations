import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

t = 0
dt = 0.05

fig = plt.figure()
ax = fig.add_subplot(projection='3d')

ax.set_xlim3d([-5,5])
ax.set_ylim3d([-5,5])
ax.set_zlim3d([-5,5])

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

fig.patch.set_facecolor('black')
ax.set_facecolor('black')
ax.xaxis.set_pane_color((0,0,0,0))
ax.yaxis.set_pane_color((0,0,0,0))
ax.zaxis.set_pane_color((0,0,0,0))
ax.tick_params(colors='white')


trail, = ax.plot([], [], [], '-', lw=1.5, color='cyan', alpha=0.5)
ball, = ax.plot([], [], [], 'o', ms=10, color='cyan')

x_history, y_history, z_history = [], [], []


def update(frame):
    global t

    x = 4.0 * np.cos(t)
    y = 4.0 * np.sin(t)
    z = 4.0 * np.sin(t * 0.5)

    t += dt

    x_history.append(x)
    y_history.append(y)
    z_history.append(z)

    trail.set_data(x_history, y_history)
    trail.set_3d_properties(z_history)

    ball.set_data([x], [y])
    ball.set_3d_properties([z])

    return trail,ball
ani = FuncAnimation(fig, update, interval=4, blit=True, cache_frame_data=False)
plt.show()