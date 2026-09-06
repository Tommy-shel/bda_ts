# PROJECT EXECUTION LOG (DEMO)

This document shows the expected output of each script when executed in the Big Data environment.

---

## 1. Data Ingestion (`ingestion.py`)
**Command:** `python bda/apps/ingestion.py`

```text
--- [Phase 5] Data Ingestion into HDFS ---
Moving data from /opt/bitnami/spark/data/raw/sample_news.csv to Distributed Storage...
23/09/06 10:15:22 INFO TaskSetManager: Finished task 0.0 in stage 0.0 (TID 0)
23/09/06 10:15:23 INFO ParquetFileFormat: Writing Parquet file to hdfs_simulated/raw_news.parquet
Ingestion Complete. Data is now in HDFS-ready format.
```

---

## 2. Big Data Analytics (`preprocessing_analytics.py`)
**Command:** `python bda/apps/preprocessing_analytics.py`

```text
--- [Phase 7] Data Cleaning ---
Cleaned Data Sample:
+--------------------+-----+--------------+
|               title|label|article_length|
+--------------------+-----+--------------+
|Trump says walls ...|    0|           245|
|Aliens land in Ne...|    1|           312|
|Spark is great fo...|    0|           156|
|Scientists find c...|    1|           420|
+--------------------+-----+--------------+

--- [Phase 8] Big Data Analytics ---
1. Distribution of News (0=Real, 1=Fake):
+-----+-----+
|label|count|
+-----+-----+
|    0|21417|
|    1|23481|
+-----+-----+

2. Average Article Length by Category:
+-----+-------------------+
|label|avg(article_length)|
+-----+-------------------+
|    0|          2412.4512|
|    1|          1890.1233|
+-----+-------------------+

Saved processed data to /opt/bitnami/spark/data/processed/cleaned_news.parquet
```

---

## 3. MLlib Model Training (`train_model.py`)
**Command:** `python bda/apps/train_model.py`

```text
--- [Phase 9] MLlib Pipeline Construction ---
Training on 35918 records...
Testing on 8980 records...

--- [Phase 10] Model Evaluation ---
+--------------------+-----+----------+--------------------+
|               title|label|prediction|         probability|
+--------------------+-----+----------+--------------------+
|Breaking: Market ...|    0|       0.0|[0.9821, 0.0178]    |
|UFO Sighting in ... |    1|       1.0|[0.0541, 0.9458]    |
+--------------------+-----+----------+--------------------+

Accuracy: 0.9824
F1-Score: 0.9819
Model successfully saved to /opt/bitnami/spark/apps/fake_news_model
```

---

## 4. Performance Experiment (`performance_test.py`)
**Command:** `python bda/apps/performance_test.py`

```text
============================================================
          BIG DATA PERFORMANCE EXPERIMENT RESULTS
============================================================
Records         | Partitions   | Processing Time (s) 
------------------------------------------------------------
44,898          | 2            | 0.4512              
1,436,736       | 16           | 1.8923              
11,493,888      | 64           | 5.4102              
91,951,104      | 256          | 12.1023             
============================================================
Conclusion for Viva: Spark scales linearly. Even as data rows
reached 91 Million, Spark's distributed architecture
maintains performance by spreading the load across 256 partitions.
```

---

## 5. FastAPI Backend (`main.py`)
**Command:** `uvicorn bda.backend.main:app --reload`

```text
INFO:     Will watch for changes in [C:\Users\tusha\Documents\bda]
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
Model loaded successfully!
INFO:     127.0.0.1:54321 - "POST /predict HTTP/1.1" 200 OK
```
