# username - complete info
# id1      - complete info
# name1    - complete info
# id2      - complete info
# name2    - complete info


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
        return None

    """returns the right child

	@rtype: AVLNode
	@returns: the right child of self, None if there is no right child (if self is virtual)
	"""

    def get_right(self):
        return None

    """returns the parent 

	@rtype: AVLNode
	@returns: the parent of self, None if there is no parent
	"""

    def get_parent(self):
        return None

    """returns the value

	@rtype: any
	@returns: the value of self, None if the node is virtual
	"""

    def get_value(self):
        return None

    """returns the height

	@rtype: int
	@returns: the height of self, -1 if the node is virtual
	"""

    def get_height(self):
        return -1

    """sets left child

	@type node: AVLNode
	@param node: a node
	"""

    def set_left(self, node):
        return None

    """sets right child

	@type node: AVLNode
	@param node: a node
	"""

    def set_right(self, node):
        return None

    """sets parent

	@type node: AVLNode
	@param node: a node
	"""

    def set_parent(self, node):
        return None

    """sets value

	@type value: any
	@param value: data
	"""

    def set_value(self, value):
        return None

    """sets the balance factor of the node

	@type h: int
	@param h: the height
	"""

    def set_height(self, h):
        return None

    """auto-rests the height of the tree when activated

		@type h: int
		@param h: the height
		"""

    def auto_reset_height(self):
        self.height = max(self.right.height, self.left.height) + 1

    """returns whether self is not a virtual node 

	@rtype: bool
	@returns: False if self is a virtual node, True otherwise.
	"""

    def is_real_node(self):
        return False


"""
A class implementing the ADT Dictionary, using an AVL tree.
"""


class AVLTree(object):
    """
	Constructor, you are allowed to add more fields.  

	"""

    def __init__(self):
        self.root = None
        self.size = 0
        self.min_node = None
        self.max_node = None

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

        if current_node.key.is_real_node():
            return current_node.value
        return None

	"""checks a certain path among the tree in order to rebalance the tree using right and left edge rotations
    
    @type start_node: AVLNode
    @pre: start_node is a real pointer to a node in self, from which the rebalance check will begin
    @rtype: int
    @returns: the number of rebalancing operation due to AVL rebalancing
    """
	def rebalance_tree(self, start_node: AVLNode, is_insert: boolean):
		rotations = 0
		current_node = start_node
		while current_node.is_real_node() and  not(rotations == 1 and is_insert):
			if current_node.right.height - current_node.left.height > 1:
				rotate_right(current_node)
				rotations += 1
			elif current_node.left.height - current_node.right.height > 1:
				rotate_left(current_node)
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
        self.size += 1
    	new_node = AVLNode(key, val)
        if key > self.max_node.key:
            new_node.parent = self.max_node
            max_node.parent.right = new_node
            self.max_node = new_node
        elif key < self.min_node.key:
            new_node.parent = self.min_node
            min_node.parent.left = new_node
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
        return rebalance_tree(new_node.parent, True)

    """deletes node from the dictionary

	@type node: AVLNode
	@pre: node is a real pointer to a node in self
	@rtype: int
	@returns: the number of rebalancing operation due to AVL rebalancing
	"""

    def delete(self, node):
        self.size -= 1
        if not(node.right.is_real_node() or node.left.is_real_node()):
            start_node = node.parent
            if node.parent.left == node:
                node.parent.left = AVLNode(None, None)
                node.parent.left.parent = node.parent
            else:
                node.parent.right = AVLNode(None, None)
                node.parent.right.parent = node.parent
        else:
            current_node = node.right
            while not(current_node.left.is_real_node()):
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
        return rebalance_tree(start_node, False)

	"""returns an array representing dictionary by making and in-order tree journey
	
		@type node: AVLNode
		@param node: The current node we are visiting during the in-order journey through the tree
		@rtype: list
		@returns: a sorted list according to key of touples (key, value) representing the data structure
		"""
	def avl_to_array_help(self, current_node: AVLNode):
		if current_node.is_real_node():
			return avl_to_array_help(current_node.left) + [(current_node.key, current_node.value)] + avl_to_array_help(current_node.right)
		return []

    """returns an array representing dictionary 

	@rtype: list
	@returns: a sorted list according to key of touples (key, value) representing the data structure
	"""

    def avl_to_array(self):
        return avl_to_array_help(self.root)

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

    def split(self, node):
        return None

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
        return None

    """returns the root of the tree representing the dictionary

	@rtype: AVLNode
	@returns: the root, None if the dictionary is empty
	"""

    def get_root(self):
        return self.root
