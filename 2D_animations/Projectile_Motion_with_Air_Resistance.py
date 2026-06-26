import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

g = 9.81
m = float(input("Enter the mass: "))
k = float(input("Enter the drag coefficient: "))
angle_deg = float(input("Enter the angle: "))
v0 = float(input("Enter the initial velocity: "))
x0 = float(input("Enter the initial x position: "))
y0 = float(input("Enter the initial y position: "))

angle_rad = np.radians(angle_deg)
vx = v0 * np.cos(angle_rad)
vy = v0 * np.sin(angle_rad)

x,y = x0,y0
x_points = [x]
y_points = [y]

fig, ax = plt.subplots(figsize=(10, 10))
ax.set_xlim(x0-5, 20*x0)
ax.set_ylim(y0-5, 2*y0)

line, = ax.plot([], [], lw=2, color = 'lime', label='Motion')

fig.patch.set_facecolor('black')
ax.set_facecolor('black')
ax.spines['bottom'].set_color('white')
ax.spines['left'].set_color('white')
ax.tick_params(axis='both', colors='white')
ax.grid(color='gray', linestyle='-', linewidth=0.5, alpha=0.8)
ax.set_title('Motion with Air Resistance')
ax.set_xlabel('x')
ax.set_ylabel('y')

def update(frame):
    global x, y, vx, vy
    dt = 0.01
    F_drag_x = -k * vx
    F_drag_y = -k * vy

    a_x = F_drag_x /m
    a_y = (F_drag_y /m)-g

    vx += a_x * dt
    vy += a_y * dt
    x += vx * dt
    y += vy * dt

    if y < 0:
        y = 0
        vx, vy = 0, 0
    x_points.append(x)
    y_points.append(y)

    line.set_data(x_points, y_points)
    return line,

ani = FuncAnimation(fig, update, frames=30000, interval=6, blit=True, repeat=False)
plt.show()