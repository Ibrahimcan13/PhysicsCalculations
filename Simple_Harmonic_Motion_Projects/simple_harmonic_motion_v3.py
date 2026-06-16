import numpy as np
import matplotlib.pyplot as plt


b = float(input("Please enter the damped force value: "))
la = float(input("Please enter the lamda value: "))
k = 2 * np.pi / la
A = float(input("Please enter the ampitude value: "))
radius = float(input("Please enter the radius value: "))
freq = float(input("Please enter the frequency value: "))
w = 2 * np.pi * freq
degree = float(input("Please enter the degree value: "))
radians = np.radians(degree)

#Theoric values of position velocity and acceleration

t= np.linspace(0, 12, 300)

x_theorical = A * np.cos(w * t + radians)
v_theorical =  -A * w * np.sin(w * t + radians)
a_theorical = -(w**2) * x_theorical

#Real results that probably I will get in Lab
r = np.linspace(0, radius, 300)

x_real = A * np.exp(-b * r) * np.cos(k * r)
v_real = -A * np.exp(-b * r) * (b * np.cos(k * r) + k * np.sin(k * r))
a_real = A * np.exp(-b * r) * (((b**2) - (k**2)) * np.cos(k * r) + 2 * b * k * np.sin(k * r))

fig, ax = plt.subplots(3,1)

ax[0].plot(t, x_theorical, color='red', linewidth=2, label='Theoric results', linestyle='--')
ax[0].plot(r,x_real, color='blue', linewidth=2, label='Real results')
ax[0].set_title("Theoric and real results of position")
ax[0].set_ylabel("Position")
ax[0].axhline(y=0, color='black', alpha =1)
ax[0].grid(True, alpha =0.3)
ax[0].legend()

ax[1].plot(t, v_theorical, color='red', linewidth=2, label='Theoric results', linestyle='--')
ax[1].plot(r,v_real, color='blue', linewidth=2, label='Real results')
ax[1].set_title("Theoric and real results of velocity")
ax[1].set_ylabel("Velocity")
ax[1].axhline(y=0, color='black', alpha =1)
ax[1].grid(True, alpha =0.3)
ax[1].legend()

ax[2].plot(t, a_theorical, color='red', linewidth=2, label='Theoric results', linestyle='--')
ax[2].plot(r,a_real, color='blue', linewidth=2, label='Real results')
ax[2].set_title("Theoric and real results of acceleration")
ax[2].set_xlabel("Red=Time ,Blue=Radius")
ax[2].set_ylabel("Acceleration")
ax[2].axhline(y=0, color='black', alpha =1)
ax[2].grid(True, alpha =0.3)
ax[2].legend()

plt.tight_layout()
plt.show()

