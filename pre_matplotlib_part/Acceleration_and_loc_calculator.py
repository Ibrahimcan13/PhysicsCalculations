import time

print("2D Physics Simulator! ")

def motion_calculator():
    try:
        mass = float(input("Please enter the mass (kg): "))
        force = float(input("Please enter the force (N): "))
        time_1 = int(input("Please enter the time (seconds): "))

        if mass <=0 or force <= 0 or time_1 <= 0:
            print("Please use only valid values!")
            return

        acceleration = force/mass
        print(f"The acceleration is: {acceleration}")
        print("Simulation has begun! ")

        velocity = 0
        location = 0
        for t in range(1, time_1+1):
            time.sleep(1)

            old_velocity = velocity
            velocity += acceleration
            location += (old_velocity + velocity)/2

            print(f"Seconds: {t} velocity: {velocity:.3f} and location: {location:.3f}")
        print("-"*20)
        print("Simulation has completed! ")

    except ValueError:
        print("Please enter valid values!")

motion_calculator()