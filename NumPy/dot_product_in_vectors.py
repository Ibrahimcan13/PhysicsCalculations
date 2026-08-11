import numpy as np

A_matrix = np.array([
    [3,2],
    [0,4]
])
B_matrix = np.array([
    [2,1],
    [3,5]
])
print("Here is the A matrix:")
print(A_matrix)

print("Here is the B matrix:")
print(B_matrix)

C_matrix = A_matrix @ B_matrix

print("Here is the C matrix:")
print(C_matrix)