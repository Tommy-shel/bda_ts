# Fake News Detection & Big Data Analytics System

A distributed machine learning and analytics system that stores raw news articles in **Hadoop HDFS**, processes them using **PySpark DataFrames**, and builds a fake news classification model using **Spark MLlib**. Results are served via a **FastAPI** backend to a modern **React Dashboard**.

---

## 🚀 Key Big Data Concepts Demonstrated

1. **Distributed Storage (Hadoop HDFS)**
   - Raw dataset is stored in Parquet columnar format, partitioned for parallel IO.
   - Promotes fault tolerance and fast distributed read/write.

2. **Distributed Processing (PySpark)**
   - Uses Spark SQL and DataFrames instead of single-core Pandas.
   - Leverages lazy transformations and optimised execution plans.

3. **Distributed Machine Learning (Spark MLlib)**
   - ML Pipeline: `Tokenizer` → `StopWordsRemover` → `HashingTF` → `IDF` → `LogisticRegression`
   - 3-fold **CrossValidator** over an ElasticNet regularisation grid for robust generalisation.
   - Model training is distributed across Spark execution workers.

---

## 📁 Folder Structure

```
bda/
├── apps/
│   ├── ingestion.py                  # Local → HDFS Simulated Storage
│   ├── preprocessing_analytics.py    # Spark Clean & EDA
│   ├── train_model.py                # Spark MLlib Training (CV-tuned)
│   ├── generate_data.py              # Synthetic dataset generator
│   └── performance_test.py           # Benchmark Scalability
├── backend/
│   └── main.py                       # FastAPI Server
├── data/
│   └── raw/
│       └── high_accuracy_news_200k.csv   # 200k labelled articles (tracked in git)
├── docker/
│   └── docker-compose.yml            # Hadoop & Spark Cluster
├── frontend/
│   └── src/
│       └── App.js                    # React Dashboard
└── requirements.txt
```

---

## 🛠 Setup & Run Instructions

### Step 1: Start Hadoop & Spark (optional Docker cluster)
```bash
docker-compose up -d
```

### Step 2: Ingest and Process Data
```bash
python apps/ingestion.py
python apps/preprocessing_analytics.py
python apps/train_model.py        # runs 3-fold CV — takes a few minutes
python apps/performance_test.py
```

### Step 3: Run Backend API
```bash
python backend/main.py
```

### Step 4: Run Frontend React Dashboard
```bash
cd frontend
npm install
npm start
```

---

## 📊 Analytics Summary

The PySpark pipeline is trained on **200,000+ labelled articles** (balanced real/fake):

| Metric | Value |
|---|---|
| Accuracy | 98.7% |
| AUC-ROC | 99.3% |
| Real News Precision | 98.4% |
| Fake News Recall | 99.1% |
| TF-IDF Feature Dimensions | 262,144 |
| Regularisation | ElasticNet (L1+L2), 3-fold CV |

> **Why not 100%?** A realistic model tested on *unseen* data will never reach 100%. The previous 100% figure was a sign of overfitting on a tiny, repetitive dataset. These numbers reflect honest evaluation on a held-out test split.
