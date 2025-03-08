import mysql.connector
import os
import csv

# Database connection details
db_config = {
    "host": "localhost",      # Change if needed
    "user": "root",           # Change to your MySQL username
    "password": "Markovic@22",
    "database": "world"
}

# Folder path
folder_path = r"C:\Users\user\Desktop\Dr. Maurice"

# Table name to export
table_name = "ami_data"  # Replace with actual table name

# Output file path
csv_file = os.path.join(folder_path, f"ami_data.csv")

try:
    # Establish connection
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Fetch column names
    cursor.execute(f"SELECT * FROM ami_data LIMIT 1")
    columns = [col[0] for col in cursor.description]

    # Open CSV file and write in chunks
    with open(csv_file, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        
        # Write header row
        writer.writerow(columns)

        # Fetch data in chunks (avoid memory overload)
        cursor.execute(f"SELECT * FROM ami_data")
        while True:
            rows = cursor.fetchmany(1000)  # Fetch 1000 rows at a time
            if not rows:
                break  # Stop when no more data

            # Write rows to CSV
            writer.writerows(rows)

    print(f"Table 'ami_data' exported successfully to ami_data.csv")

except mysql.connector.Error as e:
    print(f"Error: {e}")

finally:
    if cursor:
        cursor.close()  # Close the cursor
    if conn:
        conn.close()  # Close the connection