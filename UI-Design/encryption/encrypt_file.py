import json
import getpass
from cryptography.fernet import Fernet

# Get user input for Database stuff
host = input("Enter the host: ")
user = input("Enter the user: ")
password = getpass.getpass("Enter the password: ")
database = input("Enter the database: ")

# Configuration data
config = {
    'host': host,
    'user': user,
    'password': password,
    'database': database
}

# Serialize the configuration data to JSON
config_json = json.dumps(config).encode()

# Generate a random encryption key
encryption_key = Fernet.generate_key()

# Create a Fernet cipher using the encryption key
fernet = Fernet(encryption_key)

# Encrypt the configuration data
encrypted_data = fernet.encrypt(config_json)

# Save the encrypted data to a file
with open('config.encrypted', 'wb') as file:
    file.write(encrypted_data)

# Save the encryption key to a separate file
with open('encryption.key', 'wb') as file:
    file.write(encryption_key)
