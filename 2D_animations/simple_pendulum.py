import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

g = 9.81
L = float(input("Enter the length of the rope :"))
theta0 = float(input("Enter the angle of the rope:"))
rad_theta = np.radians(theta0)

theta = rad_theta
omega = 0.0
x_points = []
y_points = []

fig, ax = plt.subplots()
ax.set_xlim(-1-L,1+L)
ax.set_ylim(-L-1,1+L)
line, = ax.plot([], [], lw=2, color='pink')

fig.patch.set_facecolor('black')
ax.set_facecolor('black')
ax.spines['bottom'].set_color('white')
ax.spines['left'].set_color('white')
ax.tick_params(axis='both', colors='white')
ax.grid(color='gray', linestyle='solid', linewidth=0.5, alpha=0.8)
ax.set_title('Simple Pendulum')
ax.set_xlabel('x')
ax.set_ylabel('y')


def update(frame):
    global theta, omega

    dt = 0.01

    alpha = -(g / L) * np.sin(theta)

    omega += alpha * dt
    theta += omega * dt

    x = L * np.sin(theta)
    y = -L * np.cos(theta)

    line.set_data([0, x], [0, y])

    return line,

ani = FuncAnimation(fig, update, interval=6,frames=30000, blit=True)
plt.show()