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

# ---------------- USER PROFILE (FOR YOU PAGE DATA) ----------------
if "user_profile" not in st.session_state:
    st.session_state.user_profile = {
        "category_clicks": {},
        "publisher_clicks": {},
        "saved_count": 0
    }

def track_category(cat):
    st.session_state.user_profile["category_clicks"][cat] = (
        st.session_state.user_profile["category_clicks"].get(cat, 0) + 1
    )

def track_publisher(source_id):
    st.session_state.user_profile["publisher_clicks"][source_id] = (
        st.session_state.user_profile["publisher_clicks"].get(source_id, 0) + 1
    )

# ---------------- BOOKMARK STORAGE ----------------
BOOKMARK_FILE = "bookmarks.json"

def load_bookmarks():
    if os.path.exists(BOOKMARK_FILE):
        with open(BOOKMARK_FILE, "r") as f:
            return json.load(f)
    return []

def save_bookmarks(bookmarks):
    with open(BOOKMARK_FILE, "w") as f:
        json.dump(bookmarks, f, indent=4)

if "bookmarks" not in st.session_state:
    st.session_state.bookmarks = load_bookmarks()

def article_exists(article):
    return any(a["url"] == article["url"] for a in st.session_state.bookmarks)

# ---------------- SESSION STATE ----------------
if "category" not in st.session_state:
    st.session_state.category = "general"

# ---------------- TITLE ----------------
st.markdown("<h1 class='main-title'>HeadLine Hub</h1>", unsafe_allow_html=True)
st.write("Your One-Stop Destination for Today's Top News!")
st.write("---")

# ---------------- CATEGORY BUTTONS ----------------
st.subheader("Select a category to explore today’s headlines.")

categories = [
    "general", "technology", "business",
    "sports", "health", "entertainment", "science"
]

row1 = st.columns(4, gap="small")
row2 = st.columns(3, gap="small")

for i, cat in enumerate(categories[:4]):
    with row1[i]:
        if st.button(cat.capitalize(), key=f"cat_{cat}", use_container_width=True):
            st.session_state.category = cat
            track_category(cat)

for i, cat in enumerate(categories[4:]):
    with row2[i]:
        if st.button(cat.capitalize(), key=f"cat2_{cat}", use_container_width=True):
            st.session_state.category = cat
            track_category(cat)

# ---------------- TIME AGO ----------------
def time_ago(published_at):
    if not published_at:
        return ""
    published_time = datetime.fromisoformat(published_at.replace("Z", "+00:00"))
    now = datetime.now(timezone.utc)
    diff = now - published_time
    seconds = diff.total_seconds()

    if seconds < 60:
        return "Just now"
    elif seconds < 3600:
        return f"{int(seconds//60)} minutes ago"
    elif seconds < 86400:
        return f"{int(seconds//3600)} hours ago"
    else:
        days = int(seconds // 86400)
        return f"{days} day{'s' if days > 1 else ''} ago"

# ---------------- SOURCES ----------------
SOURCES = {
    "bbc-news": "BBC News",
    "cnn": "CNN",
    "nbc-news": "NBC News",
    "fox-news": "Fox News",
    "abc-news": "ABC News"
}

API_KEY = st.secrets["NEWS_API_KEY"]
@st.cache_data(ttl=3600)
def fetch_articles(source_id=None, category=None):
    base_url = "https://newsapi.org/v2/top-headlines"

    if source_id:
        url = f"{base_url}?sources={source_id}&pageSize=10&apiKey={API_KEY}"
    elif category and category != "general":
        url = f"{base_url}?country=us&category={category}&pageSize=10&apiKey={API_KEY}"
    else:
        url = f"{base_url}?country=us&pageSize=10&apiKey={API_KEY}"

    try:
        data = requests.get(url).json()
        return data.get("articles", []) if data.get("status") == "ok" else []
    except:
        return []

# ---------------- DISPLAY ----------------
st.subheader(f"{st.session_state.category.capitalize()} Headlines")
st.markdown('<div class="article-container">', unsafe_allow_html=True)

articles = (
    sum([fetch_articles(source_id=s)[:3] for s in SOURCES], [])
    if st.session_state.category == "general"
    else fetch_articles(category=st.session_state.category)
)

if not articles:
    st.markdown("<div class='empty-card'>Sorry, no news available at the moment.</div>", unsafe_allow_html=True)

for idx, article in enumerate(articles):
    source_id = article.get("source", {}).get("id")
    if source_id:
        track_publisher(source_id)

    st.markdown(
        f"""
        <div class="article-card">
            {'<img src="' + article['urlToImage'] + '">' if article.get('urlToImage') else ''}
            <h3>
                <a href="{article['url']}" target="_blank">{article['title']}</a>
            </h3>
            <p>{article.get('description','')}</p>
            <small>{time_ago(article.get("publishedAt"))}</small>
        </div>
        """,
        unsafe_allow_html=True
    )

    if not article_exists(article):
        if st.button("Save", key=f"save_{idx}"):
            st.session_state.bookmarks.append(article)
            save_bookmarks(st.session_state.bookmarks)
            st.session_state.user_profile["saved_count"] += 1
            st.success("Saved to bookmarks!")
    else:
        st.caption("✔ Already bookmarked")

st.markdown("</div>", unsafe_allow_html=True)
