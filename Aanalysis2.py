import mysql.connector
import pandas as pd
import datetime
from decimal import Decimal
import matplotlib.pyplot as plt  # Importing the matplotlib library

# Database connection
try:
    conn = mysql.connector.connect(
        host="localhost",  # Change if using a remote DB
        user="root",
        password="Markovic@22",
        database="world"
    )
    cursor = conn.cursor()
except mysql.connector.Error as err:
    print(f"Error: {err}")
    exit()

# Retrieve billing data
query = "SELECT meter_id, timestamp, consumption, billing FROM ami_data"
cursor.execute(query)
data = cursor.fetchall()

# Convert to DataFrame
columns = ["meter_id", "timestamp", "consumption", "billing"]
df = pd.DataFrame(data, columns=columns)

# Convert timestamp to datetime format
df["timestamp"] = pd.to_datetime(df["timestamp"])

# Ensure numeric columns are properly typed
df["consumption"] = df["consumption"].astype(float)
df["billing"] = df["billing"].astype(float)

# Define billing rate
billing_rate = 4.22  # Le per kWh

# Aggregate consumption per billing cycle (monthly)
df["billing_cycle"] = df["timestamp"].dt.to_period("M")
billing_summary = df.groupby(["meter_id", "billing_cycle"]).agg(
    total_consumption=("consumption", "sum"),
    actual_billing=("billing", "sum")
).reset_index()

# Convert total consumption to float before multiplication
billing_summary["expected_billing"] = billing_summary["total_consumption"].astype(float) * billing_rate

# Identify discrepancies
billing_summary["billing_discrepancy"] = billing_summary["actual_billing"] - billing_summary["expected_billing"]

# Output discrepancies
print("Discrepancies in Billing:")
discrepancies = billing_summary[billing_summary["billing_discrepancy"].abs() > 1.0]  # Adjust threshold as needed
print(discrepancies)

# Visualization of discrepancies
plt.figure(figsize=(10, 6))
plt.bar(discrepancies["meter_id"].astype(str), discrepancies["billing_discrepancy"], color='blue')
plt.xlabel('Meter ID')
plt.ylabel('Billing Discrepancy')
plt.title('Billing Discrepancies by Meter ID')
plt.axhline(0, color='red', linewidth=0.8, linestyle='--')  # Line at y=0 for reference
plt.xticks(rotation=45)
plt.tight_layout()  # Adjust layout to prevent clipping
plt.show()  # Display the plot

# Save results to CSV
billing_summary.to_csv("billing_analysis.csv", index=False)

# Close database connection
cursor.close()
conn.close()