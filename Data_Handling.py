import pandas as pd
import mysql.connector
from mysql.connector import Error
from sklearn.preprocessing import MinMaxScaler
from scipy import stats
import numpy as np
from sklearn.model_selection import train_test_split
import datetime
import json
from sklearn.impute import SimpleImputer

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

# Handling missing values
print("Handling Missing Values...")
df.fillna(df.mean(), inplace=True)  # Fill numerical missing values with mean
df.fillna(df.mode().iloc[0], inplace=True)  # Fill categorical missing values with mode
print("Dataset after handling missing values:")
print(df.head())
print("\n")