import mysql.connector
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE

# Database connection
try:
    conn = mysql.connector.connect(
        host="localhost",  # Change this if using a remote server
        user="root",
        password="Markovic@22",
        database="world"
    )
    cursor = conn.cursor()
except mysql.connector.Error as err:
    print(f"Error: {err}")
    exit()

# Retrieve consumption data
query = "SELECT meter_id, timestamp, consumption FROM ami_data"
cursor.execute(query)
data = cursor.fetchall()

# Convert to DataFrame
columns = ["meter_id", "timestamp", "consumption"]
df = pd.DataFrame(data, columns=columns)

# Convert timestamp to datetime format
df["timestamp"] = pd.to_datetime(df["timestamp"])

# Aggregate consumption per customer per month
df["billing_cycle"] = df["timestamp"].dt.to_period("M")
consumption_summary = df.groupby(["meter_id", "billing_cycle"]).agg(
    total_consumption=("consumption", "sum")
).reset_index()

# Pivot data to wide format (each row = one meter_id, columns = months)
pivot_df = consumption_summary.pivot(index="meter_id", columns="billing_cycle", values="total_consumption").fillna(0)

# Feature engineering: Average daily consumption
df['date'] = df['timestamp'].dt.date
average_daily_consumption = df.groupby(['meter_id', 'date']).agg(
    avg_consumption=('consumption', 'mean')
).reset_index()

# Merge average daily consumption back to the main DataFrame
df = df.merge(average_daily_consumption, on=['meter_id', 'date'], how='left')

# Feature engineering: Peak usage hours
df['hour'] = df['timestamp'].dt.hour
peak_usage_hours = df.groupby(['meter_id', 'hour']).agg(
    peak_usage=('consumption', 'sum')
).reset_index()

# Standardize data
scaler = StandardScaler()

# Standardize data including new features
# Update the features list to match the columns in pivot_df
features = pivot_df.columns.tolist()  # Use all columns in pivot_df for scaling
scaled_data = scaler.fit_transform(pivot_df[features])

# Dimensionality reduction using PCA
pca = PCA(n_components=2)
pca_result = pca.fit_transform(scaled_data)

# Dimensionality reduction using t-SNE
tsne = TSNE(n_components=2, random_state=42)
tsne_result = tsne.fit_transform(scaled_data)

# Determine optimal clusters using Elbow Method
wcss = []
for i in range(1, 11):
    kmeans = KMeans(n_clusters=i, random_state=42, n_init=10)
    kmeans.fit(scaled_data)
    wcss.append(kmeans.inertia_)

# Plot Elbow Curve
plt.figure(figsize=(8, 5))
plt.plot(range(1, 11), wcss, marker="o", linestyle="--")
plt.xlabel("Number of Clusters")
plt.ylabel("WCSS (Within-Cluster Sum of Squares)")
plt.title("Elbow Method for Optimal K")
plt.show()

# Choose optimal K (e.g., K=3 based on the elbow curve)
optimal_k = 3
kmeans = KMeans(n_clusters=optimal_k, random_state=42, n_init=10)
clusters = kmeans.fit_predict(scaled_data)

# Assign clusters to the original dataset
pivot_df["Cluster"] = clusters

# Visualize clusters using PCA
plt.figure(figsize=(8, 5))
plt.scatter(pca_result[:, 0], pca_result[:, 1], c=pivot_df["Cluster"], cmap='viridis')
plt.xlabel("PCA Component 1")
plt.ylabel("PCA Component 2")
plt.title("Customer Clusters (PCA)")
plt.colorbar(label='Cluster')
plt.show()

# Visualize clusters using t-SNE
plt.figure(figsize=(8, 5))
plt.scatter(tsne_result[:, 0], tsne_result[:, 1], c=pivot_df["Cluster"], cmap='viridis')
plt.xlabel("t-SNE Component 1")
plt.ylabel("t-SNE Component 2")
plt.title("Customer Clusters (t-SNE)")
plt.colorbar(label='Cluster')
plt.show()

# Save cluster assignments
pivot_df.to_csv("consumption_clusters.csv")

# Close database connection
cursor.close()
conn.close()
