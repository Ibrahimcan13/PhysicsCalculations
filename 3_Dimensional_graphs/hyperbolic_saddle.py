import numpy as np
import matplotlib.pyplot as plt

x_axes = np.linspace(-20,20,1000)
y_axes = np.linspace(-20,20,1000)

x_grid, y_grid = np.meshgrid(x_axes, y_axes)
z_grid = (x_grid**2 - y_grid**2)

fig = plt.figure()
ax = fig.add_subplot(projection='3d')
ax.plot_surface(x_grid, y_grid, z_grid, cmap=plt.cm.Blues)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title("Hyperbolic saddle")
ax.contour(x_grid, y_grid, z_grid, cmap='plasma', offset=400 ,zdir='z')
plt.show()
