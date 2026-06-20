import numpy as np
import matplotlib.pyplot as plt

x_smooth = np.linspace(-20,20,100)
y_smooth = np.linspace(-20,20,100)

x_grid , y_grid = np.meshgrid(x_smooth,y_smooth)
z_grid = np.sin(np.sqrt(x_grid**2 + y_grid**2))

n= int(input("Enter the number of points you want to plot: "))
x_data = np.random.uniform(-20,20,n)
y_data = np.random.uniform(-20,20,n)
z_data = np.random.rand(n)

fig = plt.figure()
ax = fig.add_subplot(projection='3d')
ax.plot_surface(x_grid, y_grid, z_grid, cmap='plasma', alpha=0.3)
ax.scatter(x_data, y_data,z_data, c='red', marker='o')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

plt.show()