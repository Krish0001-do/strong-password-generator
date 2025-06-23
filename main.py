import random
import string
import pyperclip
import re

def generate_password(length=12, use_upper=True, use_digits=True, use_symbols=True):
    lower = string.ascii_lowercase
    upper = string.ascii_uppercase if use_upper else ''
    digits = string.digits if use_digits else ''
    symbols = string.punctuation if use_symbols else ''
    all_chars = lower + upper + digits + symbols
    return ''.join(random.choice(all_chars) for _ in range(length))

def check_strength(password):
    score = 0
    if len(password) >= 8: score += 1
    if re.search(r"[A-Z]", password): score += 1
    if re.search(r"[a-z]", password): score += 1
    if re.search(r"\d", password): score += 1
    if re.search(r"[!@#$%^&*(),.?\":{}|<>_\-\\[\]]", password): score += 1

    if score == 5:
        return "🔐 Strong"
    elif 3 <= score < 5:
        return "⚠️ Medium"
    else:
        return "❌ Weak"

def make_stronger(base_pw):
    # Ensure length ≥ 10
    while len(base_pw) < 10:
        base_pw += random.choice(string.ascii_letters + string.digits + "!@#$%^&*")

    # Ensure presence of all char types
    if not re.search(r"[A-Z]", base_pw):
        base_pw += random.choice(string.ascii_uppercase)
    if not re.search(r"[a-z]", base_pw):
        base_pw += random.choice(string.ascii_lowercase)
    if not re.search(r"\d", base_pw):
        base_pw += random.choice(string.digits)
    if not re.search(r"[!@#$%^&*]", base_pw):
        base_pw += random.choice("!@#$%^&*")

    # Shuffle result
    return ''.join(random.sample(base_pw, len(base_pw)))

def generate_suggestions(base_pw, count=3):
    suggestions = []
    for _ in range(count):
        variant = make_stronger(base_pw)
        suggestions.append(variant)
    return suggestions

def main():
    print("🔐 Strong Password Generator")
    try:
        length = int(input("Enter password length (default 12): ") or 12)
        use_upper = input("Include uppercase letters? (y/n): ").lower() == 'y'
        use_digits = input("Include digits? (y/n): ").lower() == 'y'
        use_symbols = input("Include symbols? (y/n): ").lower() == 'y'

        password = generate_password(length, use_upper, use_digits, use_symbols)
        print("\n✅ Your strong password:\n", password)
        pyperclip.copy(password)
        print("📋 Password copied to clipboard!")

        modify = input("\n🔧 Do you want to modify the password? (y/n): ").lower()
        if modify == 'y':
            custom_pw = input("✍️ Enter your modified password: ")
            strength = check_strength(custom_pw)
            print("🔍 Password Strength:", strength)
            pyperclip.copy(custom_pw)
            print("📋 Modified password copied to clipboard!")

            print("\n💡 Generating similar but strong suggestions...")
            suggestions = generate_suggestions(custom_pw)
            for idx, sug in enumerate(suggestions, 1):
                print(f"{idx}. {sug}   ({check_strength(sug)})")

            choice = input("\n📌 Do you want to copy one of these? Enter number (1-3) or press Enter to skip: ")
            if choice in ['1', '2', '3']:
                selected = suggestions[int(choice) - 1]
                pyperclip.copy(selected)
                print(f"✅ Copied: {selected}")
            else:
                print("✅ No suggestion selected. Keeping your modified password.")

    except ValueError as e:
        print("❌ Error:", e)

if __name__ == "__main__":
    main()
