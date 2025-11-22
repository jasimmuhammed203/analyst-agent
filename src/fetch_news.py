import requests
import json

def fetch_ai_startup_news(api_key, max_articles=50):
    """
    Fetch AI startup news using the GNews API.
    """
    url = f"https://gnews.io/api/v4/search?q=AI+startup&token={api_key}&max={max_articles}"

    response = requests.get(url)
    data = response.json()

    articles = [
        {
            "title": a["title"],
            "description": a.get("description", ""),
            "content": a.get("content", ""),
            "url": a.get("url", ""),
            "published": a.get("publishedAt", ""),
            "source": a["source"]["name"]
        }
        for a in data.get("articles", [])
    ]

    # Save raw for debugging
    with open("data/raw.json", "w") as f:
        json.dump(articles, f, indent=2)

    return articles