import os
from fix_windows_hadoop import setup_winutils
setup_winutils()

from pyspark.sql import SparkSession

# 1. Initialize Spark
spark = SparkSession.builder \
    .appName("HDFS_Data_Ingestion") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

print("\n--- [Phase 5] Data Ingestion into HDFS ---")

# Robust relative path resolution
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
raw_folder = os.path.join(BASE_DIR, "data", "raw")
hdfs_path = os.path.join(BASE_DIR, "data", "hdfs_simulated", "raw_news.parquet")

# Read from Local folder containing multiple CSV files
if os.path.exists(raw_folder):
    csv_wildcard = os.path.join(raw_folder, "*.csv")
    print(f"Ingesting all CSV files from {csv_wildcard} into Distributed Storage...")
    df = spark.read.csv(csv_wildcard, header=True, inferSchema=True)
    print(f"Total ingested records: {df.count()}")
    df.write.mode("overwrite").parquet(hdfs_path)
    print("Ingestion Complete. Data is now in HDFS-ready format.")
else:
    print(f"⚠️ Error: Local raw folder not found at: {raw_folder}")

spark.stop()
