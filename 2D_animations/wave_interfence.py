import numpy as np
import matplotlib.pyplot as plt
from  matplotlib.animation import FuncAnimation

A = float(input("Please enter the amplitude (A): "))
k1 = float(input("Please enter the first wave number (k1): "))
k2 = float(input("Please enter the second wave number (k2): "))

x= np.linspace(0, 10 * np.pi, 10000)
fig, ax = plt.subplots(figsize=(8, 8))

ax.set_xlim(0, 10 * np.pi)
ax.set_ylim(-2*A -0.5, 2*A + 0.5)

line, = ax.plot([], [], lw=2, color='lime')

fig.patch.set_facecolor('black')
ax.set_facecolor('gray')
ax.spines['bottom'].set_color('white')
ax.spines['left'].set_color('white')
ax.tick_params(axis='both', colors='white')
ax.grid(True, color='gray', linestyle='-', linewidth=1.2, alpha=0.5)
ax.set_title('Wave Interfence')

def update(frame):
    t = frame / 20
    y1 = A * np.cos(k1 * x - t )
    y2 = A * np.cos(k2 * x - t )
    y = y1 + y2
    line.set_data(x, y)
    return line,
ani = FuncAnimation(fig, update, interval=6, blit=True, frames=4000)
plt.show()