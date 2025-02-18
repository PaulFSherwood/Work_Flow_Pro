import mysql.connector
import bcrypt
from utilities import decrypt_config

def authenticate(username, password):
    config = decrypt_config()
    db = mysql.connector.connect(
        host=config['host'],
        user=config['user'],
        password=config['password'],
        database=config['database']
    )

    # Execute a query to retrieve the stored hashed password for the given username
    cursor = db.cursor()
    query = "SELECT password FROM users WHERE username = %s"
    cursor.execute(query, (username,))
    result = cursor.fetchone()
    stored_hashed_password = result[0] if result else None

    # Close the database connection and cursor
    cursor.close()
    db.close()

    # Compare the entered password with the stored hashed password
    if stored_hashed_password and bcrypt.checkpw(password.encode(), stored_hashed_password.encode()):
        return True
    else:
        return False
    
def get_user_role(username):
    config = decrypt_config()
    db = mysql.connector.connect(
        host=config['host'],
        user=config['user'],
        password=config['password'],
        database=config['database']
    )

    # Execute a query to retrieve the role of the user based on the username
    cursor = db.cursor()
    query = "SELECT role FROM users WHERE username = %s"
    cursor.execute(query, (username,))
    result = cursor.fetchone()
    role = result[0] if result else None

    # Close the database connection and cursor
    cursor.close()
    db.close()

    return role

def get_user_id(username):
    config = decrypt_config()
    db = mysql.connector.connect(
        host=config['host'],
        user=config['user'],
        password=config['password'],
        database=config['database']
    )

    # get user_id based on the username
    cursor = db.cursor()
    query = "SELECT user_id FROM users WHERE username = %s"
    cursor.execute(query, (username,))
    result = cursor.fetchone()
    user_id = result[0] if result else None

    # Close the database connection and cursor
    cursor.close()
    db.close()

    return user_id