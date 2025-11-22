import os
from dotenv import load_dotenv

from src.fetch_news import fetch_ai_startup_news
from src.dedupe import dedupe_articles
from src.extract import extract_json
from src.hype_filter import is_high_information
from src.save import save_to_csv

load_dotenv()

def run_pipeline():
    gnews_key = os.getenv("GNEWS_API_KEY")
    if not gnews_key:
        raise Exception("Missing GNEWS_API_KEY in .env")

    print("\n📡 Fetching news...")
    articles = fetch_ai_startup_news(gnews_key)

    print(f"Fetched {len(articles)} articles.")

    print("\n🧹 Removing duplicates...")
    deduped = dedupe_articles(articles)
    print(f"{len(deduped)} unique articles remain.")

    print("\n🧠 Extracting structured JSON from each article...")

    results = []
    for a in deduped:
        text = f"{a['title']} {a['description']} {a['content']}"
        
        if not is_high_information(text):
            continue

        extracted = extract_json(text)
        if extracted:
            extracted["source"] = a["source"]
            extracted["published"] = a["published"]
            extracted["url"] = a["url"]
            results.append(extracted)

    print(f"\n💾 Saving {len(results)} final articles to CSV...")
    save_to_csv(results)

    print("\n✅ Done! Output saved to output/ai_startup_news.csv\n")


if __name__ == "__main__":
    run_pipeline()