import numpy as np
import matplotlib.pyplot as plt

fig = plt.subplots(figsize=(6,6))
ax = plt.axes(projection='3d')

x_positions = np.array([0,1])
y_positions = np.array([0,2])
z_positions = np.array([0,3])

ax.plot(x_positions,y_positions,z_positions,color= "red", linewidth = 2)

ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel=("Z")
plt.show()