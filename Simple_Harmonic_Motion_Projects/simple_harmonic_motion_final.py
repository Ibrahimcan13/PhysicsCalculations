import numpy as np
import matplotlib.pyplot as plt


b= float(input("Enter damped force: "))
m=float(input("Enter mass: "))
gamma = b / (2*m)

freq_0= float(input("Enter frequency: "))
omega_0 = 2*np.pi*freq_0
omega_d = np.sqrt((omega_0**2)- (gamma**2))

A = float(input("Enter amplitude: "))
degree = int(input("Enter degree: "))
radian = np.radians(degree)

time = float(input("Enter time: "))
t = np.linspace(0,time, 1000)


#Theoric Values
x_theorical=  A * np.cos(omega_d *t + radian)
v_theorical= -A * omega_d * np.sin(omega_d *t + radian)
a_theorical= -(omega_d**2) * x_theorical

#Real Values

x_real = A * np.exp(-gamma * t) * np.cos(omega_d *t + radian)
v_real = -A * np.exp(-gamma * t) * (gamma * np.cos(omega_d *t + radian) + np.sin(omega_d *t + radian)*omega_d)
a_real = A * np.exp(-gamma * t) * (((gamma**2 - omega_d**2) * np.cos(omega_d *t + radian)) + (2 * gamma * omega_d * np.sin(omega_d *t + radian)))

fig, ax = plt.subplots(3,1, sharex=True)

ax[0].plot(t, x_theorical, color='blue', linestyle='-', label='Theorical Results', linewidth=2)
ax[0].plot(t, x_real, color='red', linestyle='solid', label='Real Results', linewidth=2)
ax[0].set_title("Real and Theorical results of position")
ax[0].set_ylabel("position")
ax[0].grid(True)
ax[0].legend()
ax[0].axhline(y=0, color='k', alpha=1)

ax[1].plot(t, v_theorical, color='blue', linestyle='-', label='Theorical Results', linewidth=2)
ax[1].plot(t, v_real, color='red', linestyle='solid', label='Real Results', linewidth=2)
ax[1].set_title("Real and Theorical results of velocity")
ax[1].set_ylabel("velocity")
ax[1].grid(True)
ax[1].legend()
ax[1].axhline(y=0, color='k', alpha=1)

ax[2].plot(t, a_theorical, color='blue', linestyle='-', label='Theorical Results', linewidth=2)
ax[2].plot(t, a_real, color='red', linestyle='solid', label='Real Results', linewidth=2)
ax[2].set_title("Theorical and Real results of acceleration")
ax[2].set_ylabel("acceleration")
ax[2].set_xlabel("time")
ax[2].grid(True)
ax[2].legend()
ax[2].axhline(y=0, color='k', alpha=1)

plt.tight_layout()
plt.show()
