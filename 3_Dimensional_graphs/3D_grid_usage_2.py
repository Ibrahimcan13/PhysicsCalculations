import numpy as np
import matplotlib.pyplot as plt

x_line = np.linspace(-20, 20, 500)
y_line = np.linspace(-20, 20, 500)

x_grid, y_grid = np.meshgrid(x_line, y_line)

r_number = np.sqrt(x_grid ** 2 + y_grid ** 2)
Z = np.sin(r_number)

fig = plt.subplots(figsize=(10, 10))
ax = plt.axes(projection="3d")

ax.plot_surface(x_grid, y_grid, Z, rstride=1, cstride=1, cmap=plt.cm.coolwarm)

ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_zlabel("z")
ax.set_title("3D plot")
plt.show()