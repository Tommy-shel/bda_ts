# Real-Time Spark Structured Streaming & Kafka Pipeline

This folder contains the **Real-Time Streaming Pipeline** for Big Data Fake News Classification, extending the batch PySpark MLlib model into a sub-second distributed streaming consumer.

---

## 🏗 Architecture Overview

```
[News Feed CSV / Live RSS]
         │
         ▼
 🚀 Kafka Producer (streaming/producer.py)
         │
         ▼ (Topic: news-feed)
 📦 Apache Kafka Buffer (Docker)
         │
         ▼
 ⚡ Spark Structured Streaming Consumer (streaming/streaming_consumer.py)
         │
         ├── 🔍 Murmur3 TF-IDF Vectorization
         ├── 🧠 Spark MLlib Logistic Regression Inference
         └── 📊 Real-Time Throughput Benchmark (Articles/Sec)
```

---

## 🚀 How to Run Locally

### Step 1: Start Docker Infrastructure (Kafka + Zookeeper + Spark)
```bash
cd docker
docker-compose up -d
```
*Verify containers are running using `docker ps`.*

---

### Step 2: Start the Kafka Producer
You can run the producer in two modes:

#### Mode A: Benchmark Simulation Mode (100k CSV Stream)
Simulates a high-throughput live feed (e.g., 100 articles/sec) from `data/raw/trending_news_100k.csv`:
```bash
python streaming/producer.py --mode csv --rate 100
```

#### Mode B: Live RSS News Feed Mode
Fetches real-time live headlines from BBC and NYT RSS feeds:
```bash
python streaming/producer.py --mode rss
```

---

### Step 3: Start the Spark Structured Streaming Consumer
In a separate terminal, launch the streaming consumer:
```bash
python streaming/streaming_consumer.py
```

---

## 📊 Benchmarking & Performance Output

The consumer logs real-time throughput metrics (articles/second) per micro-batch trigger window:

```
======================================================================
⏱️  [Batch #4] Processed 120 items | Cumulative: 480
📊 [Throughput Metric]: 118.50 articles/sec
======================================================================
+------------+----------------------------------------+----------------+----------------+
|  article_id|                                   title|      prediction|          source|
+------------+----------------------------------------+----------------+----------------+
|      csv-480|Nepal Flood Relief Efforts Continue...  |  REAL (100.0%)|  CSV_Simulation|
|      csv-481|5G TOWERS ACTIVATED: Millions Hijacked  |  FAKE (100.0%)|  CSV_Simulation|
+------------+----------------------------------------+----------------+----------------+
```

---

## ⚙️ Configuration Parameters
* `--broker`: Kafka Broker host (`localhost:9092` default).
* `--topic`: Kafka topic name (`news-feed` default).
* `--rate`: Producer generation rate (messages/sec).
