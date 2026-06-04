print("Free Fall Calculation With Using Functions")
def calculation_of_time(height):
    g=9.81
    time = ((2 * height / g))** 0.5
    return time

height_input = float(input("Please enter the height: "))

calculated_time = calculation_of_time(height_input)
print(f"calculated_time is : {calculated_time:.3f}")