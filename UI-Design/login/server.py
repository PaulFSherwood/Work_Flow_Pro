import mysql.connector
import bcrypt
import socket
import threading
import json
import datetime
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

# Use the encrypted key to decrypt the configuration file
config = json.loads(decrypted_data)

# Retrieve the database credentials from the config
db_host = config['host']
db_user = config['user']
db_password = config['password']
db_database = config['database']

# Database connection using the decrypted credentials
db = mysql.connector.connect(
    host=db_host,
    user=db_user,
    password=db_password,
    database=db_database
)

# Default server connect stuff
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 9999))
server.listen()

# Function: handle_connection
# Description: This function handles the connection to the server.
#              Get username and password
#              Authenticate the user.
#              Start thread if good to go
# Parameters: client_socket - The socket object for the client
# Returns: None
def handle_connection(client_socket):

    # Get the username and password from the client
    client_socket.send("Username: ".encode())
    username = client_socket.recv(1024).decode()
    client_socket.send("Password: ".encode())
    encrypted_password = client_socket.recv(1024)

    # Decrypt the password Fernet is a symmetric encryption algorithm
    password = fernet.decrypt(encrypted_password).decode()

    cursor = db.cursor()
    # retrieve the hashed password from the database
    cursor.execute("SELECT password FROM users WHERE username = %s", (username,))
    # Get the first element of the tuple
    stored_hashed_password = cursor.fetchone()[0]

    # print(f"Password: {password} || Hashed password: {stored_hashed_password}")

    # Now we use bcrypt to compare the plain password with the hashed version stored in the database
    if stored_hashed_password and bcrypt.checkpw(password.encode(), stored_hashed_password.encode()):
        client_socket.send("Login successful".encode())
        # create a session token for the client based on the username and the date
        token = bcrypt.hashpw((username + str(datetime.datetime.now())).encode(), bcrypt.gensalt())
        # store the session token in the database for the user
        cursor.execute("UPDATE users SET token = %s WHERE username = %s", (token, username))
        db.commit()
        # send the token to the client
        client_socket.send(token)
        print("Token sent to client")



        # Start a thread to handle client queries
        threading.Thread(target=client_queries, args=(client_socket,)).start()
    else:
        client_socket.send("Login failed".encode())
        client_socket.close()

def client_queries(client_socket):
    while True:
        query = client_socket.recv(1024).decode().strip()
        # print(f"Query: {query}")
        if query == "exit":
            client_socket.close()
            break
        elif query:
            cursor = db.cursor()
            cursor.execute(query)
            if cursor.with_rows:  # Check if the statement returns rows
                result = cursor.fetchall()
                # print(f"Result: {result}")
                client_socket.send(str(result).encode())
            else:  # Non-SELECT queries like INSERT, UPDATE, DELETE
                affected_rows = cursor.rowcount
                # print(f"Affected rows: {affected_rows}")
                client_socket.send(f"Query executed. Affected rows: {affected_rows}".encode())
        else:  # Query is an empty string
            pass
            # print("Empty query received.")
            # client_socket.send("Empty query received. Please enter a valid SQL query.".encode())


while True:
    client_socket, address = server.accept()
    threading.Thread(target=handle_connection, args=(client_socket,)).start()
