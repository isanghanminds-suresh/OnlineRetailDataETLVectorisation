"""
Spark ETL Script for Retail Data Cleaning
----------------------------------------
- Loads raw retail CSV data
- Cleans and filters records (removes cancelled, negative/zero quantities, negative prices)
- Adds total_amount column
- Writes cleaned data to Parquet
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import col

# Initialize Spark session
spark = SparkSession.builder.appName("RetailETL").getOrCreate()

# Load raw data
RAW_CSV_PATH = "data/raw/raw_online_retail.csv"
PROCESSED_PARQUET_PATH = "data/processed/clean_online_retail.parquet"

retail_raw_df = spark.read.csv(
    RAW_CSV_PATH,
    header=True,
    inferSchema=True
)

# Transform phase: Data cleaning and transformation
retail_transform_df = (
    retail_raw_df.filter(~col("Invoice").startswith('C'))
                 .filter(col("Quantity") > 0)
                 .filter(col("Price") >= 0)
                 .withColumn("total_amount", col("Quantity") * col("Price"))
)

# Write cleaned data to Parquet
retail_transform_df.write.mode("overwrite").parquet(PROCESSED_PARQUET_PATH)

spark.stop()

