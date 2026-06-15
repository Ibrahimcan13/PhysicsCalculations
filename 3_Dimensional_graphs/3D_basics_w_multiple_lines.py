import numpy as np
import matplotlib.pyplot as plt
x_road = np.array([0,1,3])
y_road = np.array([0,2,1])
z_road = np.array([0,3,5])

fig = plt.subplots(figsize=(6,6))
ax = plt.axes(projection='3d')

ax.plot(x_road,y_road,z_road, linestyle='-', marker='o', color='royalblue', linewidth=2, markersize=4, markerfacecolor='red', markeredgecolor='red')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

plt.show()

