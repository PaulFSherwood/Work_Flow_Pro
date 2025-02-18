import mysql.connector
# import os
import sys
import json
import getpass
import bcrypt
from cryptography.fernet import Fernet

# Pull in the encrypted file containing the database credentials
with open('config.encrypted', 'rb') as cFile:
    encrypted_data = cFile.read()

# Pull in the encryption key
with open('encryption.key', 'rb') as eFile:
    encryption_key = eFile.read()

# Create cipher and decrypt data
fernet = Fernet(encryption_key)
decrypted_data = fernet.decrypt(encrypted_data)

# Use the decrypted key to decrypt the configuration file
config = json.loads(decrypted_data)

# Retrieve the database credentials from the config
db_host = config['host']
db_user = config['user']
db_password = config['password']
db_database = config['database']

# Database connection using the decrypted credentials
def authenticate(username, password):
    # Connect to the database
    db_connection = mysql.connector.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        database=db_database
    )

    # Execute a query to retrieve the stored hashed password for the given username
    cursor = db_connection.cursor()
    query = "SELECT password FROM users WHERE username = %s"
    cursor.execute(query, (username,))
    result = cursor.fetchone()
    stored_hashed_password = result[0] if result else None

    # Close the database connection and cursor
    cursor.close()
    db_connection.close()

    # Compare the entered password with the stored hashed password
    if stored_hashed_password and bcrypt.checkpw(password.encode(), stored_hashed_password.encode()):
        return True
    else:
        return False

# Function to get the role of the user from the database
def get_user_role(username):
    # Connect to the database
    db_connection = mysql.connector.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        database=db_database
    )

    # Execute a query to retrieve the role of the user based on the username
    cursor = db_connection.cursor()
    query = "SELECT role FROM users WHERE username = %s"
    cursor.execute(query, (username,))
    result = cursor.fetchone()
    role = result[0] if result else None

    # Close the database connection and cursor
    cursor.close()
    db_connection.close()

    return role

# Get the username from the user
username = input("Enter your username: ")

# Get the password securely using getpass.getpass()
password = getpass.getpass("Enter your password: ")

print(f"Username: {username} || Password: {password}")

# Authenticate the user
if authenticate(username, password):
    # Execute the appropriate script based on the user's role
    role = get_user_role(username)

    # Execute the appropriate script based on the user's role
    if role == 'MANAGER':
        # os.system("python admin_script.py")
        print("MANAGER")
    elif role == 'MAINTENANCE':
        # os.system("python manager_script.py")
        print("MAINTENANCE")
    elif role == 'LOGISTICS':
        # os.system("python maintenance_script.py")
        print("LOGISTICS")
    else:
        print("Invalid username or password.")
        sys.exit(1)
