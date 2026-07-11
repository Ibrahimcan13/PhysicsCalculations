import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

g = 9.81
omega = 0.0
damping = float(input('Enter damping rate: '))
deg_theta = float(input("Enter the degree: "))
theta = np.radians(deg_theta)
L = float(input("Enter the L: "))

fig, ax = plt.subplots()
ax.set_xlim(-20,20)
ax.set_ylim(-20,20)
line, = ax.plot([], [], lw=2, color='black')
ball, = ax.plot([],[], 'o' ,ms=10, color='red')

fig.patch.set_facecolor('white')
ax.set_facecolor('white')
ax.spines['bottom'].set_color('black')
ax.spines['left'].set_color('black')
ax.tick_params(axis='both', colors='black')
ax.grid(color='gray', linestyle='solid', linewidth=0.5, alpha=0.8)
ax.set_title('Simple Pendulum')
ax.set_xlabel('x')
ax.set_ylabel('y')

import numpy as np


def update(frame):
    global theta, omega

    dt = 0.02

    alpha = -(g / L) * np.sin(theta)

    omega += alpha * dt
    omega *= damping
    theta += omega * dt

    x = L * np.sin(theta)
    y = -L * np.cos(theta)

    line.set_data([0, x], [0, y])
    ball.set_data([x], [y])

    return line, ball,
ani = FuncAnimation(fig, update, interval=4,frames=40000, blit=True, repeat=True)
plt.show()