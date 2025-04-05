import mysql.connector

def get_connection():
    """
    Establish a connection to the MySQL database.
    """
    try:
        connection = mysql.connector.connect(
            host="93.127.206.58",
            user="root",
            password="Lealava@123",
            database="Ecommerce"
        )
        print("Database connected!")
        return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to the database: {err}")
        raise

# SECRET_KEY = "126945c1bdc73d55bb3d364aed2611f8"