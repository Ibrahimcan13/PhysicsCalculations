import numpy as np
import matplotlib.pyplot as plt

u = np.linspace(0, 2*np.pi, 100)
v_input = float(input("Please etner a number between 0 and 10:"))
v = np.linspace(0, v_input, 100)
U, V =np.meshgrid(u, v)
R = float(input("Please enter the radius of the cylinder:"))
X= R * np.cos(U)
Y= R * np.sin(U)
Z = V

fig = plt.figure()
ax = fig.add_subplot(projection='3d')
ax.plot_surface(X, Y, Z , color='red')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title(' 3D Cylinder')
plt.show()