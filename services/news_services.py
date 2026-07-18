import streamlit as st
import os
import requests
from dotenv import load_dotenv
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

load_dotenv()

API_KEY = os.getenv("NEWS_API_KEY")

@st.cache_data(ttl=300)
def get_company_news(company_name):

    company_name = (
        company_name.replace("Limited", "")
        .replace("Ltd.", "")
        .replace("Ltd", "")
        .strip()
    )

    url = "https://newsapi.org/v2/everything"

    params = {
        "q": company_name,
        "searchIn": "title,description",
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": 5,
        "apiKey": API_KEY,
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        return []

    data = response.json()

    articles = []

    for article in data.get("articles", []):

        articles.append({
            "title": article.get("title"),
            "description": article.get("description"),
            "url": article.get("url"),
            "source": article.get("source", {}).get("name"),
            "publishedAt": article.get("publishedAt"),
        })

    return articles