import streamlit as st
import requests
# ---------------- API CALL ----------------
API_KEY = "4bc51cffce154d918aec372fa73967db"

# ---------------- CACHE API CALLS ----------------
@st.cache_data(ttl=3600)
def fetch_articles(source_id):
    base_url = "https://newsapi.org/v2/top-headlines"
    
    if source_id:
        url = f"{base_url}?sources={source_id}&apiKey={API_KEY}"
    else:
        url = f"{base_url}?country=us&category={category}&apiKey={API_KEY}"

    try:
        response = requests.get(url)
        data = response.json()
        if data.get("status") == "ok":
            return data.get("articles", [])
        else:
            return []
    except:
        return []