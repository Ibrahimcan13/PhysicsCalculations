import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

A = float(input("Please enter the ampitude: "))
b = float(input("Please enter the damped force: "))
k = float(input("Please enter the kinematic force: "))
x = np.linspace(0, 4 * np.pi, 1000)
fig, ax = plt.subplots(figsize=(10,6))

ax.set_xlim(0, 4* np.pi)
ax.set_ylim(-A -0.5, A+ 0.5)

line, = ax.plot([], [], lw=1.5, color='red')
fig.patch.set_facecolor('black')
ax.set_facecolor('gray')
ax.spines['bottom'].set_color('white')
ax.spines['left'].set_color('white')
ax.tick_params(axis='both', colors='white')
ax.grid(True, alpha=0.5)
ax.set_title('Damped harmonic oscillator')


def update(frame):
    t = frame / 20.0
    y = A * np.exp(-b * t) * np.cos(k * x - t)

    line.set_data(x, y)
    return line,
ani = FuncAnimation(fig, update, frames= 4000, interval=6, blit=True)
plt.show()