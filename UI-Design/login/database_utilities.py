import mysql.connector

class DatabaseUtils:
    @staticmethod
    def execute_query(query, params=None):
        db = mysql.connector.connect(
            host='localhost',
            user='sherwood',
            password='sherwood',
            database='flight_simulator_db'
        )

        cursor = db.cursor()

        if params is not None:
            cursor.execute(query, params)
        else:
            cursor.execute(query)

        result = cursor.fetchall()

        cursor.close()
        db.close()

        return result

    @staticmethod
    def execute_insert_query(query, params=None):
        db = mysql.connector.connect(
            host='localhost',
            user='sherwood',
            password='sherwood',
            database='flight_simulator_db'
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
