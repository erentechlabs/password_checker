import requests
import hashlib
import sys
import getpass

def check_hibp_api(password_hash_prefix, hash_to_check):
    url = f'https://api.pwnedpasswords.com/range/{password_hash_prefix}'
    try:
        res = requests.get(url)
        if res.status_code != 200:
            print(f"[-] Error fetching data from API: Status code {res.status_code}")
            return 0
    except requests.exceptions.RequestException as e:
        print(f"[-] An error occurred during the request: {e}")
        return 0


    hashes = (line.split(':') for line in res.text.splitlines())
    for h, count in hashes:
        if h == hash_to_check:
            return int(count)
    return 0

def analyze_password_strength(password):

    strength = 0
    feedback = []


    if len(password) >= 12:
        strength += 1
    elif len(password) >= 8:
        pass
    else:
        feedback.append("Password is too short. Aim for at least 12 characters.")


    if any(char.isupper() for char in password):
        strength += 1
    else:
        feedback.append("Add at least one uppercase letter.")

    if any(char.islower() for char in password):
        strength += 1
    else:
        feedback.append("Add at least one lowercase letter.")

    if any(char.isdigit() for char in password):
        strength += 1
    else:
        feedback.append("Add at least one number.")

    special_characters = "!@#$%^&*()-+?_=,<>/"
    if any(char in special_characters for char in password):
        strength += 1
    else:
        feedback.append(f"Add at least one special character (e.g., {special_characters}).")

    if strength <= 2:
        level = "Very Weak"
    elif strength == 3:
        level = "Weak"
    elif strength == 4:
        level = "Moderate"
    else:
        level = "Strong"

    return level, feedback

def main():
    try:
        password = getpass.getpass("Enter the password to check (it will not be displayed): ")
        if not password:
            print("Password cannot be empty.")
            return

        print("\n--- Password Strength Analysis ---")
        strength_level, feedback_list = analyze_password_strength(password)
        print(f"Strength Level: {strength_level}")
        if feedback_list:
            print("Suggestions for improvement:")
            for item in feedback_list:
                print(f"- {item}")

        print("\n--- Breach Check (using HaveIBeenPwned) ---")
        sha1_password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
        prefix, suffix = sha1_password[:5], sha1_password[5:]

        count = check_hibp_api(prefix, suffix)

        if count > 0:
            print(f"\n[!] WARNING: This password has been found in a data breach {count} times.")
            print("You should change this password immediately wherever you have used it.")
        else:
            print("\n[+] GOOD NEWS: This password was not found in any of the data breaches checked by HaveIBeenPwned.")
            print("However, ensure it is still strong and unique to each service.")

    except KeyboardInterrupt:
        print("\nProcess interrupted by user. Exiting.")
        sys.exit(0)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == '__main__':
    main()