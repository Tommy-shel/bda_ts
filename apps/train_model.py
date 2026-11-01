import os
import json
from fix_windows_hadoop import setup_winutils
setup_winutils()

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, concat_ws, lower, regexp_replace, trim, length
from pyspark.ml.feature import (
    Tokenizer, StopWordsRemover, HashingTF, IDF,
    NGram, VectorAssembler
)
from pyspark.ml.classification import LogisticRegression
from pyspark.ml import Pipeline
from pyspark.ml.evaluation import MulticlassClassificationEvaluator, BinaryClassificationEvaluator
from pyspark.ml.tuning import CrossValidator, ParamGridBuilder

# ── 1. Spark Session ──────────────────────────────────────────────────────────
spark = SparkSession.builder \
    .appName("FakeNewsModelTraining") \
    .config("spark.driver.memory", "6g") \
    .config("spark.sql.shuffle.partitions", "8") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

BASE_DIR       = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
processed_path = os.path.join(BASE_DIR, "data", "processed", "cleaned_news.parquet")
model_path     = os.path.join(BASE_DIR, "apps", "fake_news_model")
export_path    = os.path.join(BASE_DIR, "apps", "spark_model_params.json")

# ── 2. Load processed data ────────────────────────────────────────────────────
print("\n--- [Phase 9] Distributed MLlib Pipeline Construction ---")
df = spark.read.parquet(processed_path)
print(f"Loaded {df.count()} records from processed parquet")

# ── Defensive: ensure text_cleaned exists and is solid ───────────────────────
if "text_cleaned" not in df.columns:
    print("⚠️  Rebuilding text_cleaned from title + text ...")
    df = df.withColumn(
        "text_cleaned",
        trim(regexp_replace(
            lower(concat_ws(" ", col("title"), col("title"), col("title"), col("text"))),
            r"[^a-zA-Z\s]", " "
        ))
    )

df = df.na.drop(subset=["text_cleaned", "label"])
df = df.filter(length(trim(col("text_cleaned"))) > 10)

# ── Label as integer ──────────────────────────────────────────────────────────
df = df.withColumn("label", col("label").cast("double"))

print(f"Records after cleaning: {df.count()}")
print("Label distribution:")
df.groupBy("label").count().orderBy("label").show()

# ── 3. Train / Test split ─────────────────────────────────────────────────────
# 85% train+val  |  15% held-out test
(train_val_data, test_data) = df.randomSplit([0.85, 0.15], seed=42)
train_val_data.cache()
test_data.cache()
print(f"Train+Val : {train_val_data.count()}")
print(f"Test      : {test_data.count()}")

# ── 4. Pipeline — Unigram + Bigram TF-IDF ────────────────────────────────────
#
# Accuracy improvements over the previous version:
#
#  Unigram branch:
#   • numFeatures=262144  (2^18) — large hash space, fewer collisions
#   • minDocFreq=5        — drop tokens appearing in <5 docs (noise/typos)
#
#  Bigram branch (NEW):
#   • Captures two-word phrases like "fake news", "breaking exclusive",
#     "deep state", "scientists say" — patterns strongly correlated with
#     real vs. fake writing style
#   • numFeatures=131072  (2^17) — bigrams are sparser so smaller space
#   • minDocFreq=5
#
#  VectorAssembler merges both feature vectors before LR.
#
#  Logistic Regression:
#   • regParam / elasticNetParam tuned via 3-fold CrossValidator
#   • maxIter=200  — more iterations for convergence on 206k rows
#   • standardization=True

# --- Unigram branch ---
tokenizer   = Tokenizer(inputCol="text_cleaned", outputCol="words")
remover     = StopWordsRemover(inputCol="words", outputCol="filtered_words")
hashingTF_1 = HashingTF(inputCol="filtered_words", outputCol="rawFeatures1", numFeatures=262144)
idf_1       = IDF(inputCol="rawFeatures1", outputCol="features1", minDocFreq=5)

# --- Bigram branch ---
ngram       = NGram(n=2, inputCol="filtered_words", outputCol="bigrams")
hashingTF_2 = HashingTF(inputCol="bigrams", outputCol="rawFeatures2", numFeatures=131072)
idf_2       = IDF(inputCol="rawFeatures2", outputCol="features2", minDocFreq=5)

# --- Merge ---
assembler = VectorAssembler(
    inputCols=["features1", "features2"],
    outputCol="features"
)

# --- Classifier ---
lr = LogisticRegression(
    featuresCol="features",
    labelCol="label",
    maxIter=200,
    regParam=0.05,
    elasticNetParam=0.1,
    standardization=True,
    threshold=0.5
)

pipeline = Pipeline(stages=[
    tokenizer, remover,
    hashingTF_1, idf_1,
    ngram, hashingTF_2, idf_2,
    assembler, lr
])

