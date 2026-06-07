import matplotlib.pyplot as plt

limit_speed = 40
gravity = 9.81
time_list = list(range(0,31))
velocity_list = []
height_list = []

for i in range(0,31):
    velocity_current = gravity*i
    if velocity_current < limit_speed:
        current_height = 0.5*gravity*(i)**2
        height_list.append(current_height)
        velocity_list.append(velocity_current)
    else:
        velocity_list.append(limit_speed)
        current_height = current_height + limit_speed
        height_list.append(current_height)

fig, ax = plt.subplots()
ax.plot( time_list, height_list, color = "red", linestyle = "dashed", label = "Fall Distance")
ax.set_xlabel("Time(s))")
ax.set_ylabel("Height (m)")
ax.tick_params(axis='y', labelcolor="red")

ax2 = ax.twinx()

ax2.plot( time_list, velocity_list, color = "blue", label = "Fall Velocity", linestyle = "solid")
ax2.set_ylabel("Velocity (m/s)", color="blue")
ax2.tick_params(axis='y', labelcolor="blue")

ax.grid(True)
plt.show()