import feedparser
import requests

url = "https://news.google.com/rss"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

try:
    response = requests.get(url, timeout=10, headers=headers)
    response.raise_for_status()
    feed = feedparser.parse(response.content)
    print(f"Feed status: {response.status_code}")
    print(f"Entries found: {len(feed.entries)}")
    if feed.entries:
        print(f"First entry: {feed.entries[0].get('title', 'No title')}")
    else:
        print("No entries found in feed")
except Exception as e:
    print(f"Error: {type(e).__name__}: {str(e)}")
