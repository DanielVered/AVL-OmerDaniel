# username - complete info
# id1      - 211399969
# name1    - Daniel Vered
# id2      - complete info
# name2    - Omer Naziri


"""A class represnting a node in an AVL tree"""


class AVLNode(object):
    """Constructor, you are allowed to add more fields.

    @type key: int or None
    @type value: any
    @param value: data of your node
    """

    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None
        self.parent = None
        self.height = -1

    """returns the left child
    @rtype: AVLNode
    @returns: the left child of self, None if there is no left child (if self is virtual)
    """

    def get_left(self):
        return self.left

    """returns the right child

    @rtype: AVLNode
    @returns: the right child of self, None if there is no right child (if self is virtual)
    """

    def get_right(self):
        return self.right

    """returns the parent 

    @rtype: AVLNode
    @returns: the parent of self, None if there is no parent
    """

    def get_parent(self):
        return self.parent

    """returns the key

        @rtype: int or None
        @returns: the key of self, None if the node is virtual
        """

    def get_key(self):
        return self.key

    """returns the value

    @rtype: any
    @returns: the value of self, None if the node is virtual
    """

    def get_value(self):
        return self.value

    """returns the height

    @rtype: int
    @returns: the height of self, -1 if the node is virtual
    """

    def get_height(self):
        return self.height

    """sets left child

    @type node: AVLNode
    @param node: a node
    """

    def set_left(self, node):
        self.left = node
        return None

    """sets right child

    @type node: AVLNode
    @param node: a node
    """

    def set_right(self, node):
        self.right = node
        return None

    """sets parent

    @type node: AVLNode
    @param node: a node
    """

    def set_parent(self, node):
        self.parent = node
        return None

    """sets key

    @type key: int or None
    @param key: key
    """

    def set_key(self, key):
        self.key = key
        return None

    """sets value

    @type value: any
    @param value: data
    """

    def set_value(self, value):
        self.value = value
        return None

    """sets the height of the node

    @type h: int
    @param h: the height
    """

    def set_height(self, h):
        self.height = h
        return None

    def auto_reset_height(self):
        if self.is_real_node():
            self.height = max(self.right.height, self.left.height) + 1
        return None

    """returns node's balance factor 

    @rtype: int
    @returns: node's balance factor, should satisfy |BF| <= 2.
    """

    def get_balance_factor(self):
        right_height = self.right.height if self.right else 0
        left_height = self.left.height if self.left else 0
        return right_height - left_height

    """returns whether self is not a virtual node 

    @rtype: bool
    @returns: False if self is a virtual node, True otherwise.
    """

    def is_real_node(self):
        return True if self.key else False

    """returns whether self is a left son or a right son
    
`   @pre: self has a parent
    @rtype: bool
    @return: True if self is a left son, False O.W.
    """
    def is_left_son(self):
        return self.parent.left


"""
A class implementing the ADT Dictionary, using an AVL tree.
"""


