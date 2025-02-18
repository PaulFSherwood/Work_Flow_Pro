import mysql.connector
from utilities import decrypt_config

def execute_query(query, params=None):
    # use decrypt_config to get the database credentials
    config = decrypt_config()
    db = mysql.connector.connect(
        host=config['host'],
        user=config['user'],
        password=config['password'],
        database=config['database']
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
    return result

def execute_insert_query(query, params=None):
    # use decrypt_config to get the database credentials
    config = decrypt_config()
    db = mysql.connector.connect(
        host=config['host'],
        user=config['user'],
        password=config['password'],
        database=config['database']
    )
    cursor = db.cursor()
    try:
        if params is not None:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        db.commit()
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))
        db.rollback()
    finally:
        cursor.close()
        db.close()