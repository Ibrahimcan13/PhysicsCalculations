import numpy as np
import matplotlib.pyplot as plt


u = np.linspace(0,np.pi, 100)
v = np.linspace(0, 2*np.pi, 100)

U , V = np.meshgrid(u, v)

r = 4*(1-(np.cos(U)/2))
x_coordinate = r * np.cos(U) * np.cos(V) - np.sin(U) * np.cos(U) * np.sin(2*V)
y_coordinate = r * np.sin(U) * np.cos(V) - np.sin(U)* np.sin(U) * np.sin(2*V)
Z = 8 * np.sin(U)

fig = plt.figure(figsize=(10,7))
ax = fig.add_subplot(projection='3d')
ax.plot_surface(x_coordinate,y_coordinate,Z,cmap='jet')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title('Klein Bottle')
plt.show()