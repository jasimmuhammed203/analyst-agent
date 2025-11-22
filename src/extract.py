import os
import json
import re
from groq import Groq

def extract_json(article_text):
    """
    Extract structured JSON using Groq Llama-3.1 model.
    Automatically cleans multiple JSON objects, markdown blocks,
    and picks the FIRST valid JSON.
    """

    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise Exception("GROQ_API_KEY is missing. Check your .env file.")

    client = Groq(api_key=api_key)

    prompt = f"""
    Extract structured fields from this news article.
    Output ONLY ONE valid JSON object using this schema:
    {{
        "company_name": "",
        "category": "",
        "sentiment_score": 0,
        "is_funding_news": false
    }}

    Do not output multiple JSON objects.
    Do not include explanations.

    ARTICLE:
    {article_text}
    """

    try:
        resp = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2
        )

        text = resp.choices[0].message.content or ""

        # Debug
        print("RAW MODEL OUTPUT:", repr(text[:200]))

        # Remove markdown
        text = re.sub(r"```json|```", "", text).strip()

        # Extract ALL json objects
        matches = re.findall(r"\{.*?\}", text, re.DOTALL)

        if not matches:
            print("No JSON found")
            return None

        # Take ONLY the first JSON object
        first_json = matches[0]

        # Parse it
        return json.loads(first_json)

    except Exception as e:
        print("Extraction failed:", e)
        return None