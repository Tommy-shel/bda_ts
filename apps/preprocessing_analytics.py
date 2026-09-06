import os
from fix_windows_hadoop import setup_winutils
setup_winutils()

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, lower, regexp_replace, length

# 1. Initialize Spark
spark = SparkSession.builder \
    .appName("FakeNewsPreprocessing") \
    .getOrCreate()

# Disable logs for cleaner output
spark.sparkContext.setLogLevel("WARN")

# Robust paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
raw_folder = os.path.join(BASE_DIR, "data", "raw")
processed_path = os.path.join(BASE_DIR, "data", "processed", "cleaned_news.parquet")

print("\n--- [Phase 7] Data Cleaning ---")
if not os.path.exists(raw_folder):
    print(f"⚠️ Error: Raw folder not found at {raw_folder}")
    spark.stop()
    exit()

csv_wildcard = os.path.join(raw_folder, "*.csv")
print(f"Loading and combining all datasets from {csv_wildcard}...")
df = spark.read.csv(csv_wildcard, header=True, inferSchema=True)
print(f"Total raw records loaded: {df.count()}")

# Remove nulls
df = df.na.drop()

# Text Cleaning: Lowercase and remove special characters
df_cleaned = df.withColumn("text_cleaned", lower(col("text"))) \
               .withColumn("text_cleaned", regexp_replace(col("text_cleaned"), "[^a-zA-Z\\s]", ""))

# Add a feature: article_length
df_cleaned = df_cleaned.withColumn("article_length", length(col("text")))

print("Cleaned Data Sample:")
df_cleaned.select("title", "label", "article_length").show(5)

print("\n--- [Phase 8] Big Data Analytics ---")

# A. Real vs Fake distribution
print("1. Distribution of News (0=Real, 1=Fake):")
df_cleaned.groupBy("label").count().show()

# B. Avg length of Real vs Fake news
print("2. Average Article Length by Category:")
df_cleaned.groupBy("label").avg("article_length").show()

# C. News by Subject
print("3. News Count by Subject:")
df_cleaned.groupBy("subject").count().orderBy(col("count").desc()).show()

# 3. Save processed data (Parquet is better for Big Data than CSV)
df_cleaned.write.mode("overwrite").parquet(processed_path)
print(f"Saved processed data to {processed_path}")

spark.stop()
