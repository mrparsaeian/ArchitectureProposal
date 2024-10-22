import configparser
import os
import sys
import getpass
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet
import base64
import hashlib
from cryptography.hazmat.primitives import hashes

# Generate key from passphrase using PBKDF2
def generate_key_from_passphrase(passphrase):
    salt = b'\x89\xbc\xad\x12\x8b\x16\xec\x93\x19\xb2\x83\xbc\xba\xf8\x14\xd8'
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),  # Fixed the algorithm usage
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(passphrase.encode()))
    return key

# Encrypt the .passwords file
def encrypt_passwords(file_path, fernet):
    config = configparser.ConfigParser()
    config.read(file_path)

    # Encrypt each password in the file
    for section in config.sections():
        for key in config[section]:
            plain_text = config[section][key]
            encrypted_text = fernet.encrypt(plain_text.encode()).decode()
            config[section][key] = encrypted_text

    # Write the encrypted passwords back to the file
    with open(f"{file_path}_encrypted", "w") as configfile:
        config.write(configfile)

# Decrypt the .passwords file and optionally print a specific password
def decrypt_passwords(file_path, fernet, specific_password=None):
    config = configparser.ConfigParser()
    config.read(file_path)

    # Decrypt each password and print it or return a specific password
    for section in config.sections():
        for key in config[section]:
            encrypted_text = config[section][key]
            print(encrypted_text)
            decrypted_text = fernet.decrypt(encrypted_text.encode()).decode()
            
            if specific_password and key == specific_password:
                print(f"{section} - {key}: {decrypted_text}")
                return

            if not specific_password:
                print(f"{section} - {key}: {decrypted_text}")
# Decrypt and save passwords to a file (part of password_encrypt_decrypt.py)
def decrypt_and_save_passwords(file_path, fernet, specific_password=None, output_file=".passwords_decrypted"):
    config = configparser.ConfigParser()
    config.read(file_path)

    with open(output_file, "w") as output:
        for section in config.sections():
            for key in config[section]:
                encrypted_text = config[section][key]
                decrypted_text = fernet.decrypt(encrypted_text.encode()).decode()
                output.write(f"{key}={decrypted_text}\n")
# Main functionality
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python password_encrypt_decrypt.py <encrypt|decrypt> <file_path> [specific_password]")
        sys.exit(1)

    action = sys.argv[1]
    file_path = sys.argv[2]
    specific_password = sys.argv[3] if len(sys.argv) > 3 else None

    # Prompt for a passphrase
    passphrase = getpass.getpass(prompt="Enter passphrase for encryption/decryption: ")

    # Generate key from the passphrase
    key = generate_key_from_passphrase(passphrase)
    fernet = Fernet(key)

    if action == "encrypt":
        encrypt_passwords(file_path, fernet)
        print("Passwords encrypted and saved.")
    elif action == "decrypt":
        decrypt_passwords(file_path, fernet, specific_password)
    else:
        print("Invalid action. Use 'encrypt' or 'decrypt'.")
        sys.exit(1)
