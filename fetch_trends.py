import feedparser
import re
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_trending_news(num_articles=10, timeout=10):
    """
    Fetch trending news from Google News RSS feed with error handling.
    
    Args:
        num_articles (int): Number of articles to fetch (default: 10)
        timeout (int): Request timeout in seconds (default: 10)
    
    Returns:
        list: List of dictionaries containing news articles
    """
    url = "https://news.google.com/rss"
    trending_news = []
    
    try:
        # Parse the RSS feed with timeout
        feed = feedparser.parse(url, timeout=timeout)
        
        # Check if feed parsing was successful
        if not feed.entries:
            logger.warning("No entries found in Google News feed")
            return trending_news
        
        # Process top articles
        for entry in feed.entries[:num_articles]:
            try:
                title = entry.get("title", "No Title")
                link = entry.get("link", "#")
                
                # Extract image from summary (Google News embeds images in summary)
                summary = entry.get("summary", "")
                thumbnail = extract_thumbnail(summary)
                
                # Extract published date
                published = entry.get("published", "Unknown date")
                
                news_item = {
                    "title": title,
                    "link": link,
                    "thumbnail": thumbnail,
                    "published": published
                }
                
                trending_news.append(news_item)
                logger.info(f"Fetched article: {title[:50]}...")
                
            except Exception as e:
                logger.error(f"Error processing entry: {str(e)}")
                continue
        
        logger.info(f"Successfully fetched {len(trending_news)} articles")
        return trending_news
    
    except Exception as e:
        logger.error(f"Error fetching Google News feed: {str(e)}")
        return trending_news

def extract_thumbnail(summary):
    """
    Extracts the first image URL from the summary (if available).
    
    Args:
        summary (str): HTML summary containing potential image tags
    
    Returns:
        str: Image URL or placeholder URL if not found
    """
    try:
        if not summary:
            return "https://via.placeholder.com/150"
        
        # Improved regex to handle various HTML attributes
        match = re.search(r'<img[^>]+src=["\']([^"\']+)["\']', summary)
        
        if match:
            image_url = match.group(1)
            logger.debug(f"Extracted thumbnail: {image_url}")
            return image_url
        else:
            logger.debug("No image found in summary, using placeholder")
            return "https://via.placeholder.com/150"
            
    except Exception as e:
        logger.error(f"Error extracting thumbnail: {str(e)}")
        return "https://via.placeholder.com/150"

def search_news(news_list, query):
    """
    Search news articles by query string.
    
    Args:
        news_list (list): List of news articles
        query (str): Search query
    
    Returns:
        list: Filtered list of articles matching the query
    """
    if not query:
        return news_list
    
    query_lower = query.lower()
    return [
        article for article in news_list
        if query_lower in article.get("title", "").lower()
    ]
