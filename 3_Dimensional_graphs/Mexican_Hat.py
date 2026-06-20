import numpy as np
import matplotlib.pyplot as plt

x_axes = np.linspace(-5,5,500)
y_axes = np.linspace(-5,5,500)
x_grid, y_grid = np.meshgrid(x_axes, y_axes)

r = np.sqrt(x_grid**2 + y_grid**2)
z_grid = (1- r**2) * np.exp(-(r**2)/2)

fig = plt.figure()
ax = fig.add_subplot(projection='3d')
ax.plot_surface(x_grid, y_grid, z_grid, cmap='plasma', shade=True, antialiased=True)
ax.view_init(elev=30, azim=45)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title('Mexican Hat')
plt.show()
