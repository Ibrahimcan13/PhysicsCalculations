import numpy as np

swimmer_pulse_matrixes = np.array([
    [140,165,120,180],
    [150,190,175,130]
])
print("Swimmer Pulse Matrix")
print(swimmer_pulse_matrixes)


limit_pulse = 160
higher_pulses = swimmer_pulse_matrixes[swimmer_pulse_matrixes>limit_pulse]

print("Higher Pulses")
print(*higher_pulses, sep=",")