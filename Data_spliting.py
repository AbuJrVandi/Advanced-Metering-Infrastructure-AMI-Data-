import pandas as pd
import mysql.connector
from mysql.connector import Error
from sklearn.preprocessing import MinMaxScaler
from scipy import stats
import numpy as np
from sklearn.model_selection import train_test_split
import datetime
import json

# Function to load data from MySQL
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
print("Initial Dataset:")
print(df.head())  # Print the first 5 rows of the dataset
print("\n")

# Data splitting
print("Splitting Data into Training and Testing Sets...")
X = df.drop('is_downtime', axis=1)  # Replace 'is_downtime' with your actual target column
y = df['is_downtime']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print("Training Data (X_train):")
print(X_train.head())
print("Testing Data (X_test):")
print(X_test.head())
print("\n")
