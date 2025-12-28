📰 HeadLine Hub — Personalized News App
A fully deployed, multi-page personalized news aggregation platform built using Streamlit that delivers curated news based on user interests, reading behavior, saved articles, and preferred publishers.

🔗 Live App: https://newsflow-headlines.streamlit.app/
📂 Tech Stack: Python · Streamlit · NewsAPI · GitHub · Streamlit Cloud 

🚀 Overview
HeadLine Hub is a modern news application that goes beyond static headlines.
It dynamically adapts to user behavior and delivers a personalized “For You” feed, making news consumption smarter, relevant, and engaging.
The application demonstrates real-world engineering practices such as API integration, personalization logic, secure secrets handling, multi-page UI architecture, and cloud deployment.

✨ Key Features

🏠 Home Page
Displays top trending news articles
Clean, responsive card-based UI
Article metadata including publish time

🔍 Explore Page
Browse news by category, keyword, or country
Dynamic filters with real-time API fetching
Smooth browsing experience

📰 Publisher Gallery
Explore articles from specific publishers
Country-based publisher filtering
Intuitive dropdown selection

⭐ Bookmarks Page
Save articles for later reading
Persistent storage using JSON
Remove bookmarks instantly

🎯 “For You” — Personalized Feed
Curated articles based on:
User clicks on categories
Preferred publishers
Saved/bookmarked articles
Explainable recommendations

🧠 Personalization Logic
The “For You” feed uses implicit user behavior tracking, such as: Category interaction frequency, Publisher affinity, Bookmark patterns
Based on these signals, relevant search terms are derived and used to fetch personalized articles via NewsAPI.
Each recommendation includes a transparent explanation, improving trust and user experience.

🔐 Secure API Key Management
API keys are stored securely using Streamlit Secrets
No sensitive credentials are exposed in the repository
Production-ready configuration for cloud deployment

🛠️ Tech Stack and the Usage
Python: Core application logic
Streamlit: UI & multi-page framework
NewsAPI: Real-time news data
Git & GitHub: Version control
Streamlit Cloud: Deployment
HTML & CSS: Custom styling

🎯 Why This Project Matters
This project demonstrates:
Real-world API handling
Personalization without heavy ML
Clean UI/UX thinking
Secure deployment practices
End-to-end product ownership

📁 Project Structure
NEWS_APP/
│
├── Home.py
├── style.css
├── bookmarks.json
├── requirements.txt
├── utils.py
│
├── pages/
│   ├── For_You.py
│   ├── Explore.py
│   ├── Publisher_Gallery.py
│   ├── My_Bookmarks.py
│
├── .streamlit/
│   └── secrets.toml
└── README.md


🧪 Current Limitations 
-Uses NewsAPI free tier (rate-limited)
-No user authentication (single-session personalization)
-JSON-based local storage

🧪 Future Enhancements
-User login system
-ML-based recommendation engine
-Database integration (PostgreSQL / Firebase)
-User profile dashboards
-Dark mode & UI animations

👩‍💻 Author
-Rishika Rai
An Aspiring Software Engineer | Data Science & AI Enthusiast
# Built with curiosity, discipline, and lots of debugging.

If you found this project interesting, feel free to ⭐ the repository!


