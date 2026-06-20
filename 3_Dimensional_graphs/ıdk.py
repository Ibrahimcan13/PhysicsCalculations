import numpy as np
import matplotlib.pyplot as plt

n=int(input("enter the number of dots:"))
x_random = np.random.uniform(-20,20,n)
y_random = np.random.uniform(-20,20,n)
z_random = np.sin(np.sqrt(x_random**2 + y_random**2))

fig = plt.figure(figsize=(10,10))
ax = fig.add_subplot(projection='3d')

ax.scatter(x_random, y_random, z_random, color='red')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

plt.show()
