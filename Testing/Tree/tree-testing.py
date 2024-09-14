import sys
import os

# Add the parent directory to the Python path to import BST
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Tree.BST import BinarySearchTree

def test_insert():
    bst = BinarySearchTree()
    bst.insert(50)
    bst.insert(30)
    bst.insert(70)
    assert bst.inorder_traversal() == [30, 50, 70], "Insert test failed"
    print("Insert test passed")

def test_search_existing():
    bst = BinarySearchTree()
    bst.insert(50)
    bst.insert(30)
    bst.insert(70)
    assert bst.search(30) is not None, "Search existing test failed"
    print("Search existing test passed")

def test_search_non_existing():
    bst = BinarySearchTree()
    bst.insert(50)
    bst.insert(30)
    bst.insert(70)
    assert bst.search(40) is None, "Search non-existing test failed"
    print("Search non-existing test passed")

def test_delete_leaf():
    bst = BinarySearchTree()
    bst.insert(50)
    bst.insert(30)
    bst.insert(70)
    bst.delete(30)
    assert bst.inorder_traversal() == [50, 70], "Delete leaf test failed"
    print("Delete leaf test passed")

def test_delete_with_one_child():
    bst = BinarySearchTree()
    bst.insert(50)
    bst.insert(30)
    bst.insert(70)
    bst.insert(60)
    bst.delete(70)
    assert bst.inorder_traversal() == [30, 50, 60], "Delete with one child test failed"
    print("Delete with one child test passed")

def test_delete_with_two_children():
    bst = BinarySearchTree()
    bst.insert(50)
    bst.insert(30)
    bst.insert(70)
    bst.insert(60)
    bst.insert(80)
    bst.delete(70)
    assert bst.inorder_traversal() == [30, 50, 60, 80], "Delete with two children test failed"
    print("Delete with two children test passed")

def test_inorder_traversal():
    bst = BinarySearchTree()
    keys = [50, 30, 70, 20, 40, 60, 80, 35]
    for key in keys:
        bst.insert(key)
    assert bst.inorder_traversal() == sorted(keys), "Inorder traversal test failed"
    print("Inorder traversal test passed")

if __name__ == "__main__":
    test_insert()
    test_search_existing()
    test_search_non_existing()
    test_delete_leaf()
    test_delete_with_one_child()
    test_delete_with_two_children()
    test_inorder_traversal()
    print("All tests completed")