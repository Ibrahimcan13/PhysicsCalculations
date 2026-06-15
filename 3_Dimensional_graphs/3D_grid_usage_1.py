import numpy as np
import matplotlib.pyplot as plt

x_line = np.linspace(-5, 5, 100)
y_line = np.linspace(-5, 5, 100)
x_grid, y_grid = np.meshgrid(x_line, y_line)

z_height = x_grid + y_grid

fig = plt.subplots(figsize=(6,6))
ax = plt.axes(projection='3d')

surface = ax.plot_surface(x_grid, y_grid, z_height, cmap= "viridis", edgecolor="none" )

ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_zlabel("z")
ax.set_title("3D plot")
plt.show()
plt.show()