from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import json
import re
import math
import zlib

app = FastAPI(title="Fake News Detection BDA API")

# Enable CORS for React Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PARAMS_PATH = os.path.join(BASE_DIR, "apps", "spark_model_params.json")

# Standard English stop words matching Spark's StopWordsRemover
STOP_WORDS = set([
    "a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are", 
    "as", "at", "be", "because", "been", "before", "being", "below", "between", "both", "but", 
    "by", "could", "did", "do", "does", "doing", "down", "during", "each", "few", "for", "from", 
    "further", "had", "has", "have", "having", "he", "her", "here", "hers", "herself", "him", 
    "himself", "his", "how", "i", "if", "in", "into", "is", "it", "its", "itself", "just", "me", 
    "more", "most", "my", "myself", "no", "nor", "not", "now", "of", "off", "on", "once", "only", 
    "or", "other", "ought", "our", "ours", "ourselves", "out", "over", "own", "same", "she", 
    "should", "so", "some", "such", "than", "that", "the", "their", "theirs", "them", "themselves", 
    "then", "there", "these", "they", "this", "those", "through", "to", "too", "under", "until", 
    "up", "very", "was", "we", "were", "what", "when", "where", "which", "while", "who", "whom", 
    "why", "with", "would", "you", "your", "yours", "yourself", "yourselves"
])

model_params = None

def load_params():
    global model_params
    if os.path.exists(PARAMS_PATH):
        with open(PARAMS_PATH, "r") as f:
            model_params = json.load(f)
            print("🎉 Loaded PySpark MLlib weights successfully!")
    else:
        print("⚠️ Model parameters file not found. Run 'train_model.py' first.")

load_params()

class NewsInput(BaseModel):
    title: str
    text: str

def predict_with_spark_weights(text: str):
    # 1. Clean and tokenize text
    cleaned = re.sub(r'[^a-zA-Z\s]', '', text.lower())
    words = [w for w in cleaned.split() if w and w not in STOP_WORDS]
    
    num_features = model_params["num_features"]
    coefficients = model_params["coefficients"]
    idf_weights = model_params["idf_weights"]
    intercept = model_params["intercept"]
    
    # 2. HashingTF (Hash words into feature buckets)
    feature_counts = {}
    for word in words:
        # Murmur/CRC hash simulation to match Spark feature indices
        idx = abs(zlib.crc32(word.encode('utf-8'))) % num_features
        feature_counts[idx] = feature_counts.get(idx, 0) + 1

    # 3. Compute Dot Product (Weights * Features * IDF) + Intercept
    raw_score = intercept
    for idx, count in feature_counts.items():
        if idx < len(coefficients) and idx < len(idf_weights):
            tfidf = count * idf_weights[idx]
            raw_score += coefficients[idx] * tfidf

    # 4. Logistic Sigmoid Function: 1 / (1 + e^(-z))
    # Bound score to avoid overflow
    raw_score = max(-500.0, min(500.0, raw_score))
    prob_fake = 1.0 / (1.0 + math.exp(-raw_score))
    
    if prob_fake >= 0.5:
        return "FAKE", prob_fake
    else:
        return "REAL", (1.0 - prob_fake)

@app.get("/")
def read_root():
    return {
        "status": "Online", 
        "engine": "PySpark MLlib",
        "model_loaded": model_params is not None
    }

@app.post("/predict")
async def predict_news(news: NewsInput):
    global model_params
    if model_params is None:
        load_params()
        if model_params is None:
            raise HTTPException(status_code=500, detail="Spark Model weights not found. Please run 'train_model.py' first.")

    full_text = f"{news.title} {news.text}"
    label, confidence = predict_with_spark_weights(full_text)

    return {
        "prediction": label,
        "confidence": f"{confidence * 100:.2f}%",
        "title": news.title,
        "model_used": model_params.get("model_name", "Spark MLlib Logistic Regression")
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
