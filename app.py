from flask import Flask, jsonify, request
from flask_cors import CORS
from fetch_trends import get_trending_news, search_news
import logging
from waitress import serve

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Enable CORS for frontend communication
CORS(app, resources={r"/api/*": {"origins": "*"}})

@app.route('/trending', methods=['GET'])
def trending():
    """Fetch trending news with optional parameters"""
    try:
        # Get query parameters
        num_articles = request.args.get('limit', default=10, type=int)
        search_query = request.args.get('search', default='', type=str)
        
        # Validate parameters
        if num_articles < 1 or num_articles > 100:
            num_articles = 10
        
        # Fetch news
        news = get_trending_news(num_articles=num_articles)
        
        # Apply search filter if provided
        if search_query:
            news = search_news(news, search_query)
            logger.info(f"Search query '{search_query}' returned {len(news)} results")
        
        response = {
            "success": True,
            "count": len(news),
            "trending_news": news
        }
        
        logger.info(f"Returned {len(news)} trending articles")
        return jsonify(response), 200
        
    except Exception as e:
        logger.error(f"Error in /trending endpoint: {str(e)}")
        return jsonify({
            "success": False,
            "error": str(e),
            "trending_news": []
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "Trending News API"
    }), 200

@app.route('/api/info', methods=['GET'])
def api_info():
    """Get API information"""
    return jsonify({
        "name": "Trending News API",
        "version": "1.0",
        "endpoints": {
            "/trending": "GET - Fetch trending news",
            "/api/health": "GET - Health check",
            "/api/info": "GET - API information"
        },
        "parameters": {
            "limit": "Number of articles (1-100, default: 10)",
            "search": "Search query to filter articles"
        }
    }), 200

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        "success": False,
        "error": "Endpoint not found",
        "message": "Visit /api/info for available endpoints"
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logger.error(f"Internal server error: {str(error)}")
    return jsonify({
        "success": False,
        "error": "Internal server error"
    }), 500

if __name__ == '__main__':
    logger.info("Starting Trending News API server on 0.0.0.0:5000")
    serve(app, host="0.0.0.0", port=5000)
