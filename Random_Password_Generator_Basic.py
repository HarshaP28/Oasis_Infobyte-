
import random
import string

def generate_password(length=12, use_upper=True, use_lower=True,
                       use_digits=True, use_symbols=True):
    characters = ""
    if use_upper:   characters += string.ascii_uppercase
    if use_lower:   characters += string.ascii_lowercase
    if use_digits:  characters += string.digits
    if use_symbols: characters += string.punctuation

    if not characters:
        return "Please select at least one character type!"

    password = ''.join(random.choice(characters) for _ in range(length))
    return password

def check_strength(password):
    score = 0
    if any(c.isupper() for c in password):   score += 1
    if any(c.islower() for c in password):   score += 1
    if any(c.isdigit() for c in password):   score += 1
    if any(c in string.punctuation for c in password): score += 1
    if len(password) >= 12: score += 1
    if len(password) >= 16: score += 1

    if score <= 2:   return "Weak 🔴"
    elif score <= 4: return "Medium 🟡"
    else:            return "Strong 🟢"

def main():
    print("=" * 45)
    print("  🔐 Basic Password Generator")
    print("=" * 45)

    while True:
        print("\nOptions:")
        print("  1. Generate Password")
        print("  2. Exit")
        print("-" * 45)

        choice = input("Enter choice (1/2): ").strip()

        if choice == "1":
            try:
                length = int(input("Password length (default 12): ").strip() or "12")
                if length < 4 or length > 64:
                    print("Length must be between 4 and 64!")
                    continue
            except ValueError:
                print("Please enter a valid number!")
                continue

            upper   = input("Include UPPERCASE? (y/n, default y): ").strip().lower() != "n"
            lower   = input("Include lowercase? (y/n, default y): ").strip().lower() != "n"
            digits  = input("Include numbers?   (y/n, default y): ").strip().lower() != "n"
            symbols = input("Include symbols?   (y/n, default y): ").strip().lower() != "n"

            print("\n" + "-" * 45)
            print("  Generated Passwords:")
            print("-" * 45)

            for i in range(5):
                pwd = generate_password(length, upper, lower, digits, symbols)
                strength = check_strength(pwd)
                print(f"  {i+1}. {pwd}  [{strength}]")

            print("-" * 45)

        elif choice == "2":
            print("\n✅ Goodbye!")
            break
        else:
            print("Invalid choice! Enter 1 or 2.")

if __name__ == "__main__":
    main()