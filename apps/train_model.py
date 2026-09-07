import os
import json
import math
from fix_windows_hadoop import setup_winutils
setup_winutils()

from pyspark.sql import SparkSession
from pyspark.ml.feature import Tokenizer, StopWordsRemover, HashingTF, IDF
from pyspark.ml.classification import LogisticRegression
from pyspark.ml import Pipeline
from pyspark.ml.evaluation import MulticlassClassificationEvaluator

# 1. Initialize Spark
spark = SparkSession.builder \
    .appName("FakeNewsModelTraining") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
processed_path = os.path.join(BASE_DIR, "data", "processed", "cleaned_news.parquet")
export_path = os.path.join(BASE_DIR, "apps", "spark_model_params.json")

print("\n--- [Phase 9] Distributed MLlib Pipeline Construction ---")
df = spark.read.parquet(processed_path)

# ML Pipeline Stages
tokenizer = Tokenizer(inputCol="text_cleaned", outputCol="words")
remover = StopWordsRemover(inputCol="words", outputCol="filtered")
hashingTF = HashingTF(inputCol="filtered", outputCol="rawFeatures", numFeatures=20000)
idf = IDF(inputCol="rawFeatures", outputCol="features")
lr = LogisticRegression(featuresCol="features", labelCol="label")

pipeline = Pipeline(stages=[tokenizer, remover, hashingTF, idf, lr])

# Train / Test split
(train_data, test_data) = df.randomSplit([0.8, 0.2], seed=123)
print(f"Training on {train_data.count()} records across distributed partitions...")
print(f"Testing on {test_data.count()} records...")

# Train Spark MLlib Model
model = pipeline.fit(train_data)

# Evaluate
print("\n--- [Phase 10] Model Evaluation on Spark ---")
predictions = model.transform(test_data)
predictions.select("title", "label", "prediction", "probability").show(5)

evaluator = MulticlassClassificationEvaluator(labelCol="label", predictionCol="prediction")
accuracy = evaluator.evaluate(predictions, {evaluator.metricName: "accuracy"})
f1 = evaluator.evaluate(predictions, {evaluator.metricName: "f1"})

print(f"✨ Spark Model Accuracy: {accuracy:.4f}")
print(f"✨ Spark Model F1-Score: {f1:.4f}")

# Extract Learned Spark MLlib Parameters for Production Serving
lr_model = model.stages[-1]
idf_model = model.stages[-2]

model_params = {
    "num_features": 20000,
    "intercept": float(lr_model.intercept),
    "coefficients": [float(x) for x in lr_model.coefficients.toArray()],
    "idf_weights": [float(x) for x in idf_model.idf.toArray()],
    "accuracy": round(accuracy * 100, 2),
    "f1_score": round(f1 * 100, 2),
    "model_name": "Logistic Regression (PySpark MLlib Distributed)"
}

with open(export_path, "w") as f:
    json.dump(model_params, f, indent=2)

print(f"🎉 Model parameters exported for FastAPI serving to: {export_path}")
spark.stop()
