import matplotlib.pyplot as plt

g = 9.81
time_list = [0,1,2,3,4,5,6,7,8,9,10]
height_list = []
for time in time_list:
    height = 0.5*g*(time)**2
    height_list.append(height)

fig, ax = plt.subplots()
ax.plot(time_list, height_list, color = "red",linestyle = "solid")
ax.set_xlabel("Time")
ax.set_ylabel("Height")
ax.grid(True)
plt.show()