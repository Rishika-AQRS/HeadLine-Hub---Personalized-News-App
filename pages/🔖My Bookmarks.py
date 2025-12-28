import streamlit as st
import json
import os

st.set_page_config(layout="wide")

def load_css():
    with open("style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

BOOKMARK_FILE = "bookmarks.json"

# ---------------- USER PROFILE (FOR YOU DATA) ----------------
if "user_profile" not in st.session_state:
    st.session_state.user_profile = {
        "category_clicks": {},
        "publisher_clicks": {},
        "search_terms": {},
        "saved_count": 0
    }

def load_bookmarks():
    if os.path.exists(BOOKMARK_FILE):
        with open(BOOKMARK_FILE, "r") as f:
            return json.load(f)
    return []

def save_bookmarks(bookmarks):
    with open(BOOKMARK_FILE, "w") as f:
        json.dump(bookmarks, f, indent=4)

st.markdown("<h1 class='main-title'>Bookmarks</h1>", unsafe_allow_html=True)
st.write("Your saved articles.")

bookmarks = load_bookmarks()

if not bookmarks:
    st.markdown(
        "<div class='empty-card'>No bookmarks saved yet.</div>",
        unsafe_allow_html=True
    )
else:
    st.markdown("<div class='article-container'>", unsafe_allow_html=True)

    for idx, article in enumerate(bookmarks):
        st.markdown(
            f"""
            <div class="article-card">
                {'<img src="' + article['urlToImage'] + '">' if article.get('urlToImage') else ''}
                <h3><a href="{article['url']}" target="_blank">{article['title']}</a></h3>
                <p>{article.get('description','')}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        if st.button("❌ Remove", key=f"rm_{idx}"):
            bookmarks.pop(idx)
            save_bookmarks(bookmarks)
            st.session_state.user_profile["saved_count"] = max(
                0, st.session_state.user_profile["saved_count"] - 1
            )
            

    st.markdown("</div>", unsafe_allow_html=True)