class AVLTree(object):
    """
    Constructor, you are allowed to add more fields.

    """

    def __init__(self):
        self.root: AVLNode = AVLNode(None, None)
        self.size: int = 0
        self.min_node: AVLNode = self.root
        self.max_node: AVLNode = self.root

    """finds the node with the maximal key
    
    @rtype: AVLNode
    @return: pointer to maximal node in AVLTree
    """
    def calc_max_node(self) -> AVLNode:
        curr_node = self.get_root()
        if not curr_node:
            return AVLNode(None, None)
        else:
            right_son = curr_node.get_right()
            while right_son:
                curr_node = right_son
                right_son = right_son.get_right()
        return curr_node

    """finds the node with the minimal key

    @rtype: AVLNode
    @return: pointer to minimal node in AVLTree
    """
    def calc_min_node(self) -> AVLNode:
        curr_node = self.get_root()
        if not curr_node:
            return AVLNode(None, None)
        else:
            left_son = curr_node.get_left()
            while left_son:
                curr_node = left_son
                left_son = left_son.get_left()
        return curr_node

    """returns the root of the tree representing the dictionary

    @rtype: AVLNode
    @returns: the root, None if the dictionary is empty
    """

    def get_root(self):
        return self.root

    """returns the min node of the AVLTree.

    @rtype: AVLNode
    @returns: the min node of the AVLTree, or None if empty.
    """

    def get_min(self) -> AVLNode:
        return self.min_node

    """returns the max node of the AVLTree.

    @rtype: AVLNode
    @returns: the max node of the AVLTree, or None if empty.
    """

    def get_max(self) -> AVLNode:
        return self.max_node

    def set_root(self, node: AVLNode):
        self.root = node
        return None

    """performs an edge rotation between a parent node and its left son

        @type parent: AVLNode
        @param parent: the parent node involved in the rotation
        @rtype: None
        @returns: None
        """

    @staticmethod
    def rotate_left(parent: AVLNode):
        son = parent.left
        parent.left = son.right
        parent.left.parent = parent
        son.right = parent
        son.parent = parent.parent
        parent.parent = son
        if son.parent.left == parent:
            son.parent.left = son
        else:
            son.parent.right = son
        parent.auto_reset_height()
        son.auto_reset_height()

    """performs an edge rotation between a parent node and its right son

        @type parent: AVLNode
        @param parent: the parent node involved in the rotation
        @rtype: None
        @returns: None
        """

    @staticmethod
    def rotate_right(parent: AVLNode):
        son = parent.right
        parent.right = son.left
        parent.right.parent = parent
        son.left = parent
        son.parent = parent.parent
        parent.parent = son
        if son.parent.left == parent:
            son.parent.left = son
        else:
            son.parent.right = son
        parent.auto_reset_height()
        son.auto_reset_height()

    """searches for a value in the dictionary corresponding to the key

    @type key: int
    @param key: a key to be searched
    @rtype: any
    @returns: the value corresponding to key.
    """

    def search(self, key):
        current_node = self.root
        while key != current_node.key and current_node.is_real_node():
            if current_node.key > key:
                current_node = current_node.left
            else:
                current_node = current_node.right

        if current_node.is_real_node():
            return current_node.value
        return None

    """checks a certain path among the tree in order to rebalance the tree using right and left edge rotations
    
    @type start_node: AVLNode
    @pre: start_node is a real pointer to a node in self, from which the rebalance check will begin
    @rtype: int
    @returns: the number of rebalancing operation due to AVL rebalancing
    """

    def rebalance_tree(self, start_node: AVLNode, is_insert: bool):
        rotations = 0
        current_node = start_node
        while current_node.is_real_node() and not (rotations == 1 and is_insert):
            if current_node.right.height - current_node.left.height > 1:
                self.rotate_right(current_node)
                rotations += 1
            elif current_node.left.height - current_node.right.height > 1:
                self.rotate_left(current_node)
                rotations += 1
            else:
                current_node.auto_reset_height()
            current_node = current_node.parent

        return rotations

    """inserts val at position i in the dictionary

    @type key: int
    @pre: key currently does not appear in the dictionary
    @param key: key of item that is to be inserted to self
    @type val: any
    @param val: the value of the item
    @rtype: int
    @returns: the number of rebalancing operation due to AVL rebalancing
    """

    def insert(self, key, val):
        if self.size == 0:
            self.root = AVLNode(key, val)
            self.root.left = AVLNode(None, None)
            self.root.right(None, None)
            self.size = 1
            return None
        self.size += 1
        new_node = AVLNode(key, val)
        if key > self.max_node.key:
            new_node.parent = self.max_node
            self.max_node.parent.right = new_node
            self.max_node = new_node
        elif key < self.min_node.key:
            new_node.parent = self.min_node
            self.min_node.parent.left = new_node
            self.min_node = new_node
        else:
            current_node = self.root
            while current_node.is_real_node():
                if current_node.key > key:
                    current_node = current_node.left
                else:
                    current_node = current_node.right

            if current_node.parent.left == current_node:
                current_node.parent.left = new_node
            else:
                current_node.parent.right = new_node
            new_node.parent = current_node.parent
            current_node.parent = None
        return self.rebalance_tree(new_node.parent, True)

    """deletes node from the dictionary

    @type node: AVLNode
    @pre: node is a real pointer to a node in self
    @rtype: int
    @returns: the number of rebalancing operation due to AVL rebalancing
    """

    def delete(self, node):
        if self.size == 1:
            self.size = 0
            self.root = AVLNode(None, None)
            return None
        self.size -= 1
        if not (node.right.is_real_node() or node.left.is_real_node()):
            start_node = node.parent
            if node.parent.left == node:
                node.parent.left = AVLNode(None, None)
                node.parent.left.parent = node.parent
            else:
                node.parent.right = AVLNode(None, None)
                node.parent.right.parent = node.parent
        else:
            current_node = node.right
            while not (current_node.left.is_real_node()):
                current_node = current_node.right
            while not (current_node.left.is_real_node()):
                current_node = current_node.left

            if current_node.right.is_real_node():
                current_node.parent.left = current_node.right
            else:
                current_node.parent.left = AVLNode(None, None)

            start_node = current_node.parent
            current_node.parent.left.parent = current_node.parent
            current_node.left = node.left
            current_node.right = node.right
            node.left.parent = current_node
            node.right.parent = current_node
            current_node.parent = node.parent
            if current_node.parent.left == node:
                current_node.parent.left = current_node
            else:
                current_node.parent.right = current_node

        node.parent = None
        node.left = None
        node.right = None
        return self.rebalance_tree(start_node, False)

    """returns an array representing dictionary by making and in-order tree journey
    
        @type node: AVLNode
        @param node: The current node we are visiting during the in-order journey through the tree
        @rtype: list
        @returns: a sorted list according to key of touples (key, value) representing the data structure
        """

    def avl_to_array_help(self, current_node: AVLNode):
        if current_node.is_real_node():
            return self.avl_to_array_help(current_node.left) + [(current_node.key, current_node.value)] + self.avl_to_array_help(
                current_node.right)
        return []

    """returns an array representing dictionary 

    @rtype: list
    @returns: a sorted list according to key of touples (key, value) representing the data structure
    """

    def avl_to_array(self):
        return self.avl_to_array_help(self.root)

    """returns the number of items in dictionary 

    @rtype: int
    @returns: the number of items in dictionary 
    """

    def size(self):
        return self.size

    """splits the dictionary at the i'th index

    @type node: AVLNode
    @pre: node is in self
    @param node: The intended node in the dictionary according to whom we split
    @rtype: list
    @returns: a list [left, right], where left is an AVLTree representing the keys in the 
    dictionary smaller than node.key, right is an AVLTree representing the keys in the 
    dictionary larger than node.key.
    """
    @staticmethod
    def split(node: AVLNode):
        smaller_tree = AVLTree()
        smaller_tree.set_root(node.get_left())
        bigger_tree = AVLTree()
        bigger_tree.set_root(node.get_right())

        parent = node.get_parent()
        while parent:
            if node.is_left_son():
                right_subtree = AVLTree()
                right_subtree.set_root(parent.get_right())
                bigger_tree.join(right_subtree, parent.get_left(), parent.get_right())
            else:
                left_subtree = AVLTree()
                left_subtree.set_root(parent.get_left())
                left_subtree.join(smaller_tree, parent.get_key(), parent.get_val())
                smaller_tree = left_subtree

            node = parent
            parent = node.get_parent()

        return [smaller_tree, bigger_tree]

    """joins self with key and another AVLTree

    @type tree2: AVLTree 
    @param tree2: a dictionary to be joined with self
    @type key: int 
    @param key: The key separting self with tree2
    @type val: any 
    @param val: The value attached to key
    @pre: all keys in self are smaller than key and all keys in tree2 are larger than key
    @rtype: int
    @returns: the absolute value of the difference between the height of the AVL trees joined
    """

    def join(self, tree2, key, val):
        tree1_height = self.get_root().get_height()
        tree2_height = tree2.get_root().get_height()
        connector = AVLNode(key, val)

        if tree1_height <= tree2_height:  # join using min anchor from tree2
            anchor = tree2.get_anchor(tree1_height, is_min=True)
            connector.set_left(self.get_root())
            connector.set_right(anchor)
            connector.set_parent(anchor.get_parent())
            anchor.set_parent(connector)
            self.set_root(tree2.get_root())

        else:  # join using max anchor from tree1
            anchor = self.get_anchor(tree2_height, is_min=False)
            connector.set_right(tree2.get_root())
            connector.set_left(anchor)
            connector.set_parent(anchor.get_parent())
            anchor.set_parent(connector)

        self.rebalance_tree(connector, is_insert=True)
        self.size += 1 + tree2.size

        return abs(tree1_height - tree2_height)

    """Getting a the most left (min) or the most right (max) node (anchor) at a given height.

    @type tree: AVLTree 
    @param tree: an AVLTree to search for an anchor
    @type height: int 
    @param key: the desired height
    @type is_min: bool 
    @param val: The value attached to key
    @pre: height is smaller than the tree root's height
    @rtype: AVLNode
    @returns: the most left (min) or the most right (max) node (anchor) where node.height in [height, height - 1]
    """

    def get_anchor(self, height: int, is_min=True) -> AVLNode:
        assert height > self.get_root().get_height()

        anchor = self.get_min() if is_min else self.get_max()
        while anchor.get_height() < height - 1:
            anchor = anchor.get_parent()
        return anchor
