import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import json
import re
import math
import zlib
import time
import random
import urllib.request
import urllib.parse

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

# ── Trending News ─────────────────────────────────────────────────────────────
# Primary: GNews free API (100 req/day, no credit card needed).
# Set GNEWS_API_KEY in environment to enable.  Without it the endpoint
# rotates through a curated fallback pool so the site always works.

GNEWS_API_KEY = os.environ.get("GNEWS_API_KEY", "")

# Rotating fallback pool — spans multiple topics and sources.
# New items will appear automatically as the list rotates each request.
FALLBACK_POOL = [
    # --- World / Conflict ---
    {"title": "India-Pakistan ceasefire talks resume along Line of Control", "source": "Reuters", "url": "https://reuters.com", "label": "world", "tag": "real"},
    {"title": "Russia launches fresh missile strikes on Ukrainian power grid", "source": "BBC News", "url": "https://bbc.com/news", "label": "world", "tag": "real"},
    {"title": "NATO foreign ministers meet to discuss eastern flank reinforcement", "source": "Reuters", "url": "https://reuters.com", "label": "world", "tag": "real"},
    {"title": "UN warns of worsening humanitarian crisis in Sudan conflict zones", "source": "Al Jazeera", "url": "https://aljazeera.com", "label": "world", "tag": "real"},
    {"title": "China conducts live-fire naval exercises near Taiwan Strait", "source": "Reuters", "url": "https://reuters.com", "label": "world", "tag": "real"},
    {"title": "North Korea fires ballistic missile into Sea of Japan", "source": "BBC News", "url": "https://bbc.com/news", "label": "world", "tag": "real"},
    {"title": "Gaza ceasefire talks continue as mediators seek agreement", "source": "Al Jazeera", "url": "https://aljazeera.com", "label": "world", "tag": "real"},
    {"title": "Iran seizes oil tanker in Strait of Hormuz over alleged violation", "source": "Reuters", "url": "https://reuters.com", "label": "world", "tag": "real"},
    # --- Tech ---
    {"title": "OpenAI announces major update to reasoning model capabilities", "source": "The Verge", "url": "https://theverge.com", "label": "tech", "tag": "real"},
    {"title": "EU regulators open antitrust probe into cloud computing dominance", "source": "Reuters", "url": "https://reuters.com", "label": "tech", "tag": "real"},
    {"title": "Apple unveils new chip architecture for next-generation devices", "source": "The Verge", "url": "https://theverge.com", "label": "tech", "tag": "real"},
    {"title": "Cybersecurity agency warns of critical vulnerability in network software", "source": "Wired", "url": "https://wired.com", "label": "tech", "tag": "real"},
    # --- Health / Science ---
    {"title": "WHO releases updated antibiotic prescribing guidance to combat resistance", "source": "BBC News", "url": "https://bbc.com/news", "label": "health", "tag": "real"},
    {"title": "Clinical trial shows promise for new drug-resistant tuberculosis treatment", "source": "Reuters", "url": "https://reuters.com", "label": "health", "tag": "real"},
    {"title": "Scientists confirm water ice deposits in permanently shadowed lunar craters", "source": "NASA", "url": "https://nasa.gov", "label": "science", "tag": "real"},
    # --- Business ---
    {"title": "Central bank raises interest rates by quarter-point to curb inflation", "source": "Reuters", "url": "https://reuters.com", "label": "business", "tag": "real"},
    {"title": "Global trade volumes expand for third consecutive quarter", "source": "Reuters", "url": "https://reuters.com", "label": "business", "tag": "real"},
    # --- Misinformation examples (for context) ---
    {"title": "SHOCKING: Pakistan launches secret nuclear strike — governments hiding it", "source": "Viral Post", "url": "#", "label": "misinformation", "tag": "fake"},
    {"title": "BREAKING: China invades US coast with 2 million troops, media blackout", "source": "Viral Post", "url": "#", "label": "misinformation", "tag": "fake"},
    {"title": "EXPOSED: 5G towers confirmed to transmit mind-control frequencies", "source": "Viral Post", "url": "#", "label": "misinformation", "tag": "fake"},
    {"title": "URGENT: WW3 officially started 2 hours ago — all governments hiding it", "source": "Viral Post", "url": "#", "label": "misinformation", "tag": "fake"},
]

# Simple in-process cache: {query_key: (timestamp, data)}
_trending_cache: dict = {}
CACHE_TTL = 300  # 5 minutes

