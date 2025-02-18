import json
import re
from cryptography.fernet import Fernet


# Open and save encrypted_data file
with open('config.encrypted', 'rb') as cFile:
    encrypted_data = cFile.read()

# Open and save encrypted_key file
with open('encryption.key', 'rb') as eFile:
    encryption_key = eFile.read()


def decrypt_config():
    fernet = Fernet(encryption_key)
    decrypted_data = fernet.decrypt(encrypted_data)
    config = json.loads(decrypted_data)
    return config

class Validator:
    @staticmethod
    def validate_username(username):
        # I wanted to add in all special characters but that could limit usernames
        sql_keywords = ['select', 'drop', ';', '--', 'insert', 'delete', 'update', 'union', 'create', 'alter']
        return not any(keyword in username.lower() for keyword in sql_keywords)

    @staticmethod
    def validate_password(password):
        # I wanted to add in all special characters but that could limit passwords
        sql_keywords = ['select', 'drop', ';', '--', 'insert', 'delete', 'update', 'union', 'create', 'alter']
        return not any(keyword in password.lower() for keyword in sql_keywords)
