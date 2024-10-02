class Node:
    def __init__(self, key, data=None):
        self.key = key
        self.data = data if data is not None else {
            "name": f"Node {key}",
            "description": f"This is node {key}",
            "metadata": {
                "created_at": "2024-09-17T10:00:00Z",
                "last_modified": "2024-09-17T10:00:00Z",
                "version": 1
            },
            "tags": [],
            "custom_attributes": {}
        }
        self.left = None
        self.right = None

class BinarySearchTree:
    def __init__(self):
        self.root = None

    def insert(self, key, data=None):
        self.root = self._insert_recursive(self.root, key, data)

    def _insert_recursive(self, root, key, data):
        if root is None:
            return Node(key, data)
        if key < root.key:
            root.left = self._insert_recursive(root.left, key, data)
        elif key > root.key:
            root.right = self._insert_recursive(root.right, key, data)
        else:
            # Update data if key already exists
            root.data.update(data or {})
        return root

    def search(self, key):
        return self._search_recursive(self.root, key)

    def _search_recursive(self, root, key):
        if root is None or root.key == key:
            return root
        if key < root.key:
            return self._search_recursive(root.left, key)
        return self._search_recursive(root.right, key)

    def delete(self, key):
        self.root = self._delete_recursive(self.root, key)

    def _delete_recursive(self, root, key):
        if root is None:
            return root
        if key < root.key:
            root.left = self._delete_recursive(root.left, key)
        elif key > root.key:
            root.right = self._delete_recursive(root.right, key)
        else:
            if root.left is None:
                return root.right
            elif root.right is None:
                return root.left
            temp = self._min_value_node(root.right)
            root.key = temp.key
            root.data = temp.data
            root.right = self._delete_recursive(root.right, temp.key)
        return root

    def _min_value_node(self, node):
        current = node
        while current.left is not None:
            current = current.left
        return current

    def inorder_traversal(self):
        result = []
        self._inorder_recursive(self.root, result)
        return result

    def _inorder_recursive(self, root, result):
        if root:
            self._inorder_recursive(root.left, result)
            result.append({"key": root.key, "data": root.data})
            self._inorder_recursive(root.right, result)

    def display(self):
        if not self.root:
            return "Empty tree"

        def display_util(node, level=0):
            if node is None:
                return []

            result = []
            if node.right:
                result.extend(display_util(node.right, level + 1))
            result.append("  " * level + f"{node.key}: {node.data['name']}")
            if node.left:
                result.extend(display_util(node.left, level + 1))
            return result

        return "\n".join(display_util(self.root))