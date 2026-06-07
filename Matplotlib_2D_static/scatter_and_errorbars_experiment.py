import matplotlib.pyplot as plt

length_list = [0.2,0.4,0.6,0.8,1.0]
period_list = [0.92,1.25,1.58,1.81,2.05]
error_margin = 0.1

fig, ax = plt.subplots()
ax.scatter(length_list,period_list,c="red",marker="o",s=100,label="length")
ax.errorbar(length_list, period_list, yerr=error_margin, fmt="o-", ecolor="black", capsize=5)
ax.set_xlabel("Length")
ax.set_ylabel("Period")
ax.set_title("Scatter plot of length and period" , color = "brown")
ax.grid(True)

plt.show()