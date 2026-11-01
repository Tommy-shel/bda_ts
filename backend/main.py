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
    # ── INDIA — Last Week Trending (Oct 25 – Nov 1, 2026) ─────────────────
    {
        "title": "INDIA bloc mega rally at Ramlila Maidan demands CEC Gyanesh Kumar's resignation over voter deletions",
        "source": "Indian Express",
        "url": "https://indianexpress.com/article/india/delhi-ramlila-maidan-india-bloc-congress-protest-sir-cec-gyanesh-kumar-rahul-gandhi-mamata-banerjee-mehbooba-mufti-akhilesh-yadav-mallikarjun-kharge-10946030/",
        "publishedAt": "2026-11-01T00:00:00Z",
        "label": "world",
        "tag": "real",
    },
    {
        "title": "Rahul Gandhi calls 2024 Lok Sabha elections 'illegal', leads 'Save Democracy' march to Ramlila Maidan",
        "source": "The Hindu",
        "url": "https://www.thehindu.com/news/national/india-bloc-public-impeachment-cec-gyanesh-kumar-sir-protest-chalo-dilli-march-rahul-gandhi-live-updates-october-31-2026/article71648094.ece",
        "publishedAt": "2026-10-31T00:00:00Z",
        "label": "world",
        "tag": "real",
    },
    {
        "title": "ED arrests Azam Khan outside Rampur jail moments after his release",
        "source": "News9 Live",
        "url": "https://www.news9live.com/india/breaking-news-live-updates-todays-news-headlines-october-31-2026-3020550",
        "publishedAt": "2026-10-31T00:00:00Z",
        "label": "world",
        "tag": "real",
    },
    {
        "title": "AAP releases first list of 40 candidates for Punjab Assembly election; CM Bhagwant Mann to contest from Dhuri",
        "source": "The Hindu",
        "url": "https://www.thehindu.com/news/the-hindu-top-news-of-the-day-october-31-2026/article71649365.ece",
        "publishedAt": "2026-10-31T00:00:00Z",
        "label": "world",
        "tag": "real",
    },
    {
        "title": "BJP slams Congress president Kharge over 'indecent' remarks against PM Modi at Patna event",
        "source": "Indian Express",
        "url": "https://indianexpress.com/article/india/india-news-live-updates-25-october-2026-delhi-mumbai-weather-breaking-latest-karnataka-odisha-cjp-protest-genz-10935685/",
        "publishedAt": "2026-10-25T00:00:00Z",
        "label": "world",
        "tag": "real",
    },
    {
        "title": "Farooq Abdullah says Pakistan kept Kashmir issue alive at international forums, BJP hits back",
        "source": "Indian Express",
        "url": "https://indianexpress.com/article/india/india-news-live-updates-24-october-2026-delhi-mumbai-weather-breaking-news-pollution-cjp-tamil-nadu-rain-10934574/",
        "publishedAt": "2026-10-24T00:00:00Z",
        "label": "world",
        "tag": "real",
    },
    {
        "title": "Tiger Shroff firing case: Crime Branch arrests accused; CJP protest leads to police action in Delhi",
        "source": "Indian Express",
        "url": "https://indianexpress.com/article/india/breaking-india-news-live-updates-20-october-2026-cjp-delhi-police-protest-crime-branch-accident-weather-rain-gyanesh-kumar-rss-tiger-shroff-shooting-10928827/",
        "publishedAt": "2026-10-20T00:00:00Z",
        "label": "world",
        "tag": "real",
    },
    {
        "title": "Kerala Mini Cooper crash: Court grants two-day custody to four accused in Nedumbassery road fatality",
        "source": "Indian Express",
        "url": "https://indianexpress.com/article/india/india-news-live-updates-30-october-2026-delhi-rain-mumbai-weather-pm-modi-sir-supreme-court-jamia-student-union-election-10942866/",
        "publishedAt": "2026-10-30T00:00:00Z",
        "label": "world",
        "tag": "real",
    },

    # ── GLOBAL — Last Week Trending (Oct 25 – Nov 1, 2026) ────────────────
    {
        "title": "Oil hits $117 a barrel as Hormuz shipping attacks complicate US-Iran diplomatic efforts",
        "source": "Al Jazeera",
        "url": "https://ca.finance.yahoo.com/news/oil-hits-six-month-highs-064011885.html",
        "publishedAt": "2026-10-31T00:00:00Z",
        "label": "business",
        "tag": "real",
    },
    {
        "title": "Trump says Iran 'wants to talk' and predicts the war will end 'very soon'",
        "source": "Fox News",
        "url": "https://www.foxnews.com/live-news/us-iran-war-oil-prices-strait-hormuz-10-30-26",
        "publishedAt": "2026-10-30T00:00:00Z",
        "label": "world",
        "tag": "real",
    },
    {
        "title": "US State Department approves $2.1 billion Patriot PAC-3 missile sale to Ukraine",
        "source": "Anadolu Agency",
        "url": "https://aa.com.tr/en/world/morning-briefing-oct-31-2026/4107022",
        "publishedAt": "2026-10-31T00:00:00Z",
        "label": "world",
        "tag": "real",
    },
    {
        "title": "NATO allies fear Trump will delay Patriot deliveries to Ukraine until after US midterms",
        "source": "Euronews",
        "url": "https://www.euronews.com/2026/10/29/nato-allies-fear-trump-will-delay-patriot-missiles-for-ukraine-until-after-us-midterms",
        "publishedAt": "2026-10-29T00:00:00Z",
        "label": "world",
        "tag": "real",
    },
    {
        "title": "Federal Reserve holds interest rates steady; two FOMC members dissent in favour of a quarter-point hike",
        "source": "NPR",
        "url": "https://www.npr.org/2026/10/30/nx-s1-6023370/the-news-roundup-for-october-30-2026",
        "publishedAt": "2026-10-30T00:00:00Z",
        "label": "business",
        "tag": "real",
    },
    {
        "title": "North Korea-linked hackers behind Binance cyberattack, blockchain intelligence firm says",
        "source": "Reuters",
        "url": "https://www.yahoo.com/news/world/articles/latest-news-bulletin-october-31st-110015150.html",
        "publishedAt": "2026-10-31T00:00:00Z",
        "label": "tech",
        "tag": "real",
    },
    {
        "title": "COP17 biodiversity summit: Financing gap for Kunming-Montreal framework remains largely unfilled",
        "source": "Global Issues / IPS",
        "url": "https://www.globalissues.org/news/2026/10",
        "publishedAt": "2026-10-30T00:00:00Z",
        "label": "science",
        "tag": "real",
    },
    {
        "title": "Canada aims to double non-US trade within a decade as Ottawa diversifies ties globally",
        "source": "Reuters",
        "url": "https://www.yahoo.com/news/world/articles/latest-news-bulletin-october-31st-060033855.html",
        "publishedAt": "2026-10-31T00:00:00Z",
        "label": "business",
        "tag": "real",
    },
    {
        "title": "Trump weighs Iran deal against military option to 'finish them off' as Gulf tensions spike",
        "source": "CBS News",
        "url": "https://www.cbsnews.com/live-updates/iran-war-trump-us-oil-gas-prices-strait-of-hormuz-midterms/",
        "publishedAt": "2026-10-30T00:00:00Z",
        "label": "world",
        "tag": "real",
    },
    {
        "title": "Xi Jinping's party central committee meeting focuses on discipline ahead of expected fourth-term bid",
        "source": "NPR",
        "url": "https://www.npr.org/sections/world/",
        "publishedAt": "2026-10-31T00:00:00Z",
        "label": "world",
        "tag": "real",
    },
    {
        "title": "Post-tropical cyclone Rachel batters California coast, beachfront homes damaged in Long Beach",
        "source": "AP / Yahoo News",
        "url": "https://ca.news.yahoo.com/major-global-news-moments-october-164718493.html",
        "publishedAt": "2026-10-12T00:00:00Z",
        "label": "world",
        "tag": "real",
    },
    {
        "title": "Russia-Ukraine diesel refinery dispute: Trump presses Kyiv to halt strikes as energy prices soar",
        "source": "Foreign Policy",
        "url": "https://foreignpolicy.com/2026/10/30/trump-russia-diesel-deal-putin-prices-midterms-iran-war/",
        "publishedAt": "2026-10-30T00:00:00Z",
        "label": "business",
        "tag": "real",
    },

    # ── Disasters — India (last week) ─────────────────────────────────────
    {
        "title": "Cyclone Arnab makes landfall on Andhra Pradesh coast; nine dead, 180,000 evacuated",
        "source": "Indian Express",
        "url": "https://indianexpress.com/article/india/cyclone-arnab-live-updates-killed-in-andhra-pradesh-heavy-rainfall-likely-for-next-3-days-10941359/",
        "publishedAt": "2026-10-29T00:00:00Z",
        "label": "world",
        "tag": "real",
    },
    {
        "title": "Cyclone Arnab: Rs 4,600 crore damage in AP; 325,000 hectares of crops inundated, Odisha airlifts 300 villages",
        "source": "ETV Bharat / Reuters",
        "url": "https://www.etvbharat.com/en/bharat/cyclone-arnab-update-deavstation-in-andhra-pradesh-casualties-odisha-rain-enn26102900680",
        "publishedAt": "2026-10-30T00:00:00Z",
        "label": "world",
        "tag": "real",
    },
    {
        "title": "Cyclone Arnab: 50+ trains cancelled; 12,500 trees uprooted in West Godavari, Konaseema, Kakinada",
        "source": "Times of India",
        "url": "https://timesofindia.indiatimes.com/city/vijayawada/cyclone-arnab-2-dead-several-flights-cancelled-over-50-trains-cancelled-as-storm-hits-andhra-odisha/articleshow/135256160.cms",
        "publishedAt": "2026-10-29T00:00:00Z",
        "label": "world",
        "tag": "real",
    },

    # ── Disasters — Global (last 3 weeks) ──────────────────────────────────
    {
        "title": "Hurricane Isaias makes Category 2 landfall in Destin, Florida; nine dead, insured losses top $2 billion",
        "source": "NPR",
        "url": "https://www.npr.org/2026/10/10/g-s1-147632/at-least-2-deaths-attributed-to-isaias-after-hurricane-bashes-florida-and-alabama",
        "publishedAt": "2026-10-10T00:00:00Z",
        "label": "world",
        "tag": "real",
    },
    {
        "title": "Magnitude 7.5 earthquake strikes Panama; three dead, 3,390 homes damaged, state of emergency declared",
        "source": "UNICEF / Reuters",
        "url": "https://www.unicefusa.org/stories/unicef-focuses-what-children-need-after-earthquake-hits-panama",
        "publishedAt": "2026-10-09T00:00:00Z",
        "label": "world",
        "tag": "real",
    },
    {
        "title": "Magnitude 7.0 earthquake kills 16, injures 76 in Tibet's Nagqu; 339 homes collapse at 4,800m altitude",
        "source": "Al Jazeera",
        "url": "https://www.aljazeera.com/news/2026/10/22/magnitude-7-earthquake-kills-16-people-in-chinas-tibet-xinhua-reports",
        "publishedAt": "2026-10-22T00:00:00Z",
        "label": "world",
        "tag": "real",
    },
    {
        "title": "Kilauea volcano paused after episode 55; USGS forecasts episode 56 eruption between November 2–9",
        "source": "USGS / Fox Weather",
        "url": "https://www.foxweather.com/extreme-weather/kilauea-hawaii-volcano-eruption-forecast-usgs-episode-56",
        "publishedAt": "2026-10-31T00:00:00Z",
        "label": "science",
        "tag": "real",
    },
    {
        "title": "Post-tropical cyclone Rachel batters California coast; beachfront homes damaged in Long Beach",
        "source": "AP / Yahoo News",
        "url": "https://ca.news.yahoo.com/major-global-news-moments-october-164718493.html",
        "publishedAt": "2026-10-12T00:00:00Z",
        "label": "world",
        "tag": "real",
    },

    # ── Misinformation examples (kept for model demonstration) ────────────
    {"title": "SHOCK CLAIM: Cyclone Arnab was artificially created by HAARP weather weapon", "source": "Viral Post", "url": "#", "label": "misinformation", "tag": "fake"},
    {"title": "EXCLUSIVE: Odisha hid 50,000 cyclone deaths — insider leak exposes cover-up", "source": "Viral Post", "url": "#", "label": "misinformation", "tag": "fake"},
    {"title": "BOMBSHELL: Panama earthquake triggered by secret underground nuclear test", "source": "Viral Post", "url": "#", "label": "misinformation", "tag": "fake"},
    {"title": "BREAKING: Tibet quake was divine punishment; magnitude 10 to destroy China in 30 days", "source": "Viral Post", "url": "#", "label": "misinformation", "tag": "fake"},
    {"title": "SHOCKING: Secret nuclear strike launched — all governments hiding the truth", "source": "Viral Post", "url": "#", "label": "misinformation", "tag": "fake"},
    {"title": "EXPOSED: Iran war is staged — oil companies manufactured the Hormuz crisis", "source": "Viral Post", "url": "#", "label": "misinformation", "tag": "fake"},
    {"title": "URGENT: India's Election Commission secretly deleting millions of votes per whistleblower", "source": "Viral Post", "url": "#", "label": "misinformation", "tag": "fake"},
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