import numpy as np
import matplotlib.pyplot as plt

mass = float(input("Please enter the mass: "))
velocity = np.arange(0,21,5)
kinetic_energy = 0.5 * mass * velocity**2

fig, ax = plt.subplots()
ax.plot(velocity, kinetic_energy, color='red', marker='o', linestyle='-', markersize=8, alpha = 0.8, markerfacecolor='blue', markeredgecolor='blue')
ax.set(xlabel='x', ylabel='y', title='Velocity and Kinetic Energy')
ax.grid(True, alpha=0.5)
plt.show()