import os
import json
import getpass
import string
import secrets
from cryptography.fernet import Fernet

MASTER_P = "SOLA081803"
vault_file = "vault.json"

key = b'4RygnXVBOxOU0r6Z2ieqrPR8mW23QZK8dgcJv8VXbOQ='
fernet = Fernet(key)



def encrypt(text):
    return fernet.encrypt(text.encode()).decode()



def decrypt(text):
    return fernet.decrypt(text.encode()).decode()
    

if os.path.exists(vault_file) and os.path.getsize(vault_file) > 0:
    with open(vault_file, 'r') as f:
        encrypted_passwords = json.load(f)
        passwords = {site: decrypt(pwd) for site, pwd in encrypted_passwords.items()}
else:
    passwords = {}



def save_vault():
    with open(vault_file, 'w') as f:
        encrypted_passwords = {site: encrypt(pwd) for site, pwd in passwords.items()}
        json.dump(encrypted_passwords, f)

def generate_password(length = 12):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(secrets.choice(characters) for _ in range(length))
    return password

def add_password():
    site = input("Site Name: ")

    choice = input("Do you want to generate a random secure password? (y/n): ").lower()
    if choice == "y":
        length_inp = input("Enter the desired length(default is 12): ")
        length = int(length_inp) if length_inp.isdigit() else 12
        pwd = generate_password(length)
        print(f"Generated Password: {pwd}")
    else:
        pwd = getpass.getpass("Password: ")
        
        
    passwords[site] = pwd
    save_vault()
    print("Password Saved")



def view_pwd(st):
    if not passwords:
        print("Vault is empty")
        return
    elif st == "all":
        for site, passwrd in passwords.items():
            print(f"{site}: {passwrd}")
    elif st not in passwords:
        print("Site not found.")
    else:
        print(f"{st}: {passwords[st]}")
    



def delete_pwd():
    site = input("Site to delete: ")
    if site in passwords:
        del passwords[site]
        save_vault()
        print("Password deleted")
    else:
        print("Site not found")



def main():
    entered = getpass.getpass("Enter Master Password: ")
    if entered != MASTER_P:
        print("Access denied.")
        return
    
    print("Welcome to your password vault!")

    while True:
        print("\n\tMenu")
        print("1. Add password")
        print("2. Delete password")
        print("3. View Password")
        print("4.Exit")
        
        choice  = input("\nChoose and Option: ")

        if choice == "1":
            add_password()
        elif choice == "2":
            delete_pwd()
        elif choice == "3":
            s = input("Enter site (or type 'all'): ")
            view_pwd(s)
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid Choice.")

if __name__ == "__main__":
    main()