import os
import sys
import json
import time
import csv
import argparse
from datetime import datetime

try:
    from kafka import KafkaProducer
except ImportError:
    print("Installing kafka-python dependency...")
    os.system(f"{sys.executable} -m pip install kafka-python feedparser")
    from kafka import KafkaProducer

import feedparser

# Resolve paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_PATH = os.path.join(BASE_DIR, "data", "raw", "trending_news_100k.csv")

RSS_FEEDS = [
    "http://feeds.bbci.co.uk/news/world/rss.xml",
    "https://rss.nytimes.com/services/xml/rss/nyt/World.xml",
    "https://news.google.com/rss?hl=en-US&gl=US&ceid=US:en"
]

def create_kafka_producer(broker="localhost:9092"):
    print(f"Connecting to Kafka broker at {broker}...")
    producer = None
    retries = 10
    while retries > 0:
        try:
            producer = KafkaProducer(
                bootstrap_servers=[broker],
                value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                key_serializer=lambda k: k.encode('utf-8') if k else None
            )
            print("Connected to Kafka successfully!")
            return producer
        except Exception as e:
            print(f"Waiting for Kafka broker to be ready... ({retries} retries left)")
            time.sleep(3)
            retries -= 1
    raise RuntimeError("Failed to connect to Kafka Broker.")

def stream_from_csv(producer, topic, rate=50):
    print(f"\n🚀 [Producer] Starting CSV Stream Simulation at ~{rate} msg/sec into topic '{topic}'...")
    if not os.path.exists(CSV_PATH):
        print(f"⚠️ Error: CSV dataset not found at {CSV_PATH}")
        return

    delay = 1.0 / rate if rate > 0 else 0
    count = 0
    start_time = time.time()

    while True:
        with open(CSV_PATH, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                msg = {
                    "article_id": f"csv-{count}",
                    "title": row.get("title", ""),
                    "text": row.get("text", ""),
                    "subject": row.get("subject", "general"),
                    "timestamp": datetime.utcnow().isoformat(),
                    "source": "CSV_Simulation"
                }
                producer.send(topic, key=msg["article_id"], value=msg)
                count += 1

                if count % 100 == 0:
                    elapsed = time.time() - start_time
                    throughput = count / elapsed if elapsed > 0 else 0
                    print(f"⚡ [Producer] Sent {count} articles | Current Rate: {throughput:.1f} msg/sec")

                if delay > 0:
                    time.sleep(delay)

def stream_from_rss(producer, topic, interval=15):
    print(f"\n📡 [Producer] Starting Live RSS Feed Stream into topic '{topic}' (polling every {interval}s)...")
    count = 0
    seen_links = set()

    while True:
        for feed_url in RSS_FEEDS:
            try:
                feed = feedparser.parse(feed_url)
                for entry in feed.entries:
                    link = entry.get("link", entry.get("id", ""))
                    if link in seen_links:
                        continue
                    seen_links.add(link)

                    title = entry.get("title", "")
                    summary = entry.get("summary", title)
                    msg = {
                        "article_id": f"rss-{count}",
                        "title": title,
                        "text": summary,
                        "subject": "world",
                        "timestamp": datetime.utcnow().isoformat(),
                        "source": feed_url
                    }
                    producer.send(topic, key=msg["article_id"], value=msg)
                    count += 1
                    print(f"📰 [Live Feed] Published: '{title[:60]}...'")
            except Exception as e:
                print(f"Error reading feed {feed_url}: {e}")

        time.sleep(interval)

def main():
    parser = argparse.ArgumentParser(description="Big Data Real-Time Kafka News Producer")
    parser.add_argument("--mode", choices=["csv", "rss"], default="csv", help="Mode: 'csv' for benchmark simulation or 'rss' for live RSS feed")
    parser.add_argument("--broker", default="localhost:9092", help="Kafka broker host:port")
    parser.add_argument("--topic", default="news-feed", help="Kafka topic name")
    parser.add_argument("--rate", type=int, default=100, help="Simulation rate (messages/sec)")
    args = parser.parse_args()

    producer = create_kafka_producer(args.broker)

    if args.mode == "csv":
        stream_from_csv(producer, args.topic, rate=args.rate)
    else:
        stream_from_rss(producer, args.topic)

if __name__ == "__main__":
    main()
