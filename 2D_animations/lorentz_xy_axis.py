import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

sigma = 10
rho = 28
beta = 8/3
x0 = float(input("Please enter the starting point in x axis (in meters): "))
y0 = float(input("Please enter the starting point in y axis (in meters): "))
z0 = float(input("Please enter the starting point in z axis (in meters): "))

fig, ax = plt.subplots()
ax.set_xlim(-25, 25)
ax.set_ylim(-35, 35)

line,= ax.plot([], [], lw=2, color='red')

fig.patch.set_facecolor('black')
ax.set_facecolor('white')
ax.spines['bottom'].set_color('black')
ax.spines['left'].set_color('black')
ax.tick_params(axis='both', colors='black')
ax.grid(True, color='white', linestyle='-', linewidth=1.2, alpha=0.5)
ax.set_title('Lorentz')

x_points, y_points, z_points = [x0], [y0], [z0]


def update(frame):
    x_current = x_points[-1]
    y_current = y_points[-1]
    z_current = z_points[-1]

    dt = 0.01
    dx = sigma * (y_current - x_current) * dt
    dy = (x_current * (rho - z_current) - y_current) * dt
    dz = (x_current * y_current - beta * z_current) * dt

    x_points.append(x_current + dx)
    y_points.append(y_current + dy)
    z_points.append(z_current + dz)

    line.set_data(x_points, y_points)

    return line,

ani = FuncAnimation(fig, update, interval=6,frames=40000, blit=True)
plt.show()