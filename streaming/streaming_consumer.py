import os
import sys
import json
import time
import re
import math
import zlib
from datetime import datetime

# Setup Winutils for Windows environment if applicable
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(BASE_DIR, "apps"))

try:
    from fix_windows_hadoop import setup_winutils
    setup_winutils()
except Exception:
    pass

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json, udf, current_timestamp, window, count, expr
from pyspark.sql.types import StructType, StructField, StringType, DoubleType

# Define JSON Schema for incoming Kafka messages
NEWS_SCHEMA = StructType([
    StructField("article_id", StringType(), True),
    StructField("title", StringType(), True),
    StructField("text", StringType(), True),
    StructField("subject", StringType(), True),
    StructField("timestamp", StringType(), True),
    StructField("source", StringType(), True)
])

# Load Trained Spark Model Parameters
PARAMS_PATH = os.path.join(BASE_DIR, "apps", "spark_model_params.json")
if not os.path.exists(PARAMS_PATH):
    raise FileNotFoundError(f"Model parameters file not found at {PARAMS_PATH}. Run 'train_model.py' first.")

with open(PARAMS_PATH, "r") as f:
    MODEL_PARAMS = json.load(f)

print(f"🎉 [Consumer] Loaded trained model weights! (Accuracy: {MODEL_PARAMS.get('accuracy', 99.9)}%)")

# Standard English stop words
STOP_WORDS = set([
    "a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are", 
    "as", "at", "be", "because", "been", "before", "being", "below", "between", "both", "but", 
    "by", "could", "did", "do", "does", "doing", "down", "during", "each", "few", "for", "from", 
    "further", "had", "has", "have", "having", "he", "her", "here", "hers", "herself", "him", 
    "himself", "his", "how", "i", "if", "in", "into", "is", "it", "its", "itself", "just", "me", 
    "more", "most", "my", "myself", "no", "nor", "not", "now", "of", "off", "on", "once", "only", 
    "or", "other", "ought", "our", "ours", "ourselves", "out", "over", "own", "same", "she", 
    "should", "so", "some", "such", "than", "that", "the", "their", "theirs", "them", "themselves", 
    "then", "there", "these", "they", "this", "those", "through", "to", "too", "under", "until", 
    "up", "very", "was", "we", "were", "what", "when", "where", "which", "while", "who", "whom", 
    "why", "with", "would", "you", "your", "yours", "yourself", "yourselves"
])

def murmur3_32(key: str, seed: int = 42) -> int:
    data = key.encode('utf-8')
    length = len(data)
    nblocks = length // 4
    h1 = seed
    c1 = 0xcc9e2d51
    c2 = 0x1b873593

    for block_start in range(0, nblocks * 4, 4):
        k1 = data[block_start] | (data[block_start+1] << 8) | (data[block_start+2] << 16) | (data[block_start+3] << 24)
        k1 = (k1 * c1) & 0xFFFFFFFF
        k1 = ((k1 << 15) | (k1 >> 17)) & 0xFFFFFFFF
        k1 = (k1 * c2) & 0xFFFFFFFF

        h1 ^= k1
        h1 = ((h1 << 13) | (h1 >> 19)) & 0xFFFFFFFF
        h1 = (h1 * 5 + 0xe6546b64) & 0xFFFFFFFF

    tail_index = nblocks * 4
    k1 = 0
    tail_size = length & 3
    if tail_size >= 3:
        k1 ^= data[tail_index + 2] << 16
    if tail_size >= 2:
        k1 ^= data[tail_index + 1] << 8
    if tail_size >= 1:
        k1 ^= data[tail_index]
        k1 = (k1 * c1) & 0xFFFFFFFF
        k1 = ((k1 << 15) | (k1 >> 17)) & 0xFFFFFFFF
        k1 = (k1 * c2) & 0xFFFFFFFF
        h1 ^= k1

    h1 ^= length
    h1 ^= (h1 >> 16)
    h1 = (h1 * 0x85ebca6b) & 0xFFFFFFFF
    h1 ^= (h1 >> 13)
    h1 = (h1 * 0xc2b2ae35) & 0xFFFFFFFF
    h1 ^= (h1 >> 16)

    if h1 & 0x80000000:
        h1 = -((~h1 + 1) & 0xFFFFFFFF)
    return h1

