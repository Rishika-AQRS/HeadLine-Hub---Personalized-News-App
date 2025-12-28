import streamlit as st
import requests
import json
import os
from datetime import datetime, timezone



# country names
COUNTRY_NAMES = {
    "ae": "United Arab Emirates",
    "ar": "Argentina",
    "at": "Austria",
    "au": "Australia",
    "be": "Belgium",
    "bg": "Bulgaria",
    "br": "Brazil",
    "ca": "Canada",
    "ch": "Switzerland",
    "cn": "China",
    "co": "Colombia",
    "cu": "Cuba",
    "cz": "Czech Republic",
    "de": "Germany",
    "eg": "Egypt",
    "fr": "France",
    "gb": "United Kingdom",
    "gr": "Greece",
    "hk": "Hong Kong",
    "hu": "Hungary",
    "id": "Indonesia",
    "ie": "Ireland",
    "il": "Israel",
    "in": "India",
    "it": "Italy",
    "jp": "Japan",
    "kr": "South Korea",
    "lt": "Lithuania",
    "lv": "Latvia",
    "ma": "Morocco",
    "mx": "Mexico",
    "my": "Malaysia",
    "ng": "Nigeria",
    "nl": "Netherlands",
    "no": "Norway",
    "nz": "New Zealand",
    "ph": "Philippines",
    "pl": "Poland",
    "pt": "Portugal",
    "ro": "Romania",
    "rs": "Serbia",
    "ru": "Russia",
    "sa": "Saudi Arabia",
    "se": "Sweden",
    "sg": "Singapore",
    "si": "Slovenia",
    "sk": "Slovakia",
    "th": "Thailand",
    "tr": "Turkey",
    "tw": "Taiwan",
    "ua": "Ukraine",
    "us": "United States",
    "ve": "Venezuela",
    "za": "South Africa"
}


st.set_page_config(layout="wide")

def load_css():
    with open("style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

st.markdown("<h1 class='main-title'>Publisher Space</h1>", unsafe_allow_html=True)
st.write("Choose your favorite publishers and explore their latest headlines 📰")

# ---------------- USER PROFILE (FOR YOU DATA) ----------------
if "user_profile" not in st.session_state:
    st.session_state.user_profile = {
        "category_clicks": {},
        "publisher_clicks": {},
        "search_terms": {},
        "saved_count": 0
    }

def track_publisher(source_id):
    st.session_state.user_profile["publisher_clicks"][source_id] = (
        st.session_state.user_profile["publisher_clicks"].get(source_id, 0) + 1
    )

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

# ---------------- BOOKMARK STORAGE ----------------
BOOKMARK_FILE = "bookmarks.json"

def load_bookmarks():
    if os.path.exists(BOOKMARK_FILE):
        with open(BOOKMARK_FILE, "r") as f:
            return json.load(f)
    return []

def save_bookmarks(data):
    with open(BOOKMARK_FILE, "w") as f:
        json.dump(data, f, indent=4)

if "bookmarks" not in st.session_state:
    st.session_state.bookmarks = load_bookmarks()

def article_exists(article):
    return any(a["url"] == article["url"] for a in st.session_state.bookmarks)

# ---------------- API ----------------
API_KEY = st.secrets["NEWS_API_KEY"]

@st.cache_data(ttl=86400)
def fetch_sources():
    url = f"https://newsapi.org/v2/sources?apiKey={API_KEY}"
    try:
        data = requests.get(url).json()
        return data["sources"] if data.get("status") == "ok" else []
    except:
        return []

@st.cache_data(ttl=1800)
def fetch_publisher_news(source_id):
    url = (
        "https://newsapi.org/v2/top-headlines?"
        f"sources={source_id}&"
        "pageSize=15&"
        f"apiKey={API_KEY}"
    )
    try:
        data = requests.get(url).json()
        return data.get("articles", []) if data.get("status") == "ok" else []
    except:
        return []

# ---------------- COUNTRY FILTER ----------------
sources = fetch_sources()

countries = sorted(set(s["country"] for s in sources))
selected_country = st.selectbox(
    "Filter by country",
    ["all"] + countries,
    format_func=lambda c: (
        "All Countries"
        if c == "all"
        else COUNTRY_NAMES.get(c, c.upper())
    )
)

filtered_sources = [
    s for s in sources
    if selected_country == "all" or s["country"] == selected_country
]

if not filtered_sources:
    st.info("No publishers available for this country.")
    st.stop()

# ---------------- PUBLISHER SELECT (NO DEFAULT) ----------------
publisher_options = ["__none__"] + filtered_sources

publisher = st.selectbox(
    "Select Publisher",
    options=publisher_options,
    format_func=lambda s: "— Select a publisher —"
    if s == "__none__"
    else f"{s['name']} ({s['country'].upper()})"
)

if publisher == "__none__":
    st.info("Please select a publisher to view headlines.")
    st.stop()

# ---------------- FETCH ARTICLES ----------------
source_id = publisher["id"]
track_publisher(source_id)

st.caption(f"Browsing publishers from **{publisher['country'].upper()}**")

articles = fetch_publisher_news(source_id)

st.markdown("<div class='article-container'>", unsafe_allow_html=True)

if not articles:
    st.markdown(
        "<div class='empty-card'>No recent articles available from this publisher.</div>",
        unsafe_allow_html=True
    )

for i, article in enumerate(articles):
    st.markdown(
        f"""
        <div class="article-card">
            {'<img src="'+article['urlToImage']+'">' if article.get('urlToImage') else ''}
            <h3><a href="{article['url']}" target="_blank">{article['title']}</a></h3>
            <p>{article.get('description','')}</p>
            <small class="time-ago">{time_ago(article.get("publishedAt"))}</small>
        """,
        unsafe_allow_html=True
    )

    if not article_exists(article):
        if st.button("Save", key=f"p_{source_id}_{i}"):
            st.session_state.bookmarks.append(article)
            save_bookmarks(st.session_state.bookmarks)
            st.session_state.user_profile["saved_count"] += 1
            st.success("Saved!")
    else:
        st.caption("✔ Bookmarked")

    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)
