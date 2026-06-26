import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

x= np.linspace(0, 20*np.pi, 80000)
x0 = float(input("Please enter teh beggining point:"))
w = float(input("Please enter width:"))
A = float(input("Please enter the Amplitude:"))
k = float(input("Please enter the k:"))

fig, ax = plt.subplots(figsize=(8, 6))

ax.set_xlim(0, 20*np.pi)
ax.set_ylim(-A-1, A+1)

line, = ax.plot([], [], lw=2, color='red')

fig.patch.set_facecolor('black')
ax.set_facecolor('black')
ax.spines['bottom'].set_color('cyan')
ax.spines['left'].set_color('cyan')
ax.tick_params(axis='both', colors='cyan')
ax.grid(True, alpha=1.0, linestyle='-', linewidth=1.1)
ax.set_title('Gaussian wave packet')
ax.set_xlabel('x', color='cyan')
ax.set_ylabel('y', color='cyan')


def update(frame):
    t = frame / 10.0
    y = A * np.exp(-((x - x0 - t) / w) ** 2) * np.cos(k * x - 5 * t)
    line.set_data(x, y)
    return line,

ani = FuncAnimation(fig, update, frames=8000, blit=True , interval = 5.5)
plt.show()

