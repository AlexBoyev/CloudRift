import sys
import os

# Add the parent directory to the Python path to import BST
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Tree.BST import BinarySearchTree

def test_bst():
    # Create a new BST
    bst = BinarySearchTree()

    # Test insertion
    keys = [50, 30, 20, 40, 70, 60, 80]
    for key in keys:
        bst.insert(key)
    print("BST created with keys:", keys)

    # Test inorder traversal
    print("Inorder traversal:", bst.inorder_traversal())

    # Test search
    for key in [20, 55]:
        result = bst.search(key)
        print(f"Search for {key}: {'Found' if result else 'Not Found'}")

    # Test deletion
    delete_key = 30
    bst.delete(delete_key)
    print(f"Deleted {delete_key}")
    print("Inorder traversal after deletion:", bst.inorder_traversal())

    # Test edge cases
    bst.insert(10)  # Insert a new minimum
    bst.insert(90)  # Insert a new maximum
    bst.delete(50)  # Delete the root
    print("Inorder traversal after edge case operations:", bst.inorder_traversal())