import streamlit as st
import requests
import json
import os
from datetime import datetime, timezone

st.set_page_config(layout="wide")

def load_css():
    with open("style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# ---------------- USER PROFILE (FOR YOU DATA) ----------------
if "user_profile" not in st.session_state:
    st.session_state.user_profile = {}

st.session_state.user_profile.setdefault("category_clicks", {})
st.session_state.user_profile.setdefault("publisher_clicks", {})
st.session_state.user_profile.setdefault("search_terms", {})
st.session_state.user_profile.setdefault("saved_count", 0)

def track_search(term):
    st.session_state.user_profile["search_terms"][term.lower()] = (
        st.session_state.user_profile["search_terms"].get(term.lower(), 0) + 1
    )

def track_publisher(source_id):
    if source_id:
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

# ---------------- API ----------------
API_KEY = st.secrets["NEWS_API_KEY"]
@st.cache_data(ttl=900)
def search_articles(query):
    url = (
        "https://newsapi.org/v2/everything?"
        f"q={query}&"
        "language=en&"
        "pageSize=20&"
        f"apiKey={API_KEY}"
    )
    try:
        data = requests.get(url).json()
        return data.get("articles", []) if data.get("status") == "ok" else []
    except:
        return []

# ---------------- UI ----------------
st.markdown("<h1 class='main-title'>Explore</h1>", unsafe_allow_html=True)
st.write("Find Articles Across All Sources.")

query = st.text_input("Search for news", placeholder="AI, elections, health...")

if query and len(query) >= 3:
    track_search(query)

    articles = search_articles(query)

    st.markdown("<div class='article-container'>", unsafe_allow_html=True)

    if not articles:
        st.markdown("<div class='empty-card'>No articles found.</div>", unsafe_allow_html=True)

    for idx, article in enumerate(articles):
        source_id = article.get("source", {}).get("id")
        track_publisher(source_id)

        st.markdown(
            f"""
            <div class="article-card">
                {'<img src="' + article['urlToImage'] + '">' if article.get('urlToImage') else ''}
                <h3><a href="{article['url']}" target="_blank">{article['title']}</a></h3>
                <p>{article.get('description','')}</p>
                <small>{time_ago(article.get("publishedAt"))}</small>
            </div>
            """,
            unsafe_allow_html=True
        )

        if not article_exists(article):
            if st.button("Save", key=f"s_{idx}"):
                st.session_state.bookmarks.append(article)
                save_bookmarks(st.session_state.bookmarks)
                st.session_state.user_profile["saved_count"] += 1
                st.success("Saved!")
        else:
            st.caption("✔ Already bookmarked")

    st.markdown("</div>", unsafe_allow_html=True)

elif query:
    st.info("Type at least 3 characters to search.")
