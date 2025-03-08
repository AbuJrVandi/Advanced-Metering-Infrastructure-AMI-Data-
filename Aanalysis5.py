import mysql.connector
import pandas as pd
import numpy as np
import lightgbm as lgb
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error
from statsmodels.tsa.arima.model import ARIMA

# 🔹 Step 1: Connect to MySQL Database & Retrieve Data
conn = mysql.connector.connect(
    host="localhost",       # Change if using a remote database
    user="root",
    password="Markovic@22",
    database="world"
)

query = "SELECT timestamp, consumption FROM ami_data"
df = pd.read_sql(query, conn)
conn.close()

# 🔹 Step 2: Data Preprocessing
df['timestamp'] = pd.to_datetime(df['timestamp'])
df['hour'] = df['timestamp'].dt.hour
df['day'] = df['timestamp'].dt.day
df['month'] = df['timestamp'].dt.month
df['weekday'] = df['timestamp'].dt.weekday

# 🔹 Step 3: Create Lag Features
num_lags = 3  # Define the number of lag features
for lag in range(1, num_lags + 1):
    df[f'lag_{lag}'] = df['consumption'].shift(lag)

# Drop rows with NaN values created by lagging
df.dropna(inplace=True)

# 🔹 Step 4: Prepare Features & Target Variable
features = ['hour', 'day', 'month', 'weekday'] + [f'lag_{lag}' for lag in range(1, num_lags + 1)]
X = df[features]
y = df['consumption']

# 🔹 Step 5: Split Data into Training & Testing Sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 🔹 Step 6: Scale Features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# 🔹 Step 7: Train LightGBM Model
model = lgb.LGBMRegressor(boosting_type='gbdt', n_estimators=500, learning_rate=0.05)
model.fit(X_train_scaled, y_train)

# 🔹 Step 8: Make Predictions with LightGBM
y_pred_lgb = model.predict(X_test_scaled)

# 🔹 Step 9: Evaluate Model Performance for LightGBM
mae_lgb = mean_absolute_error(y_test, y_pred_lgb)
rmse_lgb = np.sqrt(mean_squared_error(y_test, y_pred_lgb))

print(f"LightGBM Mean Absolute Error (MAE): {mae_lgb:.2f}")
print(f"LightGBM Root Mean Squared Error (RMSE): {rmse_lgb:.2f}")

# 🔹 Step 10: Fit ARIMA Model
# Ensure the DataFrame is indexed by timestamp for ARIMA
df.set_index('timestamp', inplace=True)

# Define a threshold value for filtering
some_value = 1000  # Adjust this value based on your data context

# Filter the dataset to reduce size
filtered_df = df[df['consumption'] < some_value]  # Adjust condition as needed

# Use a smaller sample for ARIMA if necessary
sample_size = min(len(filtered_df), 100000)  # Limit to 100,000 rows or less
train_arima = filtered_df['consumption'][:sample_size][:int(sample_size * 0.8)]
test_arima = filtered_df['consumption'][:sample_size][int(sample_size * 0.8):]

# Fit the ARIMA model
arima_model = ARIMA(train_arima, order=(5, 1, 0))  # Adjust order as needed
arima_model_fit = arima_model.fit()

# 🔹 Step 11: Make Predictions with ARIMA
arima_forecast = arima_model_fit.forecast(steps=len(test_arima))

# 🔹 Step 12: Evaluate Model Performance for ARIMA
mae_arima = mean_absolute_error(test_arima, arima_forecast)
rmse_arima = np.sqrt(mean_squared_error(test_arima, arima_forecast))

print(f"ARIMA Mean Absolute Error (MAE): {mae_arima:.2f}")
print(f"ARIMA Root Mean Squared Error (RMSE): {rmse_arima:.2f}")

# 🔹 Step 13: Visualization (Actual vs. Predicted)
plt.figure(figsize=(10, 5))
sns.lineplot(x=test_arima.index, y=test_arima.values, label="Actual", color="blue")
sns.lineplot(x=test_arima.index, y=arima_forecast, label="ARIMA Predicted", color="red")
sns.lineplot(x=range(len(y_test)), y=y_pred_lgb, label="LightGBM Predicted", color="green")
plt.xlabel("Date")
plt.ylabel("Energy Consumption")
plt.title("Actual vs. Predicted Energy Consumption")
plt.legend()
plt.grid()
plt.show()

# Optimize data types
df['consumption'] = df['consumption'].astype(np.float32)  # Change to float32 if possible
# Repeat for other columns as necessary