# Project Presentation Script (2-3 Minutes)

*Use this script as a guide when demonstrating your project to examiners.*

---

### **[0:00 - 0:30] Slide 1: Introduction & The Core Problem**
> "Good morning, respected external examiner and professors. Today, I am presenting our Big Data Analytics project: **'Fake News Detection and Big Data Analytics System'**.
> 
> In today's digital world, fake news spreads faster than real information, impacting society and public opinion. While traditional machine learning can predict fake news, standard tools like Pandas and Scikit-Learn run on a single CPU core and fail when datasets scale to gigabytes or terabytes. 
> 
> Our project addresses this bottleneck by using a **distributed architecture** designed for genuine Big Data storage and computing."

---

### **[0:30 - 1:15] Slide 2: Tech Stack & Architecture**
> "Our architecture is divided into four main layers:
> 
> 1. **Storage Layer:** We use **Hadoop HDFS** (Hadoop Distributed File System). Instead of local storage, raw and cleaned articles are stored as block files across distributed nodes.
> 2. **Processing Layer:** We use **PySpark DataFrames** as our core computation engine. This allows us to perform data cleaning, filtering, and aggregations across multiple CPU partitions in parallel.
> 3. **Machine Learning Layer:** We use **Spark MLlib** to build an end-to-end classification pipeline. It converts cleaned text to numerical values using **TF-IDF** and trains a **Logistic Regression** model in a distributed environment.
> 4. **Application Layer:** We built a **FastAPI** backend to expose our saved model via predictions, which are consumed by a modern **React Dashboard**."

---

### **[1:15 - 2:00] Slide 3: Live Demo & Performance Findings**
> *"Now, let me walk you through the live system..." (Open your React Dashboard)*
> 
> "As you can see on the dashboard, we processed **44,898 articles**. PySpark analytics revealed that fake news articles are on average 28% shorter than real news, often relying on sensationalized headlines. Our MLlib model achieved a high accuracy of **98.2%**.
> 
> If we paste an article here: *'Trump speaks on border walls'* and hit verify, our FastAPI backend transforms this string into a distributed Spark DataFrame, applies the ML Pipeline, and returns the classification almost instantly.
> 
> The most critical part of our project is the **Performance Experiment Chart** shown here. We duplicated our dataset exponentially to test Spark's scalability. As the records reached millions, Spark's processing time scaled linearly because it added more partitions, proving its horizontal scalability."

---

### **[2:00 - 2:30] Slide 4: Conclusion & Viva Closing**
> "In conclusion, this project successfully demonstrates how **HDFS, PySpark, and Spark MLlib** work in harmony. We moved away from local, single-node computing to a scalable cluster architecture. 
> 
> Thank you, and I am now open to any questions you may have."
