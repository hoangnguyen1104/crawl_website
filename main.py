from crawl_website import crawl_website
from flask import Flask, request, jsonify

app = Flask(__name__)
@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    return response

# Define a route for the home page
@app.route('/')
def home():
    return "Welcome to the Flask API!"

@app.route('/api/crawl', methods=['POST'])
def post_data():
    data = request.get_json()
    crawl_website(data.get('url'), data.get('link'), data.get('title'), data.get('content'))
    return "Success"
""
if __name__ == '__main__':
    app.run()