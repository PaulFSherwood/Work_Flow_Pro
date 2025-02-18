import socket
import getpass
from cryptography.fernet import Fernet

# Pull in the encryption key
with open('encryption.key', 'rb') as eFile:
    encryption_key = eFile.read()

# Create cipher
fernet = Fernet(encryption_key)

# Default server connect stuff - Check if the connection was successful
try:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('localhost', 9999))
except ConnectionRefusedError:
    print("Can not maintain or find a connection to the server. \n \
          Please try again later.\n")
    exit()

# client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# client.connect(('localhost', 9999))

# Wait for the server to request the username
# Get the username from the user
username = input(client.recv(1024).decode())

# Send the username to the server
client.send(username.encode("utf-8"))

# Wait for the server to request the password
# Get the password securely using getpass.getpass()
password = getpass.getpass(client.recv(1024).decode())

# Encrypt the password before sending
encrypted_password = fernet.encrypt(password.encode())

# Send the encrypted password to the server
client.send(encrypted_password)

response = client.recv(1024).decode("utf-8")
print(response)

# If the user is authenticated, start the client queries
if response == "Login successful":
    # query = "SELECT username FROM flight_simulator_db.users;"
    query = "SELECT name FROM flight_simulator_db.parts;"

    client.send(query.encode("utf-8"))
    response = client.recv(1024).decode("utf-8")
    print(f"Response: {response}")

client.send("exit".encode("utf-8"))
client.close()
