from flask import Flask, request, jsonify, render_template_string
import logging
import sys
from Tree.BST import BinarySearchTree

app = Flask(__name__)

# Set up logging to both stdout and debug level
logging.basicConfig(level=logging.DEBUG, handlers=[logging.StreamHandler(sys.stdout)])
logger = logging.getLogger('BST-API')

# Binary Search Tree instance
bst = BinarySearchTree()

# Log request information for debugging purposes
@app.before_request
def log_request_info():
    logger.info(
        f"Request from origin: {request.origin}, path: {request.path}, method: {request.method}, headers: {request.headers}")

@app.after_request
def log_response_info(response):
    logger.info(f"Response: {response.status_code} for {request.path}")
    return response

# Define the 'about' route
@app.route('/about', methods=['GET'])
def about():
    logger.debug("Processing /about route")
    return jsonify({"traversal": "shikaka"}), 200

# Documentation home page
@app.route('/', methods=['GET'])
def home():
    logger.debug("Processing / route (home)")
    html_template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Binary Search Tree API</title>
        <style>
            body { font-family: Arial, sans-serif; line-height: 1.6; padding: 20px; max-width: 800px; margin: 0 auto; }
            h1 { color: #333; }
            .endpoint { margin-bottom: 30px; border-bottom: 1px solid #ccc; padding-bottom: 20px; }
            .route { font-family: monospace; font-size: 1.2em; font-weight: bold; color: #0066cc; }
            .method { font-weight: bold; color: #009900; }
            .description { margin: 10px 0; }
            .usage { background-color: #f4f4f4; padding: 10px; border-radius: 5px; }
            .usage pre { margin: 0; white-space: pre-wrap; }
        </style>
    </head>
    <body>
        <h1>Welcome to the Binary Search Tree API</h1>

        <div class="endpoint">
            <div class="route">GET /about</div>
            <div class="description">Returns a simple about message.</div>
            <div class="usage">
                <pre>curl -X GET http://localhost/about</pre>
            </div>
        </div>

        <div class="endpoint">
            <div class="route">POST /insert</div>
            <div class="method">Method: POST</div>
            <div class="description">Inserts a new node into the binary search tree.</div>
            <div class="usage">
                <pre>
curl -X POST http://localhost/insert \\
-H "Content-Type: application/json" \\
-d '{"key": 10, "data": {"name": "Node10"}}'
                </pre>
            </div>
        </div>

        <div class="endpoint">
            <div class="route">GET /search/&lt;int:key&gt;</div>
            <div class="method">Method: GET</div>
            <div class="description">Searches for a node by key.</div>
            <div class="usage">
                <pre>curl -X GET http://localhost/search/10</pre>
            </div>
        </div>

        <div class="endpoint">
            <div class="route">DELETE /delete/&lt;int:key&gt;</div>
            <div class="method">Method: DELETE</div>
            <div class="description">Deletes a node by key from the binary search tree.</div>
            <div class="usage">
                <pre>curl -X DELETE http://localhost/delete/10</pre>
            </div>
        </div>

        <div class="endpoint">
            <div class="route">GET /traverse</div>
            <div class="method">Method: GET</div>
            <div class="description">Returns the in-order traversal of the binary search tree.</div>
            <div class="usage">
                <pre>curl -X GET http://localhost/traverse</pre>
            </div>
        </div>

        <div class="endpoint">
            <div class="route">POST /create</div>
            <div class="method">Method: POST</div>
            <div class="description">Creates a binary search tree with multiple keys.</div>
            <div class="usage">
                <pre>
curl -X POST http://localhost/create \\
-H "Content-Type: application/json" \\
-d '{
    "keys": [
        {"key": 10, "data": {"name": "Node10"}},
        {"key": 20, "data": {"name": "Node20"}},
        {"key": 5, "data": {"name": "Node5"}}
    ]
}'
                </pre>
            </div>
        </div>

        <div class="endpoint">
            <div class="route">GET /display</div>
            <div class="method">Method: GET</div>
            <div class="description">Displays the structure of the binary search tree.</div>
            <div class="usage">
                <pre>curl -X GET http://localhost/display</pre>
            </div>
        </div>

    </body>
    </html>
    """
    return render_template_string(html_template)

# Route to insert a node
@app.route('/insert', methods=['POST'])
def insert():
    data = request.json
    key = data.get('key')
    node_data = data.get('data', {})
    logger.debug(f"Received insert request with key: {key}, data: {node_data}")

    if key is not None:
        bst.insert(key, node_data)
        logger.info(f"Inserted key {key} with data {node_data}")
        return jsonify({"message": f"Inserted {key} with data {node_data}"}), 201
    else:
        logger.warning("Insert request failed: No key provided")
        return jsonify({"error": "No key provided"}), 400

# Route to search for a node by key
@app.route('/search/<int:key>', methods=['GET'])
def search(key):
    logger.debug(f"Received search request for key: {key}")
    result = bst.search(key)

    if result:
        logger.info(f"Found key {key} with data {result.data}")
        return jsonify({"key": result.key, "data": result.data}), 200
    else:
        logger.warning(f"Key {key} not found")
        return jsonify({"message": f"{key} not found"}), 404

# Route to delete a node by key
@app.route('/delete/<int:key>', methods=['DELETE'])
def delete(key):
    logger.debug(f"Received delete request for key: {key}")
    bst.delete(key)
    logger.info(f"Deleted key {key}")
    return jsonify({"message": f"Deleted {key}"}), 200

# Route for in-order traversal
@app.route('/traverse', methods=['GET'])
def traverse():
    logger.debug("Received inorder traversal request")
    traversal = bst.inorder_traversal()
    logger.info(f"Inorder traversal: {traversal}")
    return jsonify({"traversal": traversal}), 200

# Route to create a tree with multiple keys
@app.route('/create', methods=['POST'])
def create_tree():
    data = request.json
    keys = data.get('keys', [])
    logger.debug(f"Received create request with keys: {keys}")

    for item in keys:
        key = item.get('key')
        node_data = item.get('data', {})
        if key is not None:
            bst.insert(key, node_data)
            logger.info(f"Inserted key {key} with data {node_data}")

    return jsonify({"message": f"Created tree with keys: {[item['key'] for item in keys]}"}), 201

# Route to display the tree structure
@app.route('/display', methods=['GET'])
def display_tree():
    logger.debug("Received display tree request")
    tree_structure = bst.display()
    logger.info(f"Tree structure: {tree_structure}")
    return jsonify({"tree_structure": tree_structure}), 200

# Start the Flask app
if __name__ == '__main__':
    logger.info("Starting Binary Search Tree API")
    app.run(host='0.0.0.0', port=80, debug=True)
