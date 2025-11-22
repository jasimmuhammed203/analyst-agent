from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def dedupe_articles(articles, threshold=0.75):
    """
    Remove duplicate articles based on title+description similarity.
    """
    cleaned = []
    texts = []

    for article in articles:
        combined = f"{article['title']} {article['description']}".strip()

        if not texts:
            cleaned.append(article)
            texts.append(combined)
            continue

        vectorizer = TfidfVectorizer().fit_transform(texts + [combined])
        similarities = cosine_similarity(vectorizer[-1], vectorizer[:-1]).flatten()

        if max(similarities) < threshold:
            cleaned.append(article)
            texts.append(combined)

    return cleaned