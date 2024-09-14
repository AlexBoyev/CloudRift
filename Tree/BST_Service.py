from flask import Flask, request, jsonify
from bst import BinarySearchTree

app = Flask(__name__)
bst = BinarySearchTree()

@app.route('/insert', methods=['POST'])
def insert():
    data = request.json
    key = data.get('key')
    if key is not None:
        bst.insert(key)
        return jsonify({"message": f"Inserted {key}"}), 201
    return jsonify({"error": "No key provided"}), 400

@app.route('/search/<int:key>', methods=['GET'])
def search(key):
    result = bst.search(key)
    if result:
        return jsonify({"message": f"Found {key}"}), 200
    return jsonify({"message": f"{key} not found"}), 404

@app.route('/delete/<int:key>', methods=['DELETE'])
def delete(key):
    bst.delete(key)
    return jsonify({"message": f"Deleted {key}"}), 200

@app.route('/traverse', methods=['GET'])
def traverse():
    traversal = bst.inorder_traversal()
    return jsonify({"traversal": traversal}), 200

@app.route('/create', methods=['POST'])
def create_tree():
    data = request.json
    keys = data.get('keys', [])
    for key in keys:
        bst.insert(key)
    return jsonify({"message": f"Created tree with keys: {keys}"}), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)