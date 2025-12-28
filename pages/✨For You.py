import streamlit as st
import requests
import json
import os
from datetime import datetime, timezone

# ---------------- PAGE CONFIG ----------------
st.set_page_config(layout="wide")

def load_css():
    with open("style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

st.markdown("<h1 class='main-title'>For You</h1>", unsafe_allow_html=True)
st.write("A personalized feed curated just for you ✨")

# ---------------- USER PROFILE ----------------
if "user_profile" not in st.session_state:
    st.session_state.user_profile = {
        "category_clicks": {},
        "publisher_clicks": {},
        "search_terms": {},
        "saved_count": 0
    }

# ---------------- EXPLANATION LOGIC ----------------
def get_reason(article, profile):
    title = (article.get("title") or "").lower()
    description = (article.get("description") or "").lower()
    source_id = article.get("source", {}).get("id")

    if profile["search_terms"]:
        top_term = max(profile["search_terms"], key=profile["search_terms"].get)
        if top_term in title or top_term in description:
            return f"Because you searched for “{top_term}”"

    if source_id and source_id in profile["publisher_clicks"]:
        return "Based on publishers you read often"

    if profile["saved_count"] > 0:
        return "Based on articles you saved"

    return "Recommended for you"

# ---------------- BOOKMARK STORAGE ----------------
BOOKMARK_FILE = "bookmarks.json"

def load_bookmarks():
    if os.path.exists(BOOKMARK_FILE):
        with open(BOOKMARK_FILE, "r") as f:
            return json.load(f)
    return []

bookmarks = load_bookmarks()

# ---------------- TIME AGO ----------------
def time_ago(published_at):
    if not published_at:
        return ""
    published_time = datetime.fromisoformat(published_at.replace("Z", "+00:00"))
    now = datetime.now(timezone.utc)
    diff = now - published_time
    hours = diff.total_seconds() // 3600

    if hours < 1:
        return "Recently"
    elif hours < 24:
        return f"{int(hours)}h ago"
    else:
        return f"{int(hours//24)}d ago"

# ---------------- API ----------------
API_KEY = st.secrets["NEWS_API_KEY"]

@st.cache_data(ttl=1800)
def fetch_articles(query):
    url = (
        "https://newsapi.org/v2/everything?"
        f"q={query}&language=en&pageSize=10&apiKey={API_KEY}"
    )
    data = requests.get(url).json()
    return data.get("articles", []) if data.get("status") == "ok" else []

# ---------------- BUILD INTEREST TERMS ----------------
interest_terms = []

# From saved articles (strong signal)
for article in bookmarks:
    if article.get("title"):
        interest_terms.extend(article["title"].split()[:2])

# From categories
for cat, count in st.session_state.user_profile["category_clicks"].items():
    if count >= 2:
        interest_terms.append(cat)

interest_terms = list(set(interest_terms))[:5]

if not interest_terms:
    st.info("Interact with articles to personalize your feed ✨")
    st.stop()

# ---------------- FETCH PERSONALIZED ARTICLES ----------------
articles = []
for term in interest_terms:
    articles.extend(fetch_articles(term))

# Deduplicate
unique_articles = list({a["url"]: a for a in articles}.values())[:15]

# ---------------- DISPLAY ----------------
st.markdown("<div class='article-container'>", unsafe_allow_html=True)

if not unique_articles:
    st.markdown("<div class='empty-card'>No personalized articles yet.</div>", unsafe_allow_html=True)

for article in unique_articles:
    reason = get_reason(article, st.session_state.user_profile)

    st.markdown(
        f"""
        <div class="article-card">
            {'<img src="' + article['urlToImage'] + '">' if article.get('urlToImage') else ''}
            <h3><a href="{article['url']}" target="_blank">{article['title']}</a></h3>
            <p>{article.get('description','')}</p>
            <small class="time-ago">{time_ago(article.get("publishedAt"))}</small>
            <div class="why-text">🧠 {reason}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("</div>", unsafe_allow_html=True)
