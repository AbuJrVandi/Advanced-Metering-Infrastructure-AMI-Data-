# Advanced Metering Infrastructure (AMI) Data Analysis

## Project Overview
This project focuses on analyzing *Advanced Metering Infrastructure (AMI) data* within a simulated smart grid environment. It applies *data preprocessing, exploratory data analysis (EDA), machine learning, and GIS techniques* to extract insights on energy consumption patterns, detect anomalies, and forecast demand. 

## Technologies Used
- *Python* – Primary language for data processing and analysis.
- *MySQL* – Database for storing and managing AMI data.
- *Pandas & NumPy* – Data manipulation, cleaning, and numerical computations.
- *Matplotlib & Seaborn* – Data visualization tools for trends and anomalies.
- *Scikit-learn & XGBoost* – Machine learning models for clustering, anomaly detection, and forecasting.
- *GeoPandas & Folium* – GIS tools for geospatial analysis of energy usage.

## Data Preprocessing
To ensure clean and reliable data, the following preprocessing steps were performed:

1. *Handling Missing Values:*
   - Mean/Mode imputation for numerical and categorical data.
   - Forward-fill and backward-fill for time-series data.
   - Dropping excessive missing values when necessary.

2. *Removing Duplicates:*
   - Identifying duplicate records using Pandas' drop_duplicates().
   - Standardizing text data to avoid case-sensitive duplicates.
   - Using unique Meter IDs to detect redundant entries.

3. *Data Normalization & Scaling:*
   - *Min-Max Scaling:* Rescales values between 0 and 1.
   - *Z-score Scaling:* Adjusts values to a normal distribution.
   - *Log Transformation:* Handles skewed data distributions.

4. *Outlier Detection:*
   - *Z-score Analysis:* Identifies extreme deviations from the mean.
   - *Interquartile Range (IQR):* Filters values beyond 1.5x IQR.
   - *Isolation Forest:* A machine learning approach for anomaly detection.

5. *Data Splitting:*
   - Train-test split (80% training, 20% testing) for evaluation.
   - *K-Fold Cross-validation* for robust model performance.
   - *Stratified Sampling* to maintain class balance in classification problems.

## Exploratory Data Analysis (EDA)
- *Anomaly Detection:* Identified unusual consumption patterns using statistical and ML techniques.
- *Billing Analysis:* Evaluated discrepancies between actual and expected billing amounts.
- *Consumption Clustering:* Segmented customers based on energy usage using K-Means clustering.
- *Load Forecasting:* Predicted future energy demand using LightGBM and ARIMA models.
- *GIS Analysis:* Mapped energy consumption trends using spatial visualization techniques.

## Key Findings
- *Identified billing anomalies* that could help improve revenue collection.
- *Clustered customer consumption* patterns for demand-side management.
- *Detected seasonal trends* in energy usage, aiding in capacity planning.
- *Predicted future demand* with high accuracy using machine learning models.
- *Mapped high-energy consumption areas* for optimized infrastructure planning.

## Future Enhancements
- Implement *real-time data processing* using Apache Spark.
- Improve *anomaly detection* with deep learning techniques (Autoencoders, Isolation Forest).
- Integrate *external data sources* (weather, economic indicators) to enhance forecasting accuracy.
- Expand *GIS capabilities* with more detailed geospatial datasets.

## Repository Structure

├── data/                 # Raw and processed datasets
├── notebooks/            # Jupyter notebooks for data analysis
├── scripts/              # Python scripts for preprocessing, modeling, and visualization
├── results/              # Outputs, reports, and visualizations
├── README.md             # Project documentation


## How to Run the Project
1. Clone the repository:
   bash
   git clone https://github.com/your-username/ami-data-analysis.git
   
2. Install dependencies:
   bash
   pip install -r requirements.txt
   
3. Run the preprocessing script:
   bash
   python scripts/preprocess_data.py
   
4. Execute the analysis notebooks in notebooks/

## License
This project is open-source and available under
