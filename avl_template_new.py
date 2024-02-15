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
        if key is None:
            self.height = -1
        else:
            self.height = 0

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

    def set_parent(self, parent):
        self.parent = parent
        return None

    """sets value

    @type value: any
    @param value: data
    """

    def set_value(self, value):
        self.value = value
        return None

    def auto_reset_height(self):
        if self.is_real_node():
            tmp = self.height
            self.height = max(self.right.height, self.left.height) + 1
            return tmp != self.height
        return False

    """returns node's balance factor 

    @rtype: int
    @returns: node's balance factor, should satisfy |BF| <= 2.
    """

    def get_balance_factor(self):
        if self.is_real_node():
            return self.right.height - self.left.height
        return 0

    """returns whether self is not a virtual node 

    @rtype: bool
    @returns: False if self is a virtual node, True otherwise.
    """

    def is_real_node(self):
        return self.key is not None

    """returns whether self is a left son or a right son
    
`   @pre: self has a parent
    @rtype: bool
    @return: True if self is a left son, False O.W.
    """
    def is_left_son(self):
        if self.parent is not None:
            return self.parent.left is self
        return False


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

    @staticmethod
    def calc_tree_size(node: AVLNode) -> int:
        if not node.is_real_node():
            return 0

        left_size = AVLTree.calc_tree_size(node.get_left())
        right_size = AVLTree.calc_tree_size(node.get_right())
        return left_size + right_size + 1

    """finds the node with the maximal key
    
    @rtype: AVLNode
    @return: pointer to maximal node in AVLTree
    """
    def calc_max_node(self) -> AVLNode:
        curr_node = self.get_root()
        if not curr_node.is_real_node():
            return AVLNode(None, None)
        else:
            right_son = curr_node
            while right_son.is_real_node():
                curr_node = right_son
                right_son = right_son.get_right()
        return curr_node

    """finds the node with the minimal key

    @rtype: AVLNode
    @return: pointer to minimal node in AVLTree
    """
    def calc_min_node(self) -> AVLNode:
        curr_node = self.get_root()
        if not curr_node.is_real_node():
            return AVLNode(None, None)
        else:
            left_son = curr_node
            while left_son.is_real_node():
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

    def fix_edges(self):
        self.min_node = self.calc_min_node()
        self.max_node = self.calc_max_node()

    def replace_tree(self, tree):
        self.root = tree.root
        self.size = tree.size
        self.min_node = tree.min_node
        self.max_node = tree.max_node

    """An alternative contructor to initiate a tree from a root.
    @type root: AVLNode
    @return: an AVLTree whose root is the one given
    @attention: the returned tree will have an inconsistency size.
    """
    @staticmethod
    def tree_from_root(root: AVLNode):
        tree = AVLTree()
        tree.insert(root.get_key(), root.get_value())
        return tree

    """performs an edge rotation between a parent node and its left son

        @type parent: AVLNode
        @param parent: the parent node involved in the rotation
        @type normal_trigger: bool
        @param normal_trigger: True at default, False if triggered from rotate_left (dual rotation) 
        @rtype: None
        @returns: None
        """

    def rotate_left(self, parent: AVLNode, normal_trigger: bool = True):
        r_val = 1
        if normal_trigger and parent.left.is_real_node() and parent.left.right.height - parent.left.left.height > 0:
            son = parent.left.right
            self.rotate_right(parent.left, False)
            r_val = 2
        else:
            son = parent.left
        parent.left = son.right
        parent.left.parent = parent
        son.right = parent
        son.parent = parent.parent
        parent.parent = son
        if parent is self.root:
            self.root = son
            son.parent = None
        elif son.parent.left == parent:
            son.parent.left = son
        else:
            son.parent.right = son
        parent.auto_reset_height()
        son.auto_reset_height()
        return r_val

    """performs an edge rotation between a parent node and its right son

        @type parent: AVLNode
        @param parent: the parent node involved in the rotation
        @type normal_trigger: bool
        @param normal_trigger: True at default, False if triggered from rotate_left (dual rotation) 
        @rtype: int
        @returns: the number of rebalancing operations required during the rotation
        """

    def rotate_right(self, parent: AVLNode, normal_trigger: bool = True):
        r_val = 1
        if normal_trigger and parent.right.is_real_node() and parent.right.right.height - parent.right.left.height < 0:
            son = parent.right.left
            self.rotate_left(parent.right, False)
            r_val = 2
        else:
            son = parent.right
        parent.right = son.left
        parent.right.parent = parent
        son.left = parent
        son.parent = parent.parent
        parent.parent = son
        if parent is self.root:
            self.root = son
            son.parent = None
        elif son.parent.left == parent:
            son.parent.left = son
        else:
            son.parent.right = son
        parent.auto_reset_height()
        son.auto_reset_height()
        return r_val

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
    @type is_insert: bool
    @param: is_insert is True when this function is called during node insertion
    @rtype: int
    @returns: the number of rebalancing operation due to AVL rebalancing
    """

    def rebalance_tree(self, start_node: AVLNode, is_insert: bool):
        if start_node is None:
            return 0
        balance_ops = 0
        current_node = start_node
        height_change = True
        is_rotated = False
        while not (current_node is None) and not (is_rotated and is_insert):
            height_change = current_node.auto_reset_height()
            if current_node.right.height - current_node.left.height > 1:
                balance_ops += self.rotate_right(current_node)
                is_rotated = True
            elif current_node.left.height - current_node.right.height > 1:
                balance_ops += self.rotate_left(current_node)
                is_rotated = True
            else:
                if height_change:
                    balance_ops += 1
            current_node = current_node.parent

        return balance_ops

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
        self.size += 1
        new_node = AVLNode(key, val)
        new_node.right = AVLNode(None, None)
        new_node.right.parent = new_node
        new_node.left = AVLNode(None, None)
        new_node.left.parent = new_node
        new_node.auto_reset_height()
        if self.root.key is None:
            self.root = new_node
            self.min_node = new_node
            self.max_node = new_node
            return 0
        elif key > self.max_node.key:
            self.max_node.right.parent = None
            new_node.parent = self.max_node
            self.max_node.right = new_node
            self.max_node = new_node
        elif key < self.min_node.key:
            self.min_node.left.parent = None
            new_node.parent = self.min_node
            self.min_node.left = new_node
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

        return self.rebalance_tree(new_node, True)

    """swaps two nodes before deletion

    @type full_node: AVLNode
    @pre: full_node is a real pointer to a node in self which has 2 children
    @type empty_node: AVLNode
    @pre: empty_node is a real pointer to a node in self which has less than 2 children
    """
    def swap_nodes(self, full_node: AVLNode, empty_node: AVLNode):
        full_node.right.parent = empty_node
        full_node.left.parent = empty_node
        empty_node.right.parent = full_node
        empty_node.left.parent = full_node

        full_node.left, empty_node.left = empty_node.left, full_node.left
        full_node.right, empty_node.right = empty_node.right, full_node.right
        full_node.parent, empty_node.parent = empty_node.parent, full_node.parent
        full_node.auto_reset_height()
        empty_node.auto_reset_height()

        if empty_node == full_node.parent.left:
            full_node.parent.left = full_node
        else:
            full_node.parent.right = full_node

        if full_node is self.root:
            self.root = empty_node
        elif full_node == empty_node.parent.left:
            empty_node.parent.left = empty_node
        else:
            empty_node.parent.right = empty_node

    """deletes node from the dictionary

        @type node: AVLNode
        @pre: node is a real pointer to a node in self which has less than 2 children
        @rtype: AVLNode
        @returns: the node from which rebalancing operations should begin
        """
    def easy_delete(self, node: AVLNode):
        if node.right.is_real_node():
            new_node = node.right
        elif node.left.is_real_node():
            new_node = node.left
        else:
            new_node = AVLNode(None, None)
        start_node = node.parent
        new_node.parent = node.parent
        if node is self.root:
            self.root = new_node
        elif node.parent.left == node:
            node.parent.left = new_node
        else:
            node.parent.right = new_node
        node.left = None
        node.right = None
        node.key = None
        node.value = None
        node.parent = None
        return start_node

    """deletes node from the dictionary

    @type node: AVLNode
    @pre: node is a real pointer to a node in self
    @rtype: int
    @returns: the number of rebalancing operation due to AVL rebalancing
    """
    def delete(self, node):
        self.size -= 1
        if self.size == 0:
            self.root = AVLNode(None, None)
            return 0
        if node is self.min_node:
            if node is self.root:
                self.min_node = self.max_node
            else:
                self.min_node = node.parent
        elif node is self.max_node:
            if node is self.root:
                self.max_node = self.min_node
            else:
                self.max_node = node.parent
        if node.right.is_real_node() and node.left.is_real_node():
            current_node = node.right
            while current_node.left.is_real_node():
                current_node = current_node.left
            self.swap_nodes(node, current_node)

        start_node = self.easy_delete(node)
        return self.rebalance_tree(start_node, False)

    """returns an array representing dictionary by making and in-order tree journey

        @type node: AVLNode
        @param node: node is a real pointer to a node in self
        @rtype: AVLNode
        @returns: the successor of node or None if node has no successor
        """
    def successor(self, node):
        if node is self.max_node or not(node.is_real_node()) or node is None:
            return None
        if node.right.is_real_node():
            curr = node.right
            while curr.left.is_real_node():
                curr = curr.left
        else:
            curr = node
            while curr.parent is not None and curr is curr.parent.right:
                curr = curr.parent
            curr = curr.parent
        return curr

    """returns an array representing dictionary 

    @rtype: list
    @returns: a sorted list according to key of touples (key, value) representing the data structure
    """

    def avl_to_array(self):
        curr = self.min_node
        lst = []
        while curr:
            lst.append((curr.key, curr.value))
            curr = self.successor(curr)
        return lst

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
        smaller_tree = AVLTree.tree_from_root(node.get_left())
        bigger_tree = AVLTree.tree_from_root(node.get_right())

        parent = node.get_parent()
        while parent is not None:
            if node.is_left_son():
                right_subtree = AVLTree.tree_from_root(parent.get_right())
                bigger_tree.join(right_subtree, parent.get_key(), parent.get_value())
            else:  # node is right son
                left_subtree = AVLTree.tree_from_root(parent.get_left())
                left_subtree.join(smaller_tree, parent.get_key(), parent.get_value())
                smaller_tree = left_subtree

            parent.auto_reset_height()
            node = parent
            parent = node.get_parent()

        smaller_tree.fix_edges()
        bigger_tree.fix_edges()

        return [smaller_tree, bigger_tree]

    """joins self with key and another AVLTree

    @type tree2: AVLTree 
    @param tree2: a dictionary to be joined with self
    @type key: int 
    @param key: The key separating self with tree2
    @type val: any 
    @param val: The value attached to key
    @pre: all keys in self are smaller than key and all keys in tree2 are larger than key
    @rtype: int
    @returns: the absolute value of the difference between the height of the AVL trees joined
    """

    def join(self, tree2, key, val):
        tree1_height = self.root.get_height()
        tree2_height = tree2.root.get_height()
        connector = AVLNode(key, val)
        connector.set_right(AVLNode(None, None))
        connector.set_left(AVLNode(None, None))
        total_size = self.size + tree2.size + 1

        if tree2_height == -1:  # tree 2 is empty
            self.insert(key, val)
        elif tree1_height == -1:  # only self is empty
            tree2.insert(key, val)
            self.replace_tree(tree2)

        elif tree1_height == tree2_height:  # just connect the trees with connector
            connector.set_left(self.root)
            connector.set_right(tree2.root)
            self.root.set_parent(connector)
            tree2.root.set_parent(connector)
            self.root = connector
        elif tree1_height < tree2_height:  # join using min anchor from tree2
            anchor = tree2.get_anchor(tree1_height, is_min=True)
            connector.set_left(self.root)
            self.root.set_parent(connector)
            connector.set_right(anchor)
            if not anchor is tree2.root:
                anchor_parent = anchor.get_parent()
                connector.set_parent(anchor_parent)
                anchor_parent.set_left(connector)
            anchor.set_parent(connector)
            self.replace_tree(tree2)

        else:  # join using max anchor from tree1
            anchor = self.get_anchor(tree2_height, is_min=False)
            connector.set_right(tree2.root)
            tree2.root.set_parent(connector)
            connector.set_left(anchor)
            if not anchor is self.root:
                anchor_parent = anchor.get_parent()
                connector.set_parent(anchor_parent)
                anchor_parent.set_right(connector)
            anchor.set_parent(connector)

        # tree2.root = AVLNode(None, None)
        self.size = total_size
        self.rebalance_tree(connector, is_insert=True)
        self.fix_edges()

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

    def get_anchor(self, height: int, is_min) -> AVLNode:
        assert height < self.get_root().get_height()

        anchor = self.get_min() if is_min else self.get_max()
        while anchor.get_height() < height - 1:
            anchor = anchor.get_parent()
        return anchor

    def node_search(self, key):
        current_node = self.root
        while key != current_node.key and current_node.is_real_node():
            if current_node.key > key:
                current_node = current_node.left
            else:
                current_node = current_node.right

        if current_node.is_real_node():
            return current_node
        return None
