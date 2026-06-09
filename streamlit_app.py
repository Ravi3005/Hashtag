import streamlit as st
import requests
import feedparser
import re
from datetime import datetime
import pytz
import time
from bs4 import BeautifulSoup

# Page configuration
st.set_page_config(
    page_title="📰 Trending News Dashboard",
    page_icon="📰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom styling
st.markdown("""
    <style>
    .news-card {
        padding: 20px;
        border-radius: 10px;
        background-color: #f0f2f6;
        margin-bottom: 15px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        transition: transform 0.2s;
    }
    .news-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    .news-title {
        font-size: 18px;
        font-weight: bold;
        color: #1f77b4;
        margin-bottom: 10px;
    }
    .news-link {
        color: #0066cc;
        text-decoration: none;
        font-weight: 500;
    }
    .news-link:hover {
        text-decoration: underline;
    }
    </style>
""", unsafe_allow_html=True)

# Get Indian Standard Time (IST)
ist = pytz.timezone('Asia/Kolkata')
current_time_ist = datetime.now(ist)

# Title and description
st.title("📰 Trending News Dashboard")
st.markdown("Stay updated with the latest trending news from around the world!")

# Sidebar configuration
with st.sidebar:
    st.header("⚙️ Settings")
    st.caption(f"🕐 Current Time (IST): {current_time_ist.strftime('%H:%M:%S')}")
    
    # Display options
    num_articles = st.slider(
        "Number of articles to display",
        min_value=5,
        max_value=50,
        value=10,
        step=5
    )
    
    # Refresh settings
    st.subheader("Refresh Settings")
    auto_refresh = st.checkbox("Auto-refresh (every 5 minutes)", value=False)
    if st.button("🔄 Refresh Now", use_container_width=True):
        st.cache_data.clear()
        st.rerun()
    
    st.divider()
    st.info("💡 This app fetches news directly from Google News RSS feed.")

# Main content area
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("📊 Source", "Google News")
with col2:
    st.metric("⏰ Last Updated (IST)", current_time_ist.strftime("%H:%M:%S"))
with col3:
    st.metric("📰 Articles", f"~{num_articles}")

st.divider()

# Fetch trending news directly from Google News
@st.cache_data(ttl=300)  # Cache for 5 minutes
def fetch_trending_news(limit=10):
    """Fetch trending news directly from Google News RSS feed"""
    try:
        url = "https://news.google.com/rss"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, timeout=10, headers=headers)
        response.raise_for_status()
        
        # Parse the RSS feed
        feed = feedparser.parse(response.content)
        
        if not feed.entries:
            return []
        
        # Process articles
        news_articles = []
        for entry in feed.entries[:limit]:
            try:
                title = entry.get("title", "No Title")
                link = entry.get("link", "#")
                summary = entry.get("summary", "")
                published = entry.get("published", "Unknown date")
                
                # Extract source
                source = extract_source(title, summary)
                
                # Extract thumbnail from summary
                thumbnail = extract_thumbnail_from_html(summary)
                
                news_item = {
                    "title": title,
                    "link": link,
                    "thumbnail": thumbnail,
                    "published": published,
                    "source": source
                }
                news_articles.append(news_item)
            except Exception as e:
                continue
        
        return news_articles
    
    except requests.exceptions.Timeout:
        st.error("❌ Request timed out. Please try again later.")
        return []
    except requests.exceptions.RequestException as e:
        st.error(f"❌ Error fetching news: {str(e)}")
        return []
    except Exception as e:
        st.error(f"❌ Unexpected error: {str(e)}")
        return []

def extract_source(title, summary):
    """Extract news source from title or summary"""
    try:
        # Common news sources
        sources = [
            'BBC', 'CNN', 'Reuters', 'AP News', 'The Times', 'The Guardian',
            'The New York Times', 'Washington Post', 'Bloomberg', 'CNBC',
            'NBC', 'ABC', 'CBS', 'Fox', 'The Hill', 'Axios', 'Politico',
            'India Times', 'NDTV', 'The Hindu', 'Economic Times', 'India Today'
        ]
        
        # Search in title
        for source in sources:
            if source.lower() in title.lower():
                return source
        
        # Search in summary
        for source in sources:
            if source.lower() in summary.lower():
                return source
        
        # Default
        return "News"
    except:
        return "News"

