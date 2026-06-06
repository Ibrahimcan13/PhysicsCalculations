import matplotlib.pyplot as plt

x_list=[]
y_list=[]
g=9.81
velocity_initial = float(input("Enter initial velocity: "))

for i in range(41):
    time = i/10
    x_coordinate = velocity_initial * time
    y_coordinate = 0.5*g*(time**2)
    x_list.append(x_coordinate)
    y_list.append(y_coordinate)

fig, ax = plt.subplots()
ax.plot(x_list,y_list, color = "red", linestyle="solid")
ax.set(xlabel="x", ylabel="y",
title = f"Horizontal Projectile Motion, Velocity initial is equal to {velocity_initial}"
)

ax.invert_yaxis()
ax.grid(True)
plt.show()
