import matplotlib.pyplot as plt

time_list = []
velocity_list = []
location_list = []
g=9.81

for time in range(0,16,2):
    velocity = g * time
    location = (g*time**2)/2
    time_list.append(time)
    velocity_list.append(velocity)
    location_list.append(location)


fig, ax = plt.subplots(1,2)
ax[0].plot(time_list, velocity_list, color = "red", linestyle = "solid" , marker = "s")
ax[0].set_xlabel("Time")
ax[0].set_ylabel("Velocity (m/s)")
ax[0].grid(True)

ax[1].plot(time_list, location_list, color = "blue", linestyle = "dashed" , marker = "o")
ax[1].set_xlabel("Time")
ax[1].set_ylabel("Location (m)")
ax[1].grid(True)

plt.tight_layout()
plt.show()