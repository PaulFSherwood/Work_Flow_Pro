import json
import bcrypt
from cryptography.fernet import Fernet
import re
import mysql.connector

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

class Validator:
    @staticmethod
    def validate_email(email):
        match = re.compile(r"^[-\w\.]+@([\w-]+\.)+[\w-]{2,4}$")
        return bool(match.fullmatch(str(email).lower()))

    @staticmethod
    def validate_password(password):
        sql_keywords = ['select', 'drop', ';', '--', 'insert', 'delete', 'update', 'union', 'create', 'alter']
        return not any(keyword in password.lower() for keyword in sql_keywords)
