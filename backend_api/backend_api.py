from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
import requests
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

# Address of the BST service container (bst_tree)
BST_SERVICE_URL = "http://bst_tree:5001"

@app.route('/health', methods=['GET'])
def health():
    return jsonify(status="healthy"), 200

# Custom CORS configuration
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

@app.before_request
def before_request():
    app.logger.debug(f"Received request: {request.method} {request.url}")
    app.logger.debug(f"Headers: {request.headers}")

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,ngrok-skip-browser-warning')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

@app.route('/bst/traverse', methods=['GET', 'OPTIONS'])
def traverse_bst():
    if request.method == 'OPTIONS':
        return '', 204
    app.logger.debug("Received request for /bst/traverse")
    try:
        response = requests.get(f"{BST_SERVICE_URL}/traverse", timeout=5)
        app.logger.debug(f"BST service response: {response.status_code}, {response.text}")
        return jsonify(response.json()), response.status_code, {'Content-Type': 'application/json'}
    except requests.RequestException as e:
        app.logger.error(f"Error communicating with BST service: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/bst/home', methods=['GET'])
def bst_home():
    app.logger.debug("Received request for /bst/home")
    try:
        response = requests.get(f"{BST_SERVICE_URL}/", timeout=5)
        app.logger.debug(f"BST service home response: {response.status_code}, {response.text}")
        return response.text, response.status_code, {'Content-Type': 'text/html'}
    except requests.RequestException as e:
        app.logger.error(f"Error communicating with BST service home: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/bst/insert', methods=['POST'])
def insert_into_bst():
    app.logger.debug("Received request for /bst/insert")
    data = request.json
    if not data or 'key' not in data:
        return jsonify({"error": "Invalid data: 'key' is required"}), 400
    try:
        response = requests.post(f"{BST_SERVICE_URL}/insert", json=data, timeout=5)
        app.logger.debug(f"BST service insert response: {response.status_code}, {response.text}")
        return jsonify(response.json()), response.status_code
    except requests.RequestException as e:
        app.logger.error(f"Error communicating with BST service for insert: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/bst/search/<int:key>', methods=['GET'])
def search_bst(key):
    app.logger.debug(f"Received request for /bst/search/{key}")
    try:
        response = requests.get(f"{BST_SERVICE_URL}/search/{key}", timeout=5)
        app.logger.debug(f"BST service search response: {response.status_code}, {response.text}")
        return jsonify(response.json()), response.status_code
    except requests.RequestException as e:
        app.logger.error(f"Error communicating with BST service for search: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/bst/delete/<int:key>', methods=['DELETE'])
def delete_bst(key):
    app.logger.debug(f"Received request for /bst/delete/{key}")
    try:
        response = requests.delete(f"{BST_SERVICE_URL}/delete/{key}", timeout=5)
        app.logger.debug(f"BST service delete response: {response.status_code}, {response.text}")
        return jsonify(response.json()), response.status_code
    except requests.RequestException as e:
        app.logger.error(f"Error communicating with BST service for delete: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/bst/display', methods=['GET'])
def display_bst():
    app.logger.debug("Received request for /bst/display")
    try:
        response = requests.get(f"{BST_SERVICE_URL}/display", timeout=5)
        app.logger.debug(f"BST service display response: {response.status_code}, {response.text}")
        return jsonify(response.json()), response.status_code
    except requests.RequestException as e:
        app.logger.error(f"Error communicating with BST service for display: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

# Catch-all route for other BST-related requests
@app.route('/bst/<path:subpath>', methods=['GET', 'POST', 'DELETE'])
def handle_bst_requests(subpath):
    app.logger.debug(f"Received request for /bst/{subpath}")
    url = f"{BST_SERVICE_URL}/{subpath}"
    try:
        if request.method == 'GET':
            response = requests.get(url, timeout=5)
        elif request.method == 'POST':
            response = requests.post(url, json=request.json, timeout=5)
        elif request.method == 'DELETE':
            response = requests.delete(url, timeout=5)
        app.logger.debug(f"BST service response for {subpath}: {response.status_code}, {response.text}")
        return jsonify(response.json()), response.status_code
    except requests.RequestException as e:
        app.logger.error(f"Error communicating with BST service for {subpath}: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

# Start the Flask application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
