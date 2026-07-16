# ----------------------------------------------------
# NEWS SERVICE MODULE
#
# Purpose:
# Fetch recent company-related news articles using
# Google News RSS feed.
#
# Status:
# Temporarily disabled for testing and debugging.
#
# Future Enhancement:
# Integrate live news analysis using LLMs to generate
# market sentiment and investment insights.
# ----------------------------------------------------


import feedparser
from urllib.parse import quote


def get_company_news(company_name):

    # Remove common company suffixes to improve news search accuracy
    company_name = (
        company_name.replace("Limited", "")
        .replace("Ltd.", "")
        .replace("Ltd", "")
        .strip()
    )

    # Convert company name into URL-safe format
    query = quote(company_name)

    # Google News RSS Search URL 
    url = f"https://news.google.com/rss/search?q={query}"

    # Fetch and parse RSS Feed
    feed = feedparser.parse(url)

    articles = []

    for entry in feed.entries[:5]:

        articles.append({
            "title": entry.title,
            "description": entry.summary,
            "url": entry.link
        })

    return articles