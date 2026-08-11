import numpy as np
import matplotlib.pyplot as plt

mass_input = float(input("Please enter the mass: "))
force_input = float(input("Please enter the force: "))
friction_input = float(input("Please enter the friction: "))
gravity = 9.81

friction_force = mass_input * friction_input * gravity
force_net = force_input - friction_force
acceleration_net = force_net / mass_input
time = np.linspace(0,10.1,100)
acceleration_array = np.full_like(time, acceleration_net)
velocity_net = acceleration_net * time

fig, ax = plt.subplots(2,1)
ax[0].plot(time, velocity_net, label = "velocity", color = "red", linewidth = 2.5, linestyle = "solid")
ax[0].axhline(color = "black", linewidth = 1.5)
ax[0].axvline(color = "black", linewidth = 1.5)
ax[0].legend()
ax[0].grid(True, linestyle = "--", linewidth = 1.5, alpha = 0.5)

ax[1].plot(time, acceleration_array, label = "acceleration", color = "blue", linewidth = 2.5, linestyle = "solid")
ax[1].axhline(color = "black", linewidth = 1.5)
ax[1].axvline(color = "black", linewidth = 1.5)
ax[1].legend()
ax[1].grid(True, linestyle = "--", linewidth = 1.5, alpha = 0.5)

plt.tight_layout()
plt.show()