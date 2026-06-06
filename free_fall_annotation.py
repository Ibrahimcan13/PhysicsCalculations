import matplotlib.pyplot as plt
from matplotlib.pyplot import title

time_list=[]
velocity_list=[]
g=9.81

for i in range(51):
    time = i/10
    velocity = time * g
    time_list.append(time)
    velocity_list.append(velocity)

fig, ax = plt.subplots()
ax.plot(time_list,velocity_list,  color = "red", linestyle = "solid")
ax.annotate(
    "Critical Velocity Limit",
    xy=(3,29.43),
    xytext=(2.3,40),
    arrowprops=dict(facecolor="black",shrink=0.05, width=0.05, headwidth = 8)

)
ax.set_xlabel("Time")
ax.set_ylabel("Velocity")
title("Noted velocity-time")
ax.grid(True)
plt.show()
