import sympy as sp

x, y = sp.symbols('x y')

print("1. Basic Matrix Operations")


A = sp.Matrix([
    [1, 2],
    [3, 4]
])

print("Matrix A:")
sp.pprint(A)

print(f"\nTranspose of A (A^T):")
sp.pprint(A.T)

print(f"\nDeterminant of A det(A): {A.det()}")

print("\nInverse of A (A^-1):")
sp.pprint(A.inv())


print("\n 2. Eigenvalues & Eigenvectors ")

eigenvals = A.eigenvals()
print(f"Eigenvalues of A: {eigenvals}")

eigenvects = A.eigenvects()
print("\nEigenvectors of A:")
for val, mult, vec in eigenvects:
    print(f"Eigenvalue: {val} (Multiplicity: {mult})")
    print("Vector:")
    sp.pprint(vec[0])


print("\n3. Symbolic Matrix")

B = sp.Matrix([
    [x, y],
    [1, x]
])

print("Symbolic Matrix B:")
sp.pprint(B)

print(f"\nDeterminant of B: {B.det()}")


print("\n 4. Solving Linear System A * X = B ")


A_sys = sp.Matrix([
    [2, 1],
    [1, 3]
])

B_sys = sp.Matrix([5, 10])

X = A_sys.inv() * B_sys

print("Solution Vector X (x, y):")
sp.pprint(X)