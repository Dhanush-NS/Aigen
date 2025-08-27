# backend/mcp_clients/fallbacks.py
import requests

def fallback_search(query: str, max_results: int = 5):
    # Call DuckDuckGo API (or fake results for dev)
    url = f"https://api.duckduckgo.com/?q={query}&format=json"
    r = requests.get(url)
    data = r.json()
    results = []
    for topic in data.get("RelatedTopics", [])[:max_results]:
        results.append({
            "title": topic.get("Text", "No title"),
            "href": topic.get("FirstURL", "#"),
            "body": topic.get("Text", "")
        })
    return results

def fallback_image_generation(prompt: str):
    # Pollinations API (returns an image URL)
    image_url = f"https://image.pollinations.ai/prompt/{prompt.replace(' ', '%20')}"
    return {"image_url": image_url, "metadata": {}}
