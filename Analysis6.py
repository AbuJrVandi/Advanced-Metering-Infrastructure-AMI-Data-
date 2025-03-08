import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime as dt

# MySQL Database Connection
conn = mysql.connector.connect(
    host="localhost",       # Change this for a remote database
    user="root",
    password="Markovic@22",
    database="world"
)

# Query to fetch data
query = "SELECT timestamp, consumption FROM ami_data"
df = pd.read_sql(query, conn)
conn.close()

# Convert timestamp column to datetime
df['timestamp'] = pd.to_datetime(df['timestamp'], format="%d/%m/%Y %H:%M")

# Extract day of the week (0 = Monday, 6 = Sunday)
df['day_of_week'] = df['timestamp'].dt.dayofweek
df['is_weekend'] = df['day_of_week'].apply(lambda x: "Weekend" if x >= 5 else "Weekday")

# Group by weekday/weekend and calculate mean consumption
weekday_vs_weekend = df.groupby('is_weekend')['consumption'].mean().reset_index()

# Plot the difference in consumption
plt.figure(figsize=(8, 5))
sns.barplot(x="is_weekend", y="consumption", data=weekday_vs_weekend, palette="coolwarm")
plt.xlabel("Day Type")
plt.ylabel("Average Consumption")
plt.title("Weekday vs Weekend Energy Consumption")
plt.grid()
plt.show()

# Hourly consumption trends for weekdays vs weekends
plt.figure(figsize=(10, 5))
sns.lineplot(x=df[df["is_weekend"] == "Weekday"].groupby(df['timestamp'].dt.hour)['consumption'].mean().index,
             y=df[df["is_weekend"] == "Weekday"].groupby(df['timestamp'].dt.hour)['consumption'].mean().values,
             label="Weekday", color="blue")

sns.lineplot(x=df[df["is_weekend"] == "Weekend"].groupby(df['timestamp'].dt.hour)['consumption'].mean().index,
             y=df[df["is_weekend"] == "Weekend"].groupby(df['timestamp'].dt.hour)['consumption'].mean().values,
             label="Weekend", color="red")

plt.xlabel("Hour of Day")
plt.ylabel("Average Consumption")
plt.title("Hourly Consumption Trend: Weekday vs Weekend")
plt.legend()
plt.grid()
plt.show()