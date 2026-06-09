import streamlit as st
import requests
from datetime import datetime
import time

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

# Title and description
st.title("📰 Trending News Dashboard")
st.markdown("Stay updated with the latest trending news from around the world!")

# Sidebar configuration
with st.sidebar:
    st.header("⚙️ Settings")
    
    # API server configuration
    api_host = st.text_input(
        "API Server Host",
        value="localhost",
        help="Hostname of the Flask API server"
    )
    api_port = st.number_input(
        "API Server Port",
        value=5000,
        min_value=1,
        max_value=65535,
        help="Port of the Flask API server"
    )
    
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
        st.rerun()
    
    st.divider()
    st.info("💡 The API server must be running at the configured address for this to work.")

# Main content area
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("📊 Source", "Google News")
with col2:
    st.metric("⏰ Last Updated", datetime.now().strftime("%H:%M:%S"))
with col3:
    st.metric("📰 Articles", f"~{num_articles}")

st.divider()

# Fetch trending news
@st.cache_data(ttl=300)  # Cache for 5 minutes
def fetch_trending_news(host, port):
    """Fetch trending news from the Flask API"""
    try:
        url = f"http://{host}:{port}/trending"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data.get("trending_news", [])
    except requests.exceptions.ConnectionError:
        st.error(f"❌ Cannot connect to API server at {host}:{port}")
        st.info("Make sure the Flask server is running: `python app.py`")
        return []
    except requests.exceptions.Timeout:
        st.error("❌ API request timed out. The server might be slow.")
        return []
    except requests.exceptions.RequestException as e:
        st.error(f"❌ Error fetching news: {str(e)}")
        return []
    except Exception as e:
        st.error(f"❌ Unexpected error: {str(e)}")
        return []

# Search and filter options
st.subheader("🔍 Search & Filter")
search_query = st.text_input(
    "Search articles",
    placeholder="Enter keywords to search...",
    help="Filter articles by keywords in the title"
)

# Fetch data
news_articles = fetch_trending_news(api_host, api_port)

if not news_articles:
    st.warning("📭 No articles found. Please check your API server configuration.")
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
                
                # Thumbnail
                with col1:
                    try:
                        st.image(
                            article.get("thumbnail", "https://via.placeholder.com/150"),
                            use_column_width=True,
                            caption=f"Article {idx}"
                        )
                    except Exception as e:
                        st.error(f"Could not load image: {str(e)}")
                        st.image("https://via.placeholder.com/150", use_column_width=True)
                
                # Article details
                with col2:
                    st.markdown(f"### {article.get('title', 'No Title')}")
                    
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
    st.caption("🚀 Real-time trending news")

# Auto-refresh functionality
if auto_refresh:
    import time
    time.sleep(300)  # Wait 5 minutes
    st.rerun()
