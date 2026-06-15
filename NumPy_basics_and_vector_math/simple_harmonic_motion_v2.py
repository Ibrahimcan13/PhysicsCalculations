import numpy as np
import matplotlib.pyplot as plt

t = np.linspace(0,20,200)
A = float(input("Please enter the Ampitude:"))
degree = float(input("Please enter the degree: "))
radian = np.radians(degree)
freq = float(input("Please enter the frequency: "))
w = 2 * np.pi * freq
t =  np.linspace(0,20,400)

position_SHM =  A * np.cos(w*t + radian)
velocity_SHM = (-1)*A*w * np.sin(w*t + radian)
acceleration_SHM = (-1)*(w**2)* position_SHM

fig, ax = plt.subplots(3,1, sharex=True)

ax[0].plot(t,position_SHM, color="red")
ax[0].set_title("Position change in Simple Harmonic Motion")
ax[0].set_ylabel("Position")
ax[0].grid(True, alpha=0.5, linestyle='--')
ax[0].axhline(y=0, color="black", linestyle="solid")
ax[0].axvline(x=0, color="black", linestyle="solid")

ax[1].plot(t,velocity_SHM, color="blue")
ax[1].set_title("Velocity change in Simple Harmonic Motion")
ax[1].set_ylabel("Velocity")
ax[1].grid(True, alpha=0.5, linestyle='--')
ax[1].axhline(y=0, color="black", linestyle="solid")

ax[2].plot(t,acceleration_SHM, color="green")
ax[2].set_title("Acceleration change in Simple Harmonic Motion")
ax[2].set_ylabel("Acceleration")
ax[2].set_xlabel("Time")
ax[2].grid(True, alpha=0.5, linestyle='--')
ax[2].axhline(y=0, color="black", linestyle="solid")
ax[2].axvline(x=0, color="black", linestyle="solid")

plt.tight_layout()
plt.show()
