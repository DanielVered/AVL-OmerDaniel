#username - complete info
#id1      - 211399969
#name1    - Daniel Vered
#id2      - complete info
#name2    - complete info


"""A class represnting a node in an AVL tree"""


class AVLNode(object):
	"""Constructor, you are allowed to add more fields.

	@type value: any
	@param value: data of your node
	"""
	def __init__(self, key, value):
		self.key = key
		self.value = value
		self.left = None
		self.right = None
		self.parent = None
		self.height = -1  # Balance factor

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

	"""returns whether self is not a virtual node 

	@rtype: bool
	@returns: False if self is a virtual node, True otherwise.
	"""
	def is_real_node(self):
		has_children = self.right or self.left
		has_parent = self.parent
		return has_children or has_parent

"""
A class implementing the ADT Dictionary, using an AVL tree.
"""


class AVLTree(object):

	"""
	Constructor, you are allowed to add more fields.  

	"""
	def __init__(self):
		self.root: AVLNode = None
		self.size = 0
		self.min_node = None
		self.max_node = None

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

	"""set pointer to max node of the AVLTree.

		@returns: None.
		"""
	def set_max(self, node: AVLNode):
		self.max_node = node

	"""set pointer to min node of the AVLTree.

		@returns: None.
		"""
	def set_min(self, node: AVLNode):
		self.min_node = node

	def set_root(self, node: AVLNode):
		self.root = node
		return None

	def rotate_left(self, parent: AVLNode, son: AVLNode):
		return None

	def rotate_right(self, parent: AVLNode, son: AVLNode):
		return None

	"""searches for a value in the dictionary corresponding to the key

	@type key: int
	@param key: a key to be searched
	@rtype: any
	@returns: the value corresponding to key.
	"""
	def search(self, key):
		return None

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
		return -1


	"""deletes node from the dictionary

	@type node: AVLNode
	@pre: node is a real pointer to a node in self
	@rtype: int
	@returns: the number of rebalancing operation due to AVL rebalancing
	"""
	def delete(self, node):
		return -1


	"""returns an array representing dictionary 

	@rtype: list
	@returns: a sorted list according to key of touples (key, value) representing the data structure
	"""
	def avl_to_array(self):
		return None


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

	"""returns the root of the tree representing the dictionary

	@rtype: AVLNode
	@returns: the root, None if the dictionary is empty
	"""
	def get_root(self):
		return self.root
