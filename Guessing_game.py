import random
random_number = random.randint(1, 100)
while (guess := int(input("Guess a number between 1 and 100: "))) != random_number:
    if guess < random_number:
        print("Too low! Try again.")
    elif guess > random_number:
        print("Too high! Try again.")
    else:
        print("Congratulations! You've guessed the correct number.")
        break    
print(f"The correct number was: {random_number}")    