def _fetch_gnews(category: str = "world", max_items: int = 6) -> list:
    """Fetch from GNews API. Returns [] on any error."""
    if not GNEWS_API_KEY:
        return []
    try:
        params = urllib.parse.urlencode({
            "category": category,
            "lang": "en",
            "max": max_items,
            "apikey": GNEWS_API_KEY,
        })
        url = f"https://gnews.io/api/v4/top-headlines?{params}"
        req = urllib.request.Request(url, headers={"User-Agent": "FakeNewsDetector/1.0"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode())
        articles = data.get("articles", [])
        return [
            {
                "title": a.get("title", ""),
                "source": a.get("source", {}).get("name", "GNews"),
                "url": a.get("url", "#"),
                "publishedAt": a.get("publishedAt", ""),
                "label": category,
                "tag": "real",
            }
            for a in articles
            if a.get("title")
        ]
    except Exception:
        return []

def _get_trending(tab: str = "all") -> list:
    """Return trending items — live from GNews when possible, fallback otherwise."""
    now = time.time()
    cache_key = tab

    # Return cached result if fresh
    if cache_key in _trending_cache:
        ts, cached = _trending_cache[cache_key]
        if now - ts < CACHE_TTL:
            return cached

    category_map = {
        "world":    "world",
        "tech":     "technology",
        "health":   "health",
        "business": "business",
        "science":  "science",
        "all":      "world",
    }
    gnews_category = category_map.get(tab, "world")
    live = _fetch_gnews(category=gnews_category, max_items=6)

    if live:
        result = live
    else:
        # Rotate the fallback pool so different items appear each refresh
        pool = FALLBACK_POOL.copy()
        random.shuffle(pool)
        if tab == "all":
            result = pool[:6]
        else:
            filtered = [x for x in pool if x["label"] == tab]
            result = (filtered + pool)[:6]

    _trending_cache[cache_key] = (now, result)
    return result


class NewsInput(BaseModel):
    title: str
    text: str

# Pure Python MurmurHash3_x86_32 implementation matching Spark's HashingTF
def murmur3_32(key: str, seed: int = 42) -> int:
    data = key.encode('utf-8')
    length = len(data)
    nblocks = length // 4
    h1 = seed
    c1 = 0xcc9e2d51
    c2 = 0x1b873593

    # body
    for block_start in range(0, nblocks * 4, 4):
        k1 = data[block_start] | (data[block_start+1] << 8) | (data[block_start+2] << 16) | (data[block_start+3] << 24)
        k1 = (k1 * c1) & 0xFFFFFFFF
        k1 = ((k1 << 15) | (k1 >> 17)) & 0xFFFFFFFF
        k1 = (k1 * c2) & 0xFFFFFFFF

        h1 ^= k1
        h1 = ((h1 << 13) | (h1 >> 19)) & 0xFFFFFFFF
        h1 = (h1 * 5 + 0xe6546b64) & 0xFFFFFFFF

    # tail
    tail_index = nblocks * 4
    k1 = 0
    tail_size = length & 3
    if tail_size >= 3:
        k1 ^= data[tail_index + 2] << 16
    if tail_size >= 2:
        k1 ^= data[tail_index + 1] << 8
    if tail_size >= 1:
        k1 ^= data[tail_index]
        k1 = (k1 * c1) & 0xFFFFFFFF
        k1 = ((k1 << 15) | (k1 >> 17)) & 0xFFFFFFFF
        k1 = (k1 * c2) & 0xFFFFFFFF
        h1 ^= k1

    # finalization
    h1 ^= length
    h1 ^= (h1 >> 16)
    h1 = (h1 * 0x85ebca6b) & 0xFFFFFFFF
    h1 ^= (h1 >> 13)
    h1 = (h1 * 0xc2b2ae35) & 0xFFFFFFFF
    h1 ^= (h1 >> 16)

    # Convert to signed 32-bit int
    if h1 & 0x80000000:
        h1 = -((~h1 + 1) & 0xFFFFFFFF)
    return h1

def predict_with_spark_weights(text: str):
    # 1. Clean and tokenize text
    cleaned = re.sub(r'[^a-zA-Z\s]', '', text.lower())
    words = [w for w in cleaned.split() if w and w not in STOP_WORDS]
    
    # Read num_features from the exported model params so it always stays in
    # sync with whatever the training script used (50k, 262k, etc.)
    num_features = model_params.get("num_features", 262144)
    coefficients = model_params["coefficients"]
    idf_weights = model_params["idf_weights"]
    intercept = model_params["intercept"]
    
    # 2. HashingTF (Hash words into feature buckets using Murmur3 to match Spark)
    feature_counts = {}
    for word in words:
        idx = murmur3_32(word, seed=42) % num_features
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
        "model_loaded": model_params is not None,
        "accuracy": model_params.get("accuracy") if model_params else None,
        "auc_roc": model_params.get("auc_roc") if model_params else None,
        "num_features": model_params.get("num_features") if model_params else None,
    }

@app.get("/trending")
def get_trending(tab: str = "all"):
    """
    Returns live trending headlines.
    tab: all | world | tech | health | business | science
    Results are cached for 5 minutes to respect API rate limits.
    Falls back to a rotating curated pool when the API key is absent or the
    upstream API is unavailable.
    """
    items = _get_trending(tab=tab)
    return {
        "tab": tab,
        "items": items,
        "cached": tab in _trending_cache,
        "source": "live" if GNEWS_API_KEY else "fallback",
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
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)