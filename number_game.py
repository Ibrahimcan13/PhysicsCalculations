import random
print("Number  Guessing Game ")

def game_play():
    secret_number = random.randint(1,100)
    attempts = 0

    print("Guess a number between 1 and 100: ")

    while True:
        guess = int(input("Your guess: "))
        attempts += 1
        if guess < secret_number:
            print("Your guess is too low. Please try higher one:")
        elif guess > secret_number:
            print("Your guess is too high. Please try lower one:")
        else:
            print(f"You guessed the number correctly in {attempts} attempts, Congratulations! ")
            break

game_play()