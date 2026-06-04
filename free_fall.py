from sys import float_repr_style

g = 9.81
print("---Welcome to Physics Lab---")
height = float(input("Please enter the height: "))
time = (2 * height / g)**0.5
velocity_final = g * time
print(f"The final velocity is: {velocity_final:.2f} and the time spend in air is: {time:.2f}")
