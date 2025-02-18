import mysql.connector
import bcrypt

# Establish a connection to the MySQL database
cnx = mysql.connector.connect(
    host='localhost',
    user='sherwood',
    password='sherwood',
    database='flight_simulator_db'
)
cursor = cnx.cursor()

def get_user_password(username):
    query = "SELECT password FROM users WHERE username = %s"
    cursor.execute(query, (username,))
    result = cursor.fetchone()
    if result:
        print(f"Result: {result[0]}")
        return result[0]
    else:
        return None

def encrypt_password(password):
    # Generate a salt and hash the password
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)
    return hashed_password

def update_password(username, new_password):
    hashed_password = encrypt_password(new_password)
    query = "UPDATE users SET password = %s WHERE username = %s"
    cursor.execute(query, (hashed_password, username))
    print(f"Updated {username}'s password")
    cnx.commit()

            
import getpass
import getpass
import bcrypt

def verify_password(username):
    stored_password = get_user_password(username).encode("utf-8")  # string must be in byte format
    print(f"Stored password: {stored_password}")
    if stored_password:
        entered_password = getpass.getpass("Enter your password: ").encode("utf-8")  # string must be in byte format
        
        return bcrypt.checkpw(entered_password, stored_password)
    else:
        return False


# Fix passwords
# update_password("Anderson", "aaaa")
# update_password("Bailey", "bbbb")
# update_password("Carter", "cccc")
# update_password("Davis", "dddd")
# update_password("Edwards", "eeee")
# update_password("Foster", "ffff")
# update_password("Gray", "gggg")
# update_password("Hughes", "hhhh")
# update_password("Jenkins", "jjjj")
# update_password("King", "kkkk")

# password = b"super secret password"
# print(password)
# password = getpass.getpass("Enter a password: ").encode("utf-8")
# print(password)
username = input("Enter a username: ")

print(verify_password(username))

# Bcrypt Help
# https://stackoverflow.com/questions/40577867/bcrypt-checkpw-returns-typeerror-unicode-objects-must-be-encoded-before-checkin
# https://github.com/pyca/bcrypt/#usage
# # at creation first:
# password = u"seCr3t"
# hashed_password = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())

# # first attempt:
# password = u"seCrEt"
# print(bcrypt.checkpw(password.encode('utf8'), hashed_password))
# # -> False

# # second attempt:
# password = u"seCr3t"
# print(bcrypt.checkpw(password.encode('utf8'), hashed_password))
# # -> True



cursor.close()
cnx.close()
