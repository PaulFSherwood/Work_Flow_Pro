import mysql.connector
import bcrypt
import getpass

def execute_query(query, params=None):
    # Connection to the flight sim database
    db = mysql.connector.connect(
        host='localhost',
        user='sherwood',
        password='sherwood',
        database='flight_simulator_db'
    )
    # Create the cursor for the look in the db
    cursor = db.cursor()
    # Execute the query passed in by the user / function
    if params is not None:
        cursor.execute(query, params)
    else:
        cursor.execute(query)
    # save the result
    result = cursor.fetchall()
    # close the connection
    cursor.close()
    db.close()
    return result[0]


def get_user_password(username):
    query = "SELECT password FROM users WHERE username = %s"
    result = execute_query(query, (username,))
    # cursor.execute(query, (username,))
    # result = cursor.fetchone()
    if result:
        print(f"Result: {result[0]}")
        return result[0]
    else:
        return None

def verify_password(username):
    stored_password = get_user_password(username).encode("utf-8")  # string must be in byte format
    print(f"Stored password: {stored_password}")
    if stored_password:
        entered_password = getpass.getpass("Enter your password: ").encode("utf-8")  # string must be in byte format
        
        return bcrypt.checkpw(entered_password, stored_password), stored_password
    else:
        return False
    
username = input("Enter a username: ")
hash_pw = verify_password(username)[1]

print(f"User: {username}")
print(f"Hashed password: {hash_pw}")

# create a new connection to the database using the username and password
db = mysql.connector.connect(
    host='localhost',
    user=username,
    password=hash_pw.decode("utf-8"),
    database='flight_simulator_db'
)
# create a cursor to execute queries
cursor = db.cursor()

# query: SELECT model FROM flight_simulator_db.simulators;

# execute the query
cursor.execute("SELECT model FROM flight_simulator_db.simulators;")
# save the result
result = cursor.fetchall()
# print the result
print(result)
# close the connection
cursor.close()
db.close()
