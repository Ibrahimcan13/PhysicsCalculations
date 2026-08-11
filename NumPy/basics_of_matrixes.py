import numpy as np

sensor_matrix = np.array([
    [12,45,55,23],
    [62,18,34,70]
])
print("Original Matrix")
print(sensor_matrix)
print("Shape of the matrix:", sensor_matrix.shape)

limit_speed = 50
problematic_matrix_ones = sensor_matrix[sensor_matrix>limit_speed]

print("Problematic Matrixes")
print(problematic_matrix_ones)