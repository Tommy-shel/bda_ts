import os
from fix_windows_hadoop import setup_winutils
setup_winutils()

from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col, lower, regexp_replace, length, concat_ws,
    trim, when, udf
)
from pyspark.sql.types import StringType

# ── Spark Session ─────────────────────────────────────────────────────────────
spark = SparkSession.builder \
    .appName("FakeNewsPreprocessing") \
    .config("spark.driver.memory", "4g") \
    .config("spark.sql.shuffle.partitions", "8") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
raw_folder     = os.path.join(BASE_DIR, "data", "raw")
processed_path = os.path.join(BASE_DIR, "data", "processed", "cleaned_news.parquet")

# ── Phase 7: Load & Clean ─────────────────────────────────────────────────────
print("\n--- [Phase 7] Data Cleaning ---")

csv_wildcard = os.path.join(raw_folder, "*.csv")
print(f"Loading all CSVs from: {csv_wildcard}")
df = spark.read.csv(csv_wildcard, header=True, inferSchema=True)
print(f"Total raw records loaded: {df.count()}")

# ── Label normalisation ───────────────────────────────────────────────────────
# Ensure label is integer 0/1 and drop anything else
df = df.withColumn("label", col("label").cast("int"))
df = df.filter(col("label").isin([0, 1]))

# ── Drop rows missing the fields we actually need ─────────────────────────────
df = df.na.drop(subset=["title", "text", "label"])

# ── Remove duplicate articles (same title + same label) ──────────────────────
before_dedup = df.count()
df = df.dropDuplicates(["title", "text"])
after_dedup = df.count()
print(f"Removed {before_dedup - after_dedup} duplicates  →  {after_dedup} records remain")

# ── Filter out very short articles (< 20 chars of text) ──────────────────────
df = df.filter(length(trim(col("text"))) >= 20)
print(f"After length filter: {df.count()} records")

# ── Text cleaning ─────────────────────────────────────────────────────────────
# Strategy:
#   1. Combine title (weighted 3×) + text for richer signal on short articles
#   2. Lower-case
#   3. Strip URLs, mentions, HTML tags
#   4. Keep only alphabetic + space
#   5. Collapse multiple spaces

df_cleaned = df \
    .withColumn(
        "combined_raw",
        concat_ws(
            " ",
            col("title"), col("title"), col("title"),   # title repeated 3× — boosts title signal
            col("text")
        )
    ) \
    .withColumn("text_cleaned", lower(col("combined_raw"))) \
    .withColumn("text_cleaned", regexp_replace(col("text_cleaned"), r"https?://\S+", " ")) \
    .withColumn("text_cleaned", regexp_replace(col("text_cleaned"), r"@\w+", " ")) \
    .withColumn("text_cleaned", regexp_replace(col("text_cleaned"), r"<[^>]+>", " ")) \
    .withColumn("text_cleaned", regexp_replace(col("text_cleaned"), r"[^a-zA-Z\s]", " ")) \
    .withColumn("text_cleaned", regexp_replace(col("text_cleaned"), r"\s{2,}", " ")) \
    .withColumn("text_cleaned", trim(col("text_cleaned")))

# Drop if cleaning left an empty string
df_cleaned = df_cleaned.filter(length(col("text_cleaned")) > 10)

# ── Feature: article length (raw character count of body text) ────────────────
df_cleaned = df_cleaned.withColumn("article_length", length(col("text")))

# ── Phase 8: Analytics ────────────────────────────────────────────────────────
print("\n--- [Phase 8] Big Data Analytics ---")

print("1. Label distribution  (0=Real, 1=Fake):")
df_cleaned.groupBy("label").count().orderBy("label").show()

print("2. Average article length by label:")
df_cleaned.groupBy("label").avg("article_length").orderBy("label").show()

print("3. News count by subject (top 15):")
df_cleaned.groupBy("subject").count().orderBy(col("count").desc()).show(15)

print("4. Sample cleaned records:")
df_cleaned.select("title", "label", "article_length").show(5, truncate=60)

# ── Save ──────────────────────────────────────────────────────────────────────
df_final = df_cleaned.select("title", "text", "text_cleaned", "subject", "label", "article_length")
df_final.write.mode("overwrite").parquet(processed_path)

final_count = df_final.count()
print(f"\n✅ Saved {final_count} cleaned records to: {processed_path}")

spark.stop()
