import mysql.connector
from mysql.connector import Error

def create_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            password=user_password,
            database=db_name,
          
        )
        print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection

def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")

host='flask-app-mysql-server.mysql.database.azure.com',
user='dbadmin',
password='Linga@12#',
database='userdata'


connection = create_connection(host, user, password, database)


create_feedback_table = """
CREATE TABLE IF NOT EXISTS reviews (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    rating INT CHECK (rating >= 0 AND rating <= 5),
    review TEXT NOT NULL
);
"""


create_statistics_table="""
CREATE TABLE IF NOT EXISTS statistics (
  
    date DATE NOT NULL,
    outpatients INT NOT NULL,
    medicine_prescribed INT NOT NULL,
    opticals_prescribed INT NOT NULL,
    surgeries_performed INT NOT NULL,
    free_surgeries_performed INT NOT NULL,
    cataract_male INT NOT NULL,
    cataract_female INT NOT NULL,
    cornea_male INT NOT NULL,
    cornea_female INT NOT NULL,
    retina_male INT NOT NULL,
    retina_female INT NOT NULL,
    orbit_male INT NOT NULL,
    orbit_female INT NOT NULL
);
"""


execute_query(connection, create_statistics_table)


