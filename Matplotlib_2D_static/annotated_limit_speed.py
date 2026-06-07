import matplotlib.pyplot as plt

limit_speed = 50
gravity = 9.81
time_list = list(range(0,21))
velocity_list = []

for time in range(0,21,1):
    velocity_current = gravity * time
    if velocity_current < limit_speed:
        velocity_list.append(velocity_current)
    else:
        velocity_list.append(limit_speed)

fig, ax = plt.subplots()
ax.plot(time_list,velocity_list, color='red', linestyle="solid")
ax.annotate(
    "Limit Speed",
    xy=(5.0968399592,50),
    xytext=(12,15),
    arrowprops=dict(facecolor="black",shrink=0.05, width=0.05, headwidth=10)
)
ax.set_xlabel("Time")
ax.set_ylabel("Velocity")
ax.grid(True, linestyle=":")
plt.show()