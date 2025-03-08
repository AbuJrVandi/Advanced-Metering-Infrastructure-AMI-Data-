import random
from datetime import datetime, timedelta
import mysql.connector
import time  # Add time module for delays

# MySQL connection setup
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "Markovic@22",  
    "database": "world"       
}
conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()

# Create the table if it doesn't exist
def create_table():
    create_table_query = """
    CREATE TABLE IF NOT EXISTS ami_data (
        meter_id BIGINT NOT NULL,
        timestamp DATETIME NOT NULL,
        location VARCHAR(50) NOT NULL,
        season VARCHAR(20) NOT NULL,
        meter_type VARCHAR(20) NOT NULL,
        consumption DECIMAL(10, 2) NOT NULL,
        billing DECIMAL(10, 2) NOT NULL,
        is_downtime INT(1) NOT NULL,
        PRIMARY KEY (meter_id, timestamp)
    );
    """
    cursor.execute(create_table_query)
    conn.commit()  # Commit the table creation
    print("Table 'ami_data' is ready!")

# Helper functions
def get_season(month):
    return "Dry" if month in [11, 12, 1, 2, 3, 4] else "Rain"

def generate_meter_profile():
    return {
        "Residential": {"base": 0.5, "growth": 0.05, "noise": 0.1},
        "Commercial": {"base": 2.0, "growth": 0.2, "noise": 0.3},
        "Industrial": {"base": 5.0, "growth": 0.5, "noise": 0.5},
    }

def generate_consumption(base, growth, noise, hour):
    hourly_factor = 1.5 if 18 <= hour <= 22 else 1.0
    return round((base + growth * hour + random.uniform(-noise, noise)) * hourly_factor, 2)

def generate_downtime():
    # 1% chance of downtime (1), 99% chance of no downtime (0)
    return 1 if random.random() < 0.01 else 0

BASE_METER_ID = 38517635

# Data generation and insertion
def generate_and_insert_data():
    start_date = datetime(2023, 1, 1, 0, 0)
    end_date = datetime(2025, 12, 31, 23, 0)
    profiles = generate_meter_profile()
    rate_per_kwh = 4.22
    batch_size = 10000  # Reduced batch size
    data_batch = []

    meter_count = 1000
    locations = ["West", "East", "North", "South"]
    location_weights = [0.4, 0.2, 0.2, 0.2]
    meter_types = ["Residential", "Commercial", "Industrial"]
    meter_type_weights = [0.6, 0.25, 0.15]

    current_time = start_date
    total_records = 0

    while total_records < 1000000:  # Stop after 1 million records
        for i in range(meter_count):
            meter_id = BASE_METER_ID + i
            random_minutes = random.randint(0, 59)
            random_seconds = random.randint(0, 59)
            timestamp = current_time.replace(minute=random_minutes, second=random_seconds)
            location = random.choices(locations, location_weights)[0]
            meter_type = random.choices(meter_types, meter_type_weights)[0]
            season = get_season(timestamp.month)
            profile = profiles[meter_type]

            consumption = generate_consumption(profile["base"], profile["growth"], profile["noise"], timestamp.hour)
            is_downtime = generate_downtime()  # Generate 1 or 0 randomly
            if is_downtime == 1:
                consumption = 0.0  # Set consumption to 0 during downtime

            billing = round(consumption * rate_per_kwh, 2)

            data_batch.append((
                meter_id, timestamp, location, season, meter_type, consumption, billing, is_downtime
            ))

            if len(data_batch) >= batch_size:
                insert_query = """
                    INSERT INTO ami_data 
                    (meter_id, timestamp, location, season, meter_type, consumption, billing, is_downtime)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.executemany(insert_query, data_batch)
                conn.commit()  # Commit the batch insert
                total_records += len(data_batch)
                print(f"{len(data_batch)} records inserted successfully. Total records: {total_records}")
                data_batch = []
                time.sleep(1)  # Add a delay between batches

        current_time += timedelta(hours=1)

    if data_batch:
        insert_query = """
            INSERT INTO ami_data 
            (meter_id, timestamp, location, season, meter_type, consumption, billing, is_downtime)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.executemany(insert_query, data_batch)
        conn.commit()  # Commit the final batch insert
        total_records += len(data_batch)
        print(f"{len(data_batch)} records inserted successfully. Total records: {total_records}")

# Run the table creation and data insertion
create_table()
generate_and_insert_data()

cursor.close()
conn.close()

print("AMI database populated successfully with 1 million records!")