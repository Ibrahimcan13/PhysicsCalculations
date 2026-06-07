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

fig, ax = plt.subplots(1,2)
ax[0].plot(time_list,height_list, color='red',linestyle='solid',)
ax[0].set_xlabel('Time')
ax[0].set_ylabel('Height')
ax[0].set_title('Height Graph', color ="blue")
ax[0].grid(True)

ax[1].plot(time_list,velocity_list, color='black',linestyle='dashed')
ax[1].set_xlabel('Time')
ax[1].set_ylabel('Velocity')
ax[1].set_title('Velocity Graph', color ="brown")
ax[1].grid(True)
plt.show()
