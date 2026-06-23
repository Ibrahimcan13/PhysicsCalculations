import numpy as np
import matplotlib.pyplot as plt

u = np.linspace(0,np.pi, 1000)
v = np.linspace(0,2*np.pi, 1000)
U,V = np.meshgrid(u,v)
R = float(input("Enter radius of sphere: "))
X = R * np.sin(U) * np.cos(V)
Y = R * np.sin(U) * np.sin(V)
Z = R * np.cos(U)

fig = plt.figure()
ax = fig.add_subplot(projection='3d')
ax.plot_wireframe(X, Y, Z, cmap= 'plasma')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title('3D Sphere')
plt.show()
