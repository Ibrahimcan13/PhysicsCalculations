import numpy as np
import matplotlib.pyplot as plt

u = np.linspace(0, 2 * np.pi, 100)
H = float(input("Enter height: "))
v = np.linspace(0, H, 100)
R = float(input("Enter radius: "))
U, V = np.meshgrid(u, v)

X = ((H-V)/H) * R * np.cos(U)
Y = ((H-V)/H) * R * np.sin(U)
Z = V

fig = plt.figure()
ax = fig.add_subplot(projection='3d')
ax.plot_surface(X, Y, Z, cmap='plasma')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title('Cone')
plt.show()