import secrets
def generate_password(x):
    # Define the character sets to use in the password
    lowercase = 'abcdefghijklmnopqrstuvwxyz'
    uppercase = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    digits = '0123456789'
    special_characters = '!@#$%^&*()-_=+,.<>?'
    if x< 4:
        raise ValueError("Password length must be at least 4 characters.")

    password = [
secrets.choice(lowercase), 
secrets.choice(uppercase), 
secrets.choice(digits), 
secrets.choice(special_characters)
    ]



    # Combine all character sets
    all_characters = lowercase + uppercase + digits + special_characters

    # Generate a secure random password of length x
    password_length = x-4
    password += [secrets.choice(all_characters) for _ in range(password_length)]
    secrets.SystemRandom().shuffle(password)
    password = ''.join(password)

    return password
if __name__ == "__main__":
    try:
        length = int(input("Enter the desired length of the password (minimum 4): "))
        password = generate_password(length)
        print(f"Generated password: {password}")
    except ValueError as e:
        print(e)