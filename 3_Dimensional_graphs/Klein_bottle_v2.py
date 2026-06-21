import numpy as np
import matplotlib.pyplot as plt

u = np.linspace(0, np.pi, 100)
v = np.linspace(0, 2*np.pi, 100)
U, V = np.meshgrid(u, v)

cos_u = np.cos(U)
sin_u = np.sin(U)
cos_v = np.cos(V)
sin_v = np.sin(V)

X = -2/15 * cos_u * (3*cos_v - 30*sin_u + 90*cos_u**4*sin_u - 60*cos_u**6*sin_u + 5*cos_u*cos_v*sin_u)
Y = -1/15 * sin_u * (3*cos_v - 3*cos_u**2*cos_v - 48*cos_u**4*cos_v + 48*cos_u**6*cos_v - 60*sin_u + 5*cos_u*cos_v*sin_u - 5*cos_u**3*cos_v*sin_u - 80*cos_u**5*cos_v*sin_u + 80*cos_u**7*cos_v*sin_u)
Z = 2/15 * (3 + 5*cos_u*sin_u) * sin_v

fig = plt.figure(figsize=(10,7))
ax = fig.add_subplot(projection='3d')
ax.plot_surface(X, Y, Z, cmap='viridis', linewidth=0, antialiased=False, edgecolor='none', alpha=0.3)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title('Klein Bottle')
plt.show()