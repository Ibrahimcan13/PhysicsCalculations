import numpy as np
import matplotlib.pyplot as plt

# 1. Izgara oluşturma (100x100)
x_smooth = np.linspace(-20, 20, 100)
y_smooth = np.linspace(-20, 20, 100)
x_grid, y_grid = np.meshgrid(x_smooth, y_smooth)

# DÜZELTME BURADA: smooth yerine grid değişkenlerini kullanıyoruz
z_grid = np.sin(np.sqrt(x_grid**2 + y_grid**2))

# 2. Rastgele noktalar
n = 50
x_random = np.random.uniform(-20, 20, n)
y_random = np.random.uniform(-20, 20, n)
z_random = np.sin(np.sqrt(x_random**2 + y_random**2))

fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(projection='3d')

# Yüzey ve noktalar
ax.plot_surface(x_grid, y_grid, z_grid, alpha=0.3, cmap=plt.cm.Spectral)
ax.scatter(x_random, y_random, z_random, color='red', s=30)

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
plt.show()