def extract_thumbnail_from_html(html_content):
    """Extract image URL from HTML content using BeautifulSoup"""
    try:
        if not html_content:
            return None
        
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Find all img tags
        img_tags = soup.find_all('img')
        
        for img in img_tags:
            src = img.get('src')
            data_src = img.get('data-src')
            
            # Try src first
            if src and is_valid_image_url(src):
                return src
            
            # Try data-src for lazy loaded images
            if data_src and is_valid_image_url(data_src):
                return data_src
        
        # Look for picture tag with source
        picture = soup.find('picture')
        if picture:
            img = picture.find('img')
            if img:
                src = img.get('src')
                if src and is_valid_image_url(src):
                    return src
        
        return None
    except:
        return None

def is_valid_image_url(url):
    """Check if URL is a valid image URL"""
    try:
        if not url:
            return False
        
        # Check if URL starts with http or //
        if not url.startswith(('http://', 'https://', '//')):
            return False
        
        # Check for image extensions or known CDN domains
        image_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg')
        url_lower = url.lower()
        
        # Check image extensions
        if any(url_lower.endswith(ext) for ext in image_extensions):
            return True
        
        # Check for common image CDNs
        if any(cdn in url_lower for cdn in ['lh3.googleusercontent.com', 'cdn', 'images', 'img', 'static', 'media']):
            return True
        
        # Query params likely indicate image service
        if '?' in url:
            return True
        
        return False
    except:
        return False

def convert_to_ist(date_string):
    """Convert article published date to IST format"""
    try:
        from email.utils import parsedate_to_datetime
        dt = parsedate_to_datetime(date_string)
        
        # Convert to IST
        if dt.tzinfo is None:
            dt = pytz.UTC.localize(dt)
        ist_time = dt.astimezone(ist)
        return ist_time.strftime("%d %b %Y, %H:%M:%S IST")
    except:
        return date_string

# Search and filter options
st.subheader("🔍 Search & Filter")
search_query = st.text_input(
    "Search articles",
    placeholder="Enter keywords to search...",
    help="Filter articles by keywords in the title"
)

# Fetch data
news_articles = fetch_trending_news(limit=50)

if not news_articles:
    st.warning("📭 No articles found. Please try again later.")
else:
    # Filter by search query
    if search_query:
        filtered_articles = [
            article for article in news_articles
            if search_query.lower() in article.get("title", "").lower()
        ]
        st.info(f"Found {len(filtered_articles)} articles matching '{search_query}'")
    else:
        filtered_articles = news_articles
    
    # Limit to selected number
    displayed_articles = filtered_articles[:num_articles]
    
    # Display articles
    if not displayed_articles:
        st.warning("🔎 No articles match your search. Try different keywords.")
    else:
        for idx, article in enumerate(displayed_articles, 1):
            with st.container():
                col1, col2 = st.columns([1, 3])
                
                # Thumbnail or placeholder
                with col1:
                    thumbnail_url = article.get("thumbnail")
                    
                    if thumbnail_url:
                        try:
                            st.image(
                                thumbnail_url,
                                use_column_width=True,
                                caption=f"Article {idx}"
                            )
                        except:
                            # Fallback if image fails to load
                            st.markdown(f"""
                            <div style="width:100%; height:150px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius:8px; display:flex; align-items:center; justify-content:center; color:white; font-weight:bold;">
                            📰 {article.get('source', 'News')}
                            </div>
                            """, unsafe_allow_html=True)
                    else:
                        # Gradient placeholder with source
                        st.markdown(f"""
                        <div style="width:100%; height:150px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius:8px; display:flex; align-items:center; justify-content:center; color:white; font-weight:bold; text-align:center;">
                        📰 {article.get('source', 'News')}<br>Article {idx}
                        </div>
                        """, unsafe_allow_html=True)
                
                # Article details
                with col2:
                    st.markdown(f"### {article.get('title', 'No Title')}")
                    
                    # Source badge
                    source = article.get('source', 'News')
                    st.caption(f"📍 Source: {source}")
                    
                    # Published date in IST
                    published_ist = convert_to_ist(article.get("published", "Unknown date"))
                    st.caption(f"📅 Published: {published_ist}")
                    
                    # Read more button
                    link = article.get("link", "#")
                    if link != "#":
                        st.markdown(
                            f"[📖 Read Full Article]({link})",
                            unsafe_allow_html=True
                        )
                    else:
                        st.warning("Link not available")
                    
                    st.caption(f"Article #{idx}")
                
                st.divider()

# Footer
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    st.caption("📱 Built with Streamlit")
with col2:
    st.caption("🔗 Powered by Google News RSS")
with col3:
    st.caption("🇮🇳 IST - Indian Standard Time")

# Auto-refresh functionality
if auto_refresh:
    time.sleep(300)  # Wait 5 minutes
    st.rerun()
