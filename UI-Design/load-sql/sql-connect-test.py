import mysql.connector

# Prompt the user to enter the username and password
username = input("Enter the database username: ")
password = input("Enter the database password: ")

# Connect to the MySQL database
db = mysql.connector.connect(
    host="localhost",
    user=username,
    password=password,
    database="flight_simulator_db"
)

# Create a cursor to interact with the database
cursor = db.cursor()

# Specify the table to retrieve data from
table_name = "WorkOrders"

try:
    # Execute the SELECT query to retrieve all rows from the table
    print("trying SELECT * FROM {table_name}")
    query = f"SELECT * FROM {table_name}"
    cursor.execute(query)

    # Fetch all rows and print the data
    rows = cursor.fetchall()
    for row in rows:
        print(row)

except mysql.connector.Error as error:
    print(f"Error retrieving data from the database: {error}")

# Close the database connection
db.close()
