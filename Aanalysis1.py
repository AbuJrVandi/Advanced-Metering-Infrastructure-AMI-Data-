import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import mysql.connector
from datetime import datetime

# Connect to MySQL Database
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='Markovic@22',
    database='world'
)
cursor = conn.cursor()

# Query to retrieve data
query = """
SELECT meter_id, timestamp, location, season, meter_type, consumption, billing, is_downtime
FROM ami_data;
"""

# Load data into Pandas DataFrame
df = pd.read_sql(query, conn)
conn.close()

# Convert timestamp to datetime
df['timestamp'] = pd.to_datetime(df['timestamp'], format='%d/%m/%Y %H:%M')

# Detect anomalies based on statistical thresholds
mean_consumption = df['consumption'].mean()
std_consumption = df['consumption'].std()

# Define an anomaly as a value beyond 3 standard deviations
threshold = 3
lower_bound = mean_consumption - threshold * std_consumption
upper_bound = mean_consumption + threshold * std_consumption
df['is_anomaly'] = (df['consumption'] < lower_bound) | (df['consumption'] > upper_bound)



# Print detected anomalies
print("Detected Anomalies:")
print(df[df['is_anomaly']])


# Visualize the data
plt.figure(figsize=(14, 6))

# Plot the consumption values as a blue line
plt.plot(df['timestamp'], df['consumption'], color='blue', linewidth=1.5)

# Overlay anomalies with red line segments
anomalies = df[df['is_anomaly']]
if not anomalies.empty:
    for idx, row in anomalies.iterrows():
        plt.plot([row['timestamp'], row['timestamp']], [0, row['consumption']], 
                 color='red', linewidth=2, zorder=5)

# Add an annotation for clarity
if not anomalies.empty and len(anomalies) > 0:
    # Annotate the first anomaly
    first_anomaly = anomalies.iloc[0]
    plt.annotate('Anomaly', 
                xy=(first_anomaly['timestamp'], first_anomaly['consumption']),
                xytext=(15, 15),
                textcoords='offset points',
                arrowprops=dict(arrowstyle='->', color='black'))

plt.xlabel('Time')
plt.ylabel('Value')
plt.tight_layout()
plt.show()
