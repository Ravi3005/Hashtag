from flask import Flask, jsonify
from fetch_trends import get_trending_news

app = Flask(__name__)

@app.route('/trending', methods=['GET'])
def trending():
    news = get_trending_news()
    return jsonify({"trending_news": news})

if __name__ == '__main__':
    app.run(debug=True)
