import  matplotlib.pyplot as plt
import numpy as np

sigma = 10.0
rho = 27.4
beta = 8/3

dt = 0.01
num_steps = 10000

x_values = np.empty(num_steps)
y_values = np.empty(num_steps)
z_values = np.empty(num_steps)

x_values[0] , y_values[0] , z_values[0] = (0.0, 1.0,1.05)

for i in range(1,num_steps-1):
    x = x_values[i]
    y = y_values[i]
    z = z_values[i]

    dxdt = sigma * (y-x)
    dydt = x * (rho - z) - y
    dzdt = x * y - beta * z

    x_values[i+1] = x + dxdt *dt
    y_values[i+1] = y + dydt *dt
    z_values[i+1] = z + dzdt *dt

fig = plt.subplots(figsize=(10,8))
ax = plt.axes(projection='3d')
ax.plot(x_values,y_values,z_values, color= "royalblue", lw=0.5)
ax.set_title("Lorentz Chaos", fontsize=14, color="black")
ax.set_xlabel("Convection Rate")
ax.set_ylabel("Temperature Difference")
ax.set_zlabel("Temperature Profile")

ax.set_facecolor("#f0f0f0")
plt.tight_layout()
plt.show()