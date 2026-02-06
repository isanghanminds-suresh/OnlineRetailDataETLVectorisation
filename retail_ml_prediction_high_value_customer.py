"""
Retail ML Prediction: High-Value Customer Classification
-------------------------------------------------------
This script loads cleaned retail transaction data, performs feature engineering (RFM, one-hot encoding, label encoding), and prepares a machine-learning-ready dataset for high-value customer prediction.

Steps:
1. Load cleaned data from Parquet file.
2. Parse and clean columns (dates, missing values, outliers).
3. Feature engineering: label encoding, one-hot encoding, RFM metrics.
4. Create binary target for high-value customers.
5. Drop unnecessary columns and shuffle dataset.
6. Save ML-ready data to CSV.
"""

import pandas as pd
from datetime import datetime
from sklearn.preprocessing import LabelEncoder

# --- 1. Load Dataset ---
PARQUET_PATH = "data/processed/clean_online_retail.parquet"
traindata = pd.read_parquet(PARQUET_PATH)

# --- 2. Data Cleaning ---
traindata['InvoiceDate'] = pd.to_datetime(traindata['InvoiceDate'], errors='coerce')
ORIGINAL_COLUMNS = list(traindata.columns)
traindata['Customer ID'] = traindata['Customer ID'].fillna('Guest')
UPPER_PRICE = traindata['Price'].quantile(0.99)
traindata = traindata[traindata['Price'] <= UPPER_PRICE]

# --- 3. Feature Engineering ---
le_product = LabelEncoder()
traindata['Product_enc'] = le_product.fit_transform(traindata['StockCode'])
traindata['DayOfWeek'] = traindata['InvoiceDate'].dt.weekday
traindata['Month'] = traindata['InvoiceDate'].dt.month
traindata = pd.get_dummies(traindata, columns=['DayOfWeek', 'Month'], prefix=['Day', 'Month'])

# --- 4. RFM Features ---
REFERENCE_DATE = traindata['InvoiceDate'].max() + pd.Timedelta(days=1)
rfm = traindata.groupby('Customer ID').agg({
    'InvoiceDate': lambda x: (REFERENCE_DATE - x.max()).days,  # Recency
    'Invoice': 'nunique',                                      # Frequency
    'Quantity': 'sum',                                         # Monetary (total items)
    'Price': 'mean'                                            # Avg price per item
}).reset_index()
rfm.rename(columns={
    'InvoiceDate': 'Recency',
    'Invoice': 'Frequency',
    'Quantity': 'Monetary',
    'Price': 'AvgPrice'
}, inplace=True)

# --- 5. Classification Target ---
THRESHOLD = rfm['Monetary'].quantile(0.75)  # top 25% customers
rfm['HighValue'] = (rfm['Monetary'] > THRESHOLD).astype(int)

# --- 6. Merge and Clean Final Dataset ---
traindata_ml = traindata.merge(rfm, on='Customer ID', how='left')
traindata_ml = traindata_ml.drop(ORIGINAL_COLUMNS, axis=1)
traindata_ml = traindata_ml.drop(["Monetary", "AvgPrice"], axis=1)
traindata_ml = traindata_ml.sample(frac=1, random_state=42).reset_index(drop=True)  # Shuffle

# --- 7. Output ---
print(traindata_ml.head(50))
print(len(traindata_ml.columns))
traindata_ml.to_csv("train_data_retail_data.csv", index=False)
