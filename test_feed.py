import feedparser

url = "https://news.google.com/rss"
feed = feedparser.parse(url, timeout=10)
print(f"Feed status: {feed.status}")
print(f"Entries found: {len(feed.entries)}")
if feed.entries:
    print(f"First entry: {feed.entries[0].get('title', 'No title')}")
else:
    print("No entries found in feed")
