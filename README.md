# 📰 Trending News Dashboard

A modern, real-time trending news aggregator built with Flask backend and Streamlit frontend. Fetches the latest trending news from Google News RSS feed and displays them in an interactive dashboard.

## ✨ Features

- **Real-time News Fetching**: Automatically fetches trending news from Google News RSS
- **Interactive Dashboard**: Beautiful Streamlit UI with search and filtering capabilities
- **REST API**: Flask backend with CORS support for flexible integration
- **Error Handling**: Robust error handling and logging throughout the application
- **Auto-Refresh**: Optional auto-refresh functionality to keep news up-to-date
- **Search & Filter**: Search articles by keywords
- **Responsive Design**: Works on desktop and mobile devices
- **Image Thumbnails**: Displays article thumbnails from RSS feed

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **Backend**: Flask
- **Data Source**: Google News RSS Feed
- **Utilities**: feedparser, requests

## 📋 Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/Ravi3005/Hashtag.git
cd Hashtag
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the Backend API Server

Open a terminal and start the Flask server:

```bash
python app.py
```

The API server will start on `http://localhost:5000`

Expected output:
```
Starting Trending News API server on 0.0.0.0:5000
```

### 4. Run the Streamlit Frontend (New Terminal)

Open another terminal in the same directory:

```bash
streamlit run streamlit_app.py
```

The Streamlit app will automatically open in your browser at `http://localhost:8501`

## 📖 Usage

### Frontend (Streamlit Dashboard)

1. **View Trending News**: The dashboard displays top trending articles by default
2. **Search Articles**: Use the search box to filter articles by keywords
3. **Adjust Settings**: 
   - Change the API server host/port if running on a different machine
   - Select number of articles to display
   - Enable auto-refresh for continuous updates
4. **Click Articles**: Click the "Read Full Article" link to open articles in a new tab

### Backend API (Flask)

#### Base URL
```
http://localhost:5000
```

#### Endpoints

**1. Get Trending News**
```
GET /trending?limit=10&search=keyword
```

Query Parameters:
- `limit` (optional): Number of articles (1-100, default: 10)
- `search` (optional): Search query to filter articles

Example:
```bash
curl "http://localhost:5000/trending?limit=5"
curl "http://localhost:5000/trending?limit=10&search=technology"
```

Response:
```json
{
  "success": true,
  "count": 10,
  "trending_news": [
    {
      "title": "Article Title",
      "link": "https://news.google.com/...",
      "thumbnail": "https://image-url.jpg",
      "published": "1 hour ago"
    }
  ]
}
```

**2. Health Check**
```
GET /api/health
```

Response:
```json
{
  "status": "healthy",
  "service": "Trending News API"
}
```

**3. API Information**
```
GET /api/info
```

Response:
```json
{
  "name": "Trending News API",
  "version": "1.0",
  "endpoints": {...},
  "parameters": {...}
}
```

## 📁 Project Structure

```
Hashtag/
├── app.py                 # Flask backend with REST API
├── fetch_trends.py        # News fetching and parsing logic
├── streamlit_app.py       # Streamlit frontend dashboard
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## 🔧 Configuration

### API Server Settings
In `streamlit_app.py`, you can modify:
- `API Server Host`: Default is `localhost`
- `API Server Port`: Default is `5000`
- `Number of articles`: Default is 10
- `Auto-refresh interval`: 5 minutes

### Logging
Both `app.py` and `fetch_trends.py` include logging configuration. Logs are printed to console.

## 📊 Features Explained

### Error Handling
- **Connection Errors**: Handles API connection failures gracefully
- **Timeout Handling**: 10-second timeout for news feed requests
- **Image Loading**: Fallback to placeholder image if thumbnail unavailable
- **Search Validation**: Filters articles safely without crashes

### Performance
- **Caching**: Streamlit caches API results for 5 minutes to reduce server load
- **Lazy Loading**: Images are loaded on-demand
- **Pagination**: Supports configurable number of articles

### Security
- **CORS Enabled**: Flask backend accepts requests from any origin
- **Input Validation**: Query parameters are validated before processing
- **Error Messages**: User-friendly error messages without exposing internal details

## 🐛 Troubleshooting

### Issue: "Cannot connect to API server"
**Solution**: Make sure the Flask app is running on the correct host and port.
```bash
python app.py  # Make sure this is running
```

### Issue: "No articles found"
**Solution**: Check your internet connection. The RSS feed might be temporarily unavailable.

### Issue: "Images not loading"
**Solution**: Google News might be blocking image requests. Placeholder images will be used instead.

### Issue: Port already in use
**Solution**: Change the port in `app.py`:
```python
serve(app, host="0.0.0.0", port=5001)  # Change 5000 to 5001
```

And update Streamlit sidebar settings to match.

## 📝 API Response Examples

### Successful Request
```bash
curl "http://localhost:5000/trending?limit=2"
```

Response:
```json
{
  "success": true,
  "count": 2,
  "trending_news": [
    {
      "title": "Breaking News: Major Technology Breakthrough",
      "link": "https://news.google.com/articles/...",
      "thumbnail": "https://news.google.com/images/...",
      "published": "2 hours ago"
    },
    {
      "title": "Global Markets React to Economic Data",
      "link": "https://news.google.com/articles/...",
      "thumbnail": "https://news.google.com/images/...",
      "published": "3 hours ago"
    }
  ]
}
```

### Error Response
```json
{
  "success": false,
  "error": "Connection error details",
  "trending_news": []
}
```

## 🚀 Deployment

### Local Network Access
To access the app from other machines on your network:

1. Find your machine's IP address:
   ```bash
   # On Windows
   ipconfig
   
   # On macOS/Linux
   ifconfig
   ```

2. Update Flask server in `app.py`:
   ```python
   serve(app, host="0.0.0.0", port=5000)  # Already configured
   ```

3. Update Streamlit settings to use your IP address instead of `localhost`

### Docker Deployment
Create a `Dockerfile`:
```dockerfile
FROM python:3.9
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
EXPOSE 5000 8501
CMD ["sh", "-c", "python app.py & streamlit run streamlit_app.py"]
```

Build and run:
```bash
docker build -t trending-news .
docker run -p 5000:5000 -p 8501:8501 trending-news
```

## 📚 Additional Resources

- [Streamlit Documentation](https://docs.streamlit.io/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Google News RSS Feed](https://news.google.com/rss)
- [feedparser Documentation](https://feedparser.readthedocs.io/)

## 🤝 Contributing

Feel free to fork this project and submit pull requests for any improvements!

## 📄 License

This project is open source and available under the MIT License.

## 💬 Support

For issues and questions, please create an issue in the GitHub repository.

---

**Made with ❤️ by Ravi3005**
