import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm

# MySQL Database Connection
conn = mysql.connector.connect(
    host="localhost",       # Change this if connecting to a remote DB
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
df.set_index('timestamp', inplace=True)

# Resample data to daily frequency
daily_consumption = df['consumption'].resample('D').sum()

# Time series decomposition
decomposition = sm.tsa.seasonal_decompose(daily_consumption, model='additive')
decomposition.plot()
plt.suptitle('Time Series Decomposition', fontsize=16)
plt.show()

# Calculate rolling averages and moving standard deviations
rolling_mean = daily_consumption.rolling(window=30).mean()
rolling_std = daily_consumption.rolling(window=30).std()

# Plotting the consumption trends
plt.figure(figsize=(14, 7))
plt.plot(daily_consumption, label='Daily Consumption', color='blue', alpha=0.5)
plt.plot(rolling_mean, label='30-Day Rolling Mean', color='orange')
plt.fill_between(rolling_std.index, rolling_mean - rolling_std, rolling_mean + rolling_std, color='orange', alpha=0.2, label='30-Day Rolling Std Dev')
plt.title('Daily Energy Consumption with Rolling Mean and Std Dev', fontsize=16)
plt.xlabel('Date', fontsize=14)
plt.ylabel('Consumption', fontsize=14)
plt.legend()
plt.grid()
plt.show()

# Extract time-based features for further analysis
df['hour'] = df.index.hour
df['day'] = df.index.date
df['month'] = df.index.month

# Plot hourly consumption trend
plt.figure(figsize=(10, 5))
sns.lineplot(x=df.groupby('hour')['consumption'].mean().index, y=df.groupby('hour')['consumption'].mean().values)
plt.xlabel("Hour of Day")
plt.ylabel("Average Consumption")
plt.title("Hourly Consumption Trend")
plt.grid()
plt.show()

# Plot daily consumption trend
plt.figure(figsize=(12, 6))
sns.lineplot(x=df.groupby('day')['consumption'].sum().index, y=df.groupby('day')['consumption'].sum().values)
plt.xlabel("Day")
plt.ylabel("Total Consumption")
plt.title("Daily Consumption Trend")
plt.xticks(rotation=45)
plt.grid()
plt.show()

# Plot monthly consumption trend
plt.figure(figsize=(8, 5))
sns.barplot(x=df.groupby('month')['consumption'].sum().index, y=df.groupby('month')['consumption'].sum().values, palette="Blues")
plt.xlabel("Month")
plt.ylabel("Total Consumption")
plt.title("Monthly Consumption Trend")
plt.grid()
plt.show()
