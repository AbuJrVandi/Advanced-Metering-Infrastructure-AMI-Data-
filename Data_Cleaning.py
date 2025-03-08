import pandas as pd
import mysql.connector
from mysql.connector import Error

def load_data_from_mysql(query, db_config):
    try:
        connection = mysql.connector.connect(**db_config)
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute(query)
            result = cursor.fetchall()
            columns = cursor.column_names
            df = pd.DataFrame(result, columns=columns)
            return df
    except Error as e:
        print(f"Error: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Database configuration
db_config = {
    'host': 'localhost',
    'database': 'world',
    'user': 'root',
    'password': 'Markovic@22'
}

# SQL query to fetch data
query = "SELECT * FROM ami_data"

# Load data
df = load_data_from_mysql(query, db_config)

print(df)