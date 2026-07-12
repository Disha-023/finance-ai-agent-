import feedparser
from urllib.parse import quote


def get_company_news(company_name):

    company_name = (
        company_name.replace("Limited", "")
        .replace("Ltd.", "")
        .replace("Ltd", "")
        .strip()
    )

    query = quote(company_name)

    url = f"https://news.google.com/rss/search?q={query}"

    feed = feedparser.parse(url)

    articles = []

    for entry in feed.entries[:5]:

        articles.append({
            "title": entry.title,
            "description": entry.summary,
            "url": entry.link
        })

    return articles