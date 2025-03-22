import feedparser

def get_trending_news():
    url = "https://news.google.com/rss"
    feed = feedparser.parse(url)

    trending_news = []
    
    for entry in feed.entries[:10]:  # Get top 10 trending news
        title = entry.get("title", "No Title")
        link = entry.get("link", "#")
        
        # Extract image (Google News often embeds images in summary)
        summary = entry.get("summary", "")
        thumbnail = extract_thumbnail(summary)

        trending_news.append({
            "title": title,
            "link": link,
            "thumbnail": thumbnail
        })
    
    return trending_news

def extract_thumbnail(summary):
    """ Extracts the first image URL from the summary (if available). """
    import re
    match = re.search(r'<img.*?src="(.*?)"', summary)
    return match.group(1) if match else "https://via.placeholder.com/150"