# ── 5. Cross-validation ───────────────────────────────────────────────────────
param_grid = ParamGridBuilder() \
    .addGrid(lr.regParam,        [0.01, 0.05, 0.1]) \
    .addGrid(lr.elasticNetParam, [0.0,  0.1,  0.2]) \
    .build()

binary_evaluator = BinaryClassificationEvaluator(
    labelCol="label",
    metricName="areaUnderROC"
)

cv = CrossValidator(
    estimator=pipeline,
    estimatorParamMaps=param_grid,
    evaluator=binary_evaluator,
    numFolds=3,
    seed=42
)

print("\n🔄 Running 3-fold cross-validation (9 hyperparameter combos × 3 folds)...")
print("   This will take several minutes on 206k rows — this is expected.\n")
cv_model = cv.fit(train_val_data)

best_model = cv_model.bestModel
best_lr    = best_model.stages[-1]   # LogisticRegressionModel

print(f"✅ Best regParam      : {best_lr._java_obj.getRegParam()}")
print(f"✅ Best elasticNet    : {best_lr._java_obj.getElasticNetParam()}")

# ── 6. Evaluate on held-out test set ─────────────────────────────────────────
print("\n--- [Phase 10] Evaluation on Held-Out Test Set ---")
predictions = best_model.transform(test_data)
predictions.select("label", "prediction", "probability").show(10)

multi_eval = MulticlassClassificationEvaluator(
    labelCol="label", predictionCol="prediction"
)
accuracy  = multi_eval.evaluate(predictions, {multi_eval.metricName: "accuracy"})
f1        = multi_eval.evaluate(predictions, {multi_eval.metricName: "f1"})
precision = multi_eval.evaluate(predictions, {multi_eval.metricName: "weightedPrecision"})
recall    = multi_eval.evaluate(predictions, {multi_eval.metricName: "weightedRecall"})
auc       = binary_evaluator.evaluate(predictions)

print(f"\n📊 Accuracy   : {accuracy:.4f}  ({accuracy*100:.2f}%)")
print(f"📊 F1-Score   : {f1:.4f}  ({f1*100:.2f}%)")
print(f"📊 Precision  : {precision:.4f}")
print(f"📊 Recall     : {recall:.4f}")
print(f"📊 AUC-ROC    : {auc:.4f}")

# ── 7. Save model to disk ─────────────────────────────────────────────────────
print(f"\n💾 Saving model to: {model_path}")
best_model.write().overwrite().save(model_path)

# ── 8. Export params for FastAPI inference ────────────────────────────────────
# Stage indices in the merged pipeline:
#   0  Tokenizer
#   1  StopWordsRemover
#   2  HashingTF (unigrams)
#   3  IDF (unigrams)       ← idf_model_1
#   4  NGram
#   5  HashingTF (bigrams)
#   6  IDF (bigrams)        ← idf_model_2
#   7  VectorAssembler
#   8  LogisticRegression   ← lr_model

stages       = best_model.stages
idf_model_1  = stages[3]
idf_model_2  = stages[6]
lr_model     = stages[8]

num_features_1 = stages[2].getNumFeatures()
num_features_2 = stages[5].getNumFeatures()

model_params = {
    # Unigram branch
    "num_features"       : num_features_1,
    "idf_weights"        : [float(x) for x in idf_model_1.idf.toArray()],
    # Bigram branch
    "num_features_bigram": num_features_2,
    "idf_weights_bigram" : [float(x) for x in idf_model_2.idf.toArray()],
    # LR model
    "intercept"          : float(lr_model.intercept),
    "coefficients"       : [float(x) for x in lr_model.coefficients.toArray()],
    # Metrics
    "accuracy"           : round(accuracy  * 100, 2),
    "f1_score"           : round(f1        * 100, 2),
    "precision"          : round(precision * 100, 2),
    "recall"             : round(recall    * 100, 2),
    "auc_roc"            : round(auc       * 100, 2),
    # Meta
    "model_name"         : "Logistic Regression — Unigram+Bigram TF-IDF (3-fold CV, ElasticNet)",
    "reg_param"          : float(lr_model._java_obj.getRegParam()),
    "elastic_net"        : float(lr_model._java_obj.getElasticNetParam()),
    "training_rows"      : int(train_val_data.count()),
    "pipeline_stages"    : "Tokenizer → StopWords → HashTF(uni) → IDF → NGram(2) → HashTF(bi) → IDF → Assembler → LR",
}

with open(export_path, "w") as f:
    json.dump(model_params, f, indent=2)

print(f"\n🎉 Model parameters exported to: {export_path}")
print(f"   Unigram features  = {num_features_1}")
print(f"   Bigram  features  = {num_features_2}")
print(f"   Accuracy          = {accuracy*100:.2f}%")
print(f"   AUC-ROC           = {auc*100:.2f}%")

spark.stop()
