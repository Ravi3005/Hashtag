from flask import Flask, jsonify
from fetch_trends import get_trending_news

app = Flask(__name__)

@app.route('/trending', methods=['GET'])
def trending():
    news = get_trending_news()
    return jsonify({"trending_news": news})

from waitress import serve

if __name__ == '__main__':
    serve(app, host="0.0.0.0", port=5000)

