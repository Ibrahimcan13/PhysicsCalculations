import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

G = 100.0
M = 10.0

x = 10.0
y = 0.0

vx = 0.0
vy = 8.0

fig, ax = plt.subplots()

ax.set_xlim([-25,25])
ax.set_ylim([-25,25])
planet, = ax.plot([0], [0], 'o', ms=20, color='red')
satellite, = ax.plot([], [], 'o', ms=8, color='yellow')

fig.patch.set_facecolor('black')
ax.set_facecolor('black')
ax.spines['bottom'].set_color('white')
ax.spines['left'].set_color('white')
ax.tick_params(axis='both', colors='white')
ax.grid(color='gray', linestyle='solid', linewidth=0.5, alpha=0.8)

def update(frame):
    global x, y, vx, vy

    dt = 0.01

    r = np.sqrt(x**2 + y**2)

    if r < 0.5:
        return satellite,

    a_total = (G * M) / (r**2)

    ax_force = -a_total * (x / r)
    ay_force = -a_total * (y / r)

    vx += ax_force * dt
    vy += ay_force * dt
    x += vx * dt
    y += vy * dt

    satellite.set_data([x], [y])
    return satellite,
ani = FuncAnimation(fig, update, interval=5, frames=30000, blit=True)
plt.show()