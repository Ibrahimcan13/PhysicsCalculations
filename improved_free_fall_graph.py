import matplotlib.pyplot as plt

time_list =[]
velocity_list =[]
location_list =[]
g=9.81

for i in range(51):
    time = i/10
    velocity = time * g
    location = 0.5*g*(time**2)
    time_list.append(time)
    velocity_list.append(velocity)
    location_list.append(location)

fig, ax = plt.subplots(1,2)
ax[0].plot(time_list,velocity_list,color = "red" , linestyle = "dashed")
ax[0].set_xlabel("Time")
ax[0].set_ylabel("Velocity")
ax[0].grid(True)

ax[1].plot(time_list,location_list,color = "green" , linestyle = "solid")
ax[1].set_xlabel("Time")
ax[1].set_ylabel("Location")
ax[1].grid(True)

plt.tight_layout()
plt.show()