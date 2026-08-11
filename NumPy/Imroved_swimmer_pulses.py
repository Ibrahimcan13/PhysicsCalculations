import numpy as np

pulse_matrixes = np.array([
    [140,165,120,185],
    [160,198,173,130]
])
print("ORIGINAL PULSE MATRIX")
print(pulse_matrixes)

global_max = np.max(pulse_matrixes)
print(f"Global Max: {global_max}")
print(" ")

swimmer_max = np.max(pulse_matrixes, axis=1)
print(f"Each swimmers Max: {','.join(swimmer_max.astype(str))}")
print(" ")

series_max = np.max(pulse_matrixes, axis=0)
print(f"Each series Max: {','.join(series_max.astype(str))}")
print(" ")