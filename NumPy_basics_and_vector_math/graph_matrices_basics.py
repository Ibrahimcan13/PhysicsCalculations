import numpy as np
import matplotlib.pyplot as plt

days = np.array([1,2,3,4,5])
laps = np.array([10,15,12,18,20])

plt.scatter(days, laps, color='red' , s=100 , marker='o')
plt.title("Weekly Training Schedule")
plt.xlabel("Days")
plt.ylabel("Laps")
plt.grid(True)
plt.show()