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
local_path = os.path.join(BASE_DIR, "data", "raw", "sample_news.csv")
hdfs_path = os.path.join(BASE_DIR, "data", "hdfs_simulated", "raw_news.parquet")

# Read from Local
if os.path.exists(local_path):
    df = spark.read.csv(local_path, header=True, inferSchema=True)
    print(f"Moving data from {local_path} to Distributed Storage...")
    df.write.mode("overwrite").parquet(hdfs_path)
    print("Ingestion Complete. Data is now in HDFS-ready format.")
else:
    print(f"⚠️ Error: Local raw news file not found at: {local_path}")

spark.stop()
