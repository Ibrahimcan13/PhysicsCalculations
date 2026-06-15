import numpy as np
import matplotlib.pyplot as plt

t = np.linspace(0, 4 * np.pi, 100)

x_road = np.cos(t)
y_road = np.sin(t)
z_road =(t)

fig = plt.subplots(figsize=(6,6))
ax = plt.axes(projection='3d')

ax.plot(x_road, y_road, z_road, color='green', linewidth=3)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title('3D Spiral Problem')
plt.show()