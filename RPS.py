import random
choices = ['rock', 'paper', 'scissors']
def RPS():

    while True:
        computer_choice = random.choice(choices)
        user_choice = input("Enter your choice (rock, paper, scissors): ").lower()
        if user_choice == 'exit' or user_choice == 'quit':
            print("Thanks for playing!")
            break
        while user_choice not in choices:
            print("Invalid choice. Please try again.")
            user_choice = input("Enter your choice (rock, paper, scissors): ").lower()

        print(f"Computer chose: {computer_choice}")
        print(f"You chose: {user_choice}")
        if user_choice == computer_choice:
            print("It's a tie!")
        elif (user_choice == 'rock' and computer_choice == 'scissors') or \
            (user_choice == 'paper' and computer_choice == 'rock') or \
            (user_choice == 'scissors' and computer_choice == 'paper'):    
            print("You win!")
        else:
            print("Computer wins!")    

if __name__ == "__main__":
    RPS()