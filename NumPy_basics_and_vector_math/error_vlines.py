import matplotlib.pyplot as plt
import numpy as np

t_theoric = np.linspace(0,10,500)
degree = float(input("Please enter the degree of rotation: "))
radian = np.radians(degree)
A =float(input("Please enter the ampitude: "))
freq = float(input("Please enter the frequency: "))
omega = 2*np.pi*freq
x_theorical = A * np.cos(omega * t_theoric + radian)

t_lab = np.array([1,2.5,4,5.5,7,8.5,10])
x_lab = np.array([4.2,-1.8,-4.7,2,5.3,-0.5,-4.2])

x_lab_theorical = A * np.cos(omega * t_lab + radian)

fig, ax = plt.subplots(figsize=(10,6))

ax.plot(t_theoric, x_theorical, color='red', linewidth=2, label='Theoric results')
ax.scatter(t_lab, x_lab, color='blue', marker='o', s=100, label='Lab results')

ax.vlines(t_lab, ymin=x_lab, ymax=x_lab_theorical, color='purple', linewidth=2 , alpha=0.8, label='Difference of theorical and real results', zorder=1)

ax.set_title('Theoric and Lab results')
ax.set_xlabel('Time(s)')
ax.set_ylabel("Position(m)")
ax.axhline(y=0, color='black', linewidth=2)
ax.axvline(x=0, color='black', linewidth=2)
ax.legend()

plt.show()