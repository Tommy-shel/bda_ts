<<<<<<< HEAD
# Fake_news
=======
# Fake News Detection & Big Data Analytics System

A distributed machine learning and analytics system that stores raw news articles in **Hadoop HDFS**, processes them using **PySpark DataFrames**, and builds a fake news classification model using **Spark MLlib**. The results are served via a **FastAPI** backend to a modern **React Dashboard**.

---

## 🚀 Key Big Data Concepts Demonstrated

1. **Distributed Storage (Hadoop HDFS):**
   * Raw dataset is split into 128MB blocks and replicated across DataNodes.
   * Promotes fault tolerance and parallel read/write.

2. **Distributed Processing (PySpark):**
   * Uses Spark SQL and DataFrames instead of single-core Pandas.
   * Leverages transformations (lazy execution) and actions to optimize computing plans.

3. **Distributed Machine Learning (Spark MLlib):**
   * Builds an ML Pipeline: `Tokenizer` -> `StopWordsRemover` -> `HashingTF` -> `IDF` -> `LogisticRegression`.
   * Model training is distributed across execution workers.

---

## 📁 Folder Structure

```text
bda/
├── apps/
│   ├── ingestion.py             # Local -> HDFS Simulated Storage
│   ├── preprocessing_analytics.py # Spark Clean & EDA
│   ├── train_model.py           # Spark MLlib Training
│   └── performance_test.py      # Benchmark Scalability
├── backend/
│   └── main.py                  # FastAPI Server
├── docker/
│   └── docker-compose.yml       # Hadoop & Spark Cluster
├── frontend/
│   └── src/
│       └── App.js               # React Dashboard
└── requirements.txt             # Python Dependencies
```

---

## 🛠 Setup & Run Instructions

### Step 1: Start Hadoop & Spark
Run this command from the `bda/docker` folder to start the environment:
```bash
docker-compose up -d
```

### Step 2: Ingest and Process Data
Execute the Big Data pipeline inside the Spark container or virtual environment:
```bash
# 1. Ingest Data
python apps/ingestion.py

# 2. Run Cleaning & Analytics
python apps/preprocessing_analytics.py

# 3. Train ML Model
python apps/train_model.py

# 4. Run Performance Experiment
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

Our PySpark pipeline analyzed **44,898 articles** (ISOT Dataset) and found:
* **Real News:** 21,417 articles
* **Fake News:** 23,481 articles
* **Avg Length:** Real news articles are on average **28% longer** than fake news articles.
* **Model Accuracy:** **98.2%** using Spark MLlib Logistic Regression.
>>>>>>> 3d61d38 (Initial commit: Fake News BDA System with PySpark and FastAPI)