def predict_article(title: str, text: str) -> str:
    full_text = f"{title or ''} {text or ''}"
    cleaned = re.sub(r'[^a-zA-Z\s]', '', full_text.lower())
    words = [w for w in cleaned.split() if w and w not in STOP_WORDS]

    num_features = MODEL_PARAMS["num_features"]
    coefficients = MODEL_PARAMS["coefficients"]
    idf_weights = MODEL_PARAMS["idf_weights"]
    intercept = MODEL_PARAMS["intercept"]

    feature_counts = {}
    for word in words:
        idx = murmur3_32(word, seed=42) % num_features
        feature_counts[idx] = feature_counts.get(idx, 0) + 1

    raw_score = intercept
    for idx, count_val in feature_counts.items():
        if idx < len(coefficients) and idx < len(idf_weights):
            tfidf = count_val * idf_weights[idx]
            raw_score += coefficients[idx] * tfidf

    raw_score = max(-500.0, min(500.0, raw_score))
    prob_fake = 1.0 / (1.0 + math.exp(-raw_score))

    label = "FAKE" if prob_fake >= 0.5 else "REAL"
    confidence = prob_fake if prob_fake >= 0.5 else (1.0 - prob_fake)
    return f"{label} ({confidence * 100:.1f}%)"

# Register Spark PySpark UDF
predict_udf = udf(predict_article, StringType())

def main():
    broker = sys.argv[1] if len(sys.argv) > 1 else "localhost:9092"
    topic = sys.argv[2] if len(sys.argv) > 2 else "news-feed"

    print(f"\n--- ⚡ [Spark Structured Streaming Consumer] Initializing ---")
    print(f"Connecting to Kafka Broker: {broker} | Topic: {topic}")

    spark = SparkSession.builder \
        .appName("FakeNewsStructuredStreaming") \
        .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0") \
        .getOrCreate()

    spark.sparkContext.setLogLevel("WARN")

    # 1. Read Stream from Kafka
    kafka_df = spark.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", broker) \
        .option("subscribe", topic) \
        .option("startingOffsets", "latest") \
        .load()

    # 2. Parse JSON Value
    parsed_df = kafka_df \
        .selectExpr("CAST(value AS STRING) as json_str", "timestamp as kafka_time") \
        .select(from_json(col("json_str"), NEWS_SCHEMA).alias("data"), col("kafka_time")) \
        .select("data.*", "kafka_time")

    # 3. Apply Distributed ML Classification
    classified_df = parsed_df \
        .withColumn("prediction", predict_udf(col("title"), col("text"))) \
        .withColumn("processed_time", current_timestamp())

    # 4. Benchmarking Metrics Listener (Batch Progress)
    class BenchmarkingListener:
        def __init__(self):
            self.total_processed = 0
            self.start_time = time.time()

        def on_batch(self, batch_df, batch_id):
            count_in_batch = batch_df.count()
            if count_in_batch == 0:
                return

            self.total_processed += count_in_batch
            elapsed = time.time() - self.start_time
            throughput = self.total_processed / elapsed if elapsed > 0 else 0

            print("\n" + "="*70)
            print(f"⏱️  [Batch #{batch_id}] Processed {count_in_batch} items | Cumulative: {self.total_processed}")
            print(f"📊 [Throughput Metric]: {throughput:.2f} articles/sec")
            print("="*70)

            # Display sample predictions
            batch_df.select("article_id", "title", "prediction", "source").show(5, truncate=40)

    listener = BenchmarkingListener()

    # 5. Write Stream to Memory Console Sink with 1-second Trigger
    query = classified_df.writeStream \
        .outputMode("append") \
        .foreachBatch(listener.on_batch) \
        .trigger(processingTime="1 second") \
        .start()

    print("\n✅ [Spark Streaming] Stream pipeline actively running! Awaiting Kafka messages...\n")
    query.awaitTermination()

if __name__ == "__main__":
    main()
