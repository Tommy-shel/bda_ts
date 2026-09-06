from pyspark.sql import SparkSession

# 1. Initialize SparkSession (The entry point to Spark)
spark = SparkSession.builder \
    .appName("FakeNewsDataCheck") \
    .getOrCreate()

print("\n" + "="*50)
print("PYSPARK ENVIRONMENT IS WORKING!")
print("="*50 + "\n")

# 2. Read the local CSV file
df = spark.read.csv("/opt/bitnami/spark/data/raw/sample_news.csv", header=True, inferSchema=True)

# 3. Show the data
print("Sample Data:")
df.show()

# 4. Print Schema (Big Data needs structured schemas)
print("Data Schema:")
df.printSchema()

# 5. Basic Count
print(f"Total Records: {df.count()}")

spark.stop()
