"""
File: linkedbst.py
"""
import random
import sys
import threading
import time

from abstractcollection import AbstractCollection
from bstnode import BSTNode
from linkedstack import LinkedStack

sys.setrecursionlimit(100000)
threading.stack_size(200000000)


# pylint: disable=invalid-name, no-self-use, protected-access, attribute-defined-outside-init
# pylint: disable= singleton-comparison, too-many-instance-attributes

class LinkedBST(AbstractCollection):
    """An link-based binary search tree implementation."""

    def __init__(self, sourceCollection=None):
        """Sets the initial state of self, which includes the
        contents of sourceCollection, if it's present."""
        self._root = None
        AbstractCollection.__init__(self, sourceCollection)

    # Accessor methods
    def __str__(self):
        """Returns a string representation with the tree rotated
        90 degrees counterclockwise."""

        def recurse(node, level):
            s = ""
            if node != None:
                s += recurse(node.right, level + 1)
                s += "| " * level
                s += str(node.data) + "\n"
                s += recurse(node.left, level + 1)
            return s

        return recurse(self._root, 0)

    def __iter__(self):
        """Supports a preorder traversal on a view of self."""
        if not self.isEmpty():
            stack = LinkedStack()
            stack.push(self._root)
            while not stack.isEmpty():
                node = stack.pop()
                yield node.data
                if node.right != None:
                    stack.push(node.right)
                if node.left != None:
                    stack.push(node.left)

    def preorder(self):
        """Supports a preorder traversal on a view of self."""
        return None

    def inorder(self):
        """Supports an inorder traversal on a view of self."""
        lyst = []

        def recurse(node):
            if node != None:
                recurse(node.left)
                lyst.append(node.data)
                recurse(node.right)

        recurse(self._root)
        return iter(lyst)

    def postorder(self):
        """Supports a postorder traversal on a view of self."""
        return None

    def levelorder(self):
        """Supports a levelorder traversal on a view of self."""
        return None

    def __contains__(self, item):
        """Returns True if target is found or False otherwise."""
        return self.find(item) != None

    def find(self, item):
        """If item matches an item in self, returns the
        matched item, or None otherwise."""

        def recurse(node):
            if node is None:
                return None
            if item == node.data:
                return node.data
            if item < node.data:
                return recurse(node.left)
            return recurse(node.right)

        return recurse(self._root)

    # Mutator methods
    def clear(self):
        """Makes self become empty."""
        self._root = None
        self._size = 0

    def add(self, item):
        """Adds item to the tree."""

        # Helper function to search for item's position
        def recurse(node):
            # New item is less, go left until spot is found
            if item < node.data:
                if node.left == None:
                    node.left = BSTNode(item)
                else:
                    recurse(node.left)
            # New item is greater or equal,
            # go right until spot is found
            elif node.right == None:
                node.right = BSTNode(item)
            else:
                recurse(node.right)
                # End of recurse

        # Tree is empty, so new item goes at the root
        if self.isEmpty():
            self._root = BSTNode(item)
        # Otherwise, search for the item's spot
        else:
            recurse(self._root)
        self._size += 1

    def remove(self, item):
        """Precondition: item is in self.
        Raises: KeyError if item is not in self.
        postcondition: item is removed from self."""
        if not item in self:
            raise KeyError("Item not in tree.""")

        # Helper function to adjust placement of an item
        def liftMaxInLeftSubtreeToTop(top):
            # Replace top's datum with the maximum datum in the left subtree
            # Pre:  top has a left child
            # Post: the maximum node in top's left subtree
            #       has been removed
            # Post: top.data = maximum value in top's left subtree
            parent = top
            currentNode = top.left
            while not currentNode.right == None:
                parent = currentNode
                currentNode = currentNode.right
            top.data = currentNode.data
            if parent == top:
                top.left = currentNode.left
            else:
                parent.right = currentNode.left

        # Begin main part of the method
        if self.isEmpty():
            return None

        # Attempt to locate the node containing the item
        itemRemoved = None
        preRoot = BSTNode(None)
        preRoot.left = self._root
        parent = preRoot
        direction = 'L'
        currentNode = self._root
        while not currentNode == None:
            if currentNode.data == item:
                itemRemoved = currentNode.data
                break
            parent = currentNode
            if currentNode.data > item:
                direction = 'L'
                currentNode = currentNode.left
            else:
                direction = 'R'
                currentNode = currentNode.right

        # Return None if the item is absent
        if itemRemoved == None:
            return None

        # The item is present, so remove its node

        # Case 1: The node has a left and a right child
        #         Replace the node's value with the maximum value in the
        #         left subtree
        #         Delete the maximium node in the left subtree
        if not currentNode.left == None \
                and not currentNode.right == None:
            liftMaxInLeftSubtreeToTop(currentNode)
        else:

            # Case 2: The node has no left child
            if currentNode.left == None:
                newChild = currentNode.right

                # Case 3: The node has no right child
            else:
                newChild = currentNode.left

                # Case 2 & 3: Tie the parent to the new child
            if direction == 'L':
                parent.left = newChild
            else:
                parent.right = newChild

        # All cases: Reset the root (if it hasn't changed no harm done)
        #            Decrement the collection's size counter
        #            Return the item
        self._size -= 1
        if self.isEmpty():
            self._root = None
        else:
            self._root = preRoot.left
        return itemRemoved

    def replace(self, item, newItem):
        """
        If item is in self, replaces it with newItem and
        returns the old item, or returns None otherwise."""
        probe = self._root
        while probe != None:
            if probe.data == item:
                oldData = probe.data
                probe.data = newItem
                return oldData
            if probe.data > item:
                probe = probe.left
            else:
                probe = probe.right
        return None

    def height(self):
        """
        Return the height of tree
        :return: int
        """

        def height1(top):
            """
            Helper function
            :param top: BSTNode
            :return: int
            """
            if top == None:
                return 0
            return 1 + max(height1(top.left), height1(top.right))

        return height1(self._root)

    def is_balanced(self):
        """
        Return True if tree is balanced
        :return: bool
        """

        def height1(top):
            """
            Helper function to calculate height
            :param top: BSTNode
            :type top: BSTNode
            :return: int
            :rtype: int
            """
            if top == None:
                return 0
            return 1 + max(height1(top.left), height1(top.right))

        def is_balanced1(top):
            """
            Helper function to check if tree is balanced
            :param top: BSTNode
            :type top: BSTNode
            :return: bool (True if balanced)
            :rtype: bool
            """
            if top == None:
                return True
            return (abs(height1(top.left) - height1(top.right)) <= 1 and
                    is_balanced1(top.left) and
                    is_balanced1(top.right))

        return is_balanced1(self._root)

    def range_find(self, low, high):
        """ Returns a list of the items in the tree, where low <= item <= high. """

        def range_find_1(top, low, high):
            """ Recursive helper function to rangeFind """
            if top == None:
                return []
            if top.data > high:
                return range_find_1(top.left, low, high)
            if top.data < low:
                return range_find_1(top.right, low, high)
            return (range_find_1(top.left, low, high) +
                    [top.data] + range_find_1(top.right, low, high))

        return range_find_1(self._root, low, high)

    def rebalance(self):
        """
        Rebalances the tree.
        :return:
        """
        elements_list = list(self.inorder())
        elements_list.sort()

        new_tree = LinkedBST()

        def add_middle_to_tree(elements_list, start, end):
            """
            Helper function to add middle elements to the tree
            :param elements_list: list
            :param start: int
            :param end: int
            """
            if start > end:
                return
            middle = (start + end) // 2
            new_tree.add(elements_list[middle])
            add_middle_to_tree(elements_list, start, middle - 1)
            add_middle_to_tree(elements_list, middle + 1, end)

        add_middle_to_tree(elements_list, 0, len(elements_list) - 1)

        self._root = new_tree._root
        return self

    def successor(self, item):
        """
        Returns the smallest item that is larger than
        item, or None if there is no such item.
        :param item: int
        :type item: int
        :return: int
        :rtype: int
        """

        def successor1(top):
            """ Helper function to find successor """
            if top == None:
                return None

            if top.data > item:
                if top.left == None or top.left.data <= item:
                    return top.data
                return successor1(top.left)

            if top.right is None or top.right.data >= item:
                return top.data
            return successor1(top.right)

        return successor1(self._root)

    def predecessor(self, item):
        """
        Returns the largest item that is smaller than
        item, or None if there is no such item.
        :param item: item to find predecessor of
        :type item: int
        :return: the predecessor of item
        :rtype: int
        """

        def predecessor1(top):
            """ Helper function """
            if top == None:
                return None

            if top.data < item:
                if top.right == None or top.right.data >= item:
                    return top.data
                return predecessor1(top.right)

            if top.left == None or top.left.data <= item:
                return top.data
            return predecessor1(top.left)

        return predecessor1(self._root)

    @staticmethod
    def lines_read(file_name: str) -> list:
        """ Gets list of lines from file

        :param file_name: name of file
        :type file_name: str
        :return: list of lines from file
        :rtype: list
        """

        with open(file_name, "r", encoding='utf-8') as file:
            all_lines = [line.rstrip() for line in file.readlines() if len(line.rstrip()) > 0]
        return all_lines

    @classmethod
    def demo_bst(cls, path, number_of_lines=10000, number_of_tests=5000):
        """
        Demonstration of efficiency binary search tree for the search tasks.
        :param path: path to the file
        :type path: str
        :param number_of_lines: number of lines in file to use for testing
        :type number_of_lines: int
        :param number_of_tests: number of tests
        :type number_of_tests: int

        Test example:

        Start of testing binary search tree
        Test can take a while
        Number of lines used: 10000
        Number of tests:  5000
        File:  words.txt

        Time for searching in list of words:  0.20072197914123535
        Time for searching in unbalanced tree:  4.189276218414307
        Time for searching in shuffled tree:  0.01829361915588379
        Time for searching in balanced tree:  0.010142087936401367
        """
        print("Start of testing binary search tree")
        print("Test can take a while")
        print(f"Number of lines used: {number_of_lines}")
        print(f"Number of tests: {number_of_tests}")
        print(f"File: {path}")
        print("")

        lines = cls.lines_read(path)[:number_of_lines]

        random_words_to_search = []
        for i in range(number_of_tests):
            random_words_to_search.append(lines[random.randint(0, len(lines) - 1)])

        start = time.time()
        for i in range(number_of_tests):
            try:
                lines.index(random_words_to_search[i])  # search for word in list
            except ValueError:
                pass
        end = time.time()
        print("Time for searching in list of words: ", end - start)

        test_tree_1 = LinkedBST()
        for line in lines:
            test_tree_1.add(line)

        start = time.time()
        for i in range(number_of_tests):
            test_tree_1.find(random_words_to_search[i])  # search for word in tree
        end = time.time()
        print("Time for searching in unbalanced tree: ", end - start)

        test_tree_2 = LinkedBST()
        random.shuffle(lines)
        for line in lines:
            test_tree_2.add(line)

        start = time.time()
        for i in range(number_of_tests):
            test_tree_2.find(random_words_to_search[i])  # search for word in tree
        end = time.time()
        print("Time for searching in shuffled tree: ", end - start)

        test_tree_1.rebalance()
        start = time.time()
        for i in range(number_of_tests):
            test_tree_1.find(random_words_to_search[i])  # search for word in tree
        end = time.time()
        print("Time for searching in balanced tree: ", end - start)


if __name__ == '__main__':
    lbst = LinkedBST()
    lbst.add(5)
    lbst.add(3)
    lbst.add(7)
    lbst.add(2)
    lbst.add(4)
    lbst.add(6)
    lbst.add(8)
    lbst.add(1)
    lbst.add(9)
    lbst.add(10)
    lbst.add(11)
    lbst.add(12)
    lbst.add(13)
    lbst.add(14)

    print(lbst)

    print(lbst.height())  # 9
    print(lbst.is_balanced())  # False
    print(lbst.range_find(1, 14))  # [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
    print(lbst.successor(1))  # 2
    print(lbst.predecessor(14))  # 13

    print(lbst.rebalance())
    print(lbst.is_balanced())  # True
    print(lbst.height())  # 4

    print()

    # Fix for big recursion limit
    thread = threading.Thread(target=LinkedBST.demo_bst, args=["words.txt"])
    thread.start()
