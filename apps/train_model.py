import os
import json
import math
from fix_windows_hadoop import setup_winutils
setup_winutils()

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, concat_ws, lower, regexp_replace
from pyspark.ml.feature import Tokenizer, StopWordsRemover, HashingTF, IDF
from pyspark.ml.classification import LogisticRegression
from pyspark.ml import Pipeline
from pyspark.ml.evaluation import MulticlassClassificationEvaluator, BinaryClassificationEvaluator
from pyspark.ml.tuning import CrossValidator, ParamGridBuilder

# ── 1. Spark Session ─────────────────────────────────────────────────────────
spark = SparkSession.builder \
    .appName("FakeNewsModelTraining") \
    .config("spark.driver.memory", "4g") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
processed_path = os.path.join(BASE_DIR, "data", "processed", "cleaned_news.parquet")
export_path    = os.path.join(BASE_DIR, "apps", "spark_model_params.json")

# ── 2. Load processed data ───────────────────────────────────────────────────
print("\n--- [Phase 9] Distributed MLlib Pipeline Construction ---")
df = spark.read.parquet(processed_path)

# Defensive: rebuild text_cleaned in case the column is missing or stale.
# Combines title + text, lowercases and strips non-alpha characters — same
# transformation as preprocessing_analytics.py so the pipeline is consistent.
if "text_cleaned" not in df.columns or "title" not in df.columns:
    print("⚠️  Rebuilding text_cleaned from title + text columns...")
    df = df.withColumn(
        "text_cleaned",
        regexp_replace(lower(concat_ws(" ", col("title"), col("text"))), r"[^a-zA-Z\s]", "")
    )
else:
    # Reinforce: make sure title words are included in the cleaned text
    df = df.withColumn(
        "text_cleaned",
        regexp_replace(
            lower(concat_ws(" ", col("title"), col("text_cleaned"))),
            r"[^a-zA-Z\s]", ""
        )
    )

# Drop nulls in the columns the pipeline needs
df = df.na.drop(subset=["text_cleaned", "label"])

# ── 3. Train / Validation / Test split ──────────────────────────────────────
# 70 % train | 15 % validation (used by CrossValidator) | 15 % held-out test
(train_val_data, test_data) = df.randomSplit([0.85, 0.15], seed=42)
print(f"Train+Val records : {train_val_data.count()}")
print(f"Held-out test     : {test_data.count()}")

# ── 4. ML Pipeline ──────────────────────────────────────────────────────────
#
# Key generalisation improvements vs. previous version:
#
#  • numFeatures=262144  — larger hash space reduces collisions so rare
#    legitimate words don't cancel each other out
#  • minDocFreq=3 on IDF  — ignore tokens that appear in < 3 documents;
#    filters out typos, IDs and one-off noise that cause overfitting
#  • elasticNetParam=0.15 — mixes L1 into the L2 penalty; drives truly
#    uninformative feature weights toward exactly zero (sparse model)
#  • regParam=0.05        — slightly tighter regularisation than 0.01 to
#    reduce memorisation of training-set quirks
#  • maxIter=100          — more gradient steps for convergence on 200k rows
#  • CrossValidator (3-fold) — objective model selection instead of a single
#    lucky random split; picks the regParam that best generalises

tokenizer = Tokenizer(inputCol="text_cleaned", outputCol="words")

remover = StopWordsRemover(inputCol="words", outputCol="filtered")

hashingTF = HashingTF(
    inputCol="filtered",
    outputCol="rawFeatures",
    numFeatures=262144          # 2^18 — large enough to minimise hash collisions
)

idf = IDF(
    inputCol="rawFeatures",
    outputCol="features",
    minDocFreq=3                # ignore tokens seen in fewer than 3 documents
)

lr = LogisticRegression(
    featuresCol="features",
    labelCol="label",
    maxIter=100,
    regParam=0.05,              # tighter than 0.01 to reduce overfitting
    elasticNetParam=0.15,       # 15 % L1 + 85 % L2 — promotes sparsity
    standardization=True        # normalise feature scale before optimisation
)

pipeline = Pipeline(stages=[tokenizer, remover, hashingTF, idf, lr])

# ── 5. Cross-validation over regParam ───────────────────────────────────────
param_grid = ParamGridBuilder() \
    .addGrid(lr.regParam, [0.01, 0.05, 0.1]) \
    .addGrid(lr.elasticNetParam, [0.0, 0.15]) \
    .build()

binary_evaluator = BinaryClassificationEvaluator(
    labelCol="label",
    metricName="areaUnderROC"   # AUC-ROC is more informative than raw accuracy
)

cv = CrossValidator(
    estimator=pipeline,
    estimatorParamMaps=param_grid,
    evaluator=binary_evaluator,
    numFolds=3,                 # 3-fold CV — robust without excessive compute
    seed=42
)

print("\nRunning 3-fold cross-validation over hyperparameter grid...")
print("(This may take a few minutes on large datasets — this is normal)")
cv_model = cv.fit(train_val_data)

best_model = cv_model.bestModel
print(f"\n✅ Best regParam       : {best_model.stages[-1]._java_obj.getRegParam()}")
print(f"✅ Best elasticNet     : {best_model.stages[-1]._java_obj.getElasticNetParam()}")

# ── 6. Evaluate on held-out test set ────────────────────────────────────────
print("\n--- [Phase 10] Model Evaluation on Held-Out Test Set ---")
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

print(f"\n📊 Accuracy          : {accuracy:.4f}  ({accuracy*100:.2f}%)")
print(f"📊 F1-Score          : {f1:.4f}  ({f1*100:.2f}%)")
print(f"📊 Precision         : {precision:.4f}")
print(f"📊 Recall            : {recall:.4f}")
print(f"📊 AUC-ROC           : {auc:.4f}")

# ── 7. Export parameters for FastAPI inference ───────────────────────────────
lr_model  = best_model.stages[-1]   # LogisticRegressionModel
idf_model = best_model.stages[-2]   # IDFModel

# num_features must match what the backend uses for hashing
num_features = best_model.stages[2].getNumFeatures()

model_params = {
    "num_features"   : num_features,
    "intercept"      : float(lr_model.intercept),
    "coefficients"   : [float(x) for x in lr_model.coefficients.toArray()],
    "idf_weights"    : [float(x) for x in idf_model.idf.toArray()],
    "accuracy"       : round(accuracy  * 100, 2),
    "f1_score"       : round(f1        * 100, 2),
    "precision"      : round(precision * 100, 2),
    "recall"         : round(recall    * 100, 2),
    "auc_roc"        : round(auc       * 100, 2),
    "model_name"     : "Logistic Regression (PySpark MLlib — CV-tuned, ElasticNet)",
    "reg_param"      : float(lr_model._java_obj.getRegParam()),
    "elastic_net"    : float(lr_model._java_obj.getElasticNetParam()),
    "training_rows"  : int(train_val_data.count()),
}

with open(export_path, "w") as f:
    json.dump(model_params, f, indent=2)

print(f"\n🎉 Model parameters exported to: {export_path}")
print(f"   num_features = {num_features}")
print(f"   accuracy     = {accuracy*100:.2f}%")
print(f"   AUC-ROC      = {auc*100:.2f}%")

spark.stop()
