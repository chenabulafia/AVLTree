#username - chenabulafia and zivaviv
#id1      - 323014001
#name1    - Chen Abulafia 
#id2      - 213784358
#name2    - Ziv Aviv



"""A class represnting a node in an AVL tree"""

class AVLNode(object):
	"""Constructor, you are allowed to add more fields. 
	
	@type key: int or None
	@param key: key of your node
	@type value: string
	@param value: data of your node
	"""
	def __init__(self, key, value):
		self.key = key
		self.value = value
		self.left = None
		self.right = None
		self.parent = None
		self.height = -1
		self.bf = 0
		

	"""returns whether self is not a virtual node 

	@rtype: bool
	@returns: False if self is a virtual node, True otherwise.
	"""
	def is_real_node(self):
		if self.key is None:
			return False
		return True



"""
A class implementing an AVL tree.
"""

class AVLTree(object):

	"""
	Constructor, you are allowed to add more fields.  

	"""
	def __init__(self):
		self.root = AVLNode(None, None)
		self.max = AVLNode(None, None)
		self.tree_size = 0 


	"""searches for a node in the dictionary corresponding to the key

	@type key: int
	@param key: a key to be searched
	@rtype: AVLNode
	@returns: node corresponding to key
	"""
	def search(self, key):
		node = self.root
		while (node.is_real_node()):
			if node.key == key:
				return node
			
			if node.key < key:
				node = node.right
			node = node.left
		return None


	"""inserts a new node into the dictionary with corresponding key and value

	@type key: int
	@pre: key currently does not appear in the dictionary
	@param key: key of item that is to be inserted to self
	@type val: string
	@param val: the value of the item
    @param start: can be either "root" or "max"
	@rtype: int
	@returns: the number of rebalancing operation due to AVL rebalancing
	"""
	def insert(self, key, val, start="root"):
		self.tree_size += 1
		if start == "max":
			new_node, heigth_changed = self.insert_from_max(key, val)
		if start == "root":
			new_node, heigth_changed = self.insert_from_root(key, val)

		node = new_node.parent
		num_of_rotations = 0
		while (node is not None) and (node.is_real_node()):
			abs_bf = abs(node.bf)
			if (abs_bf < 2) and (not heigth_changed):
				return 0
			if (abs_bf < 2) and (heigth_changed):
				node = node.parent
			if abs_bf == 2:
				num_of_rotations += self.rotations(node)
				node = node.parent

		return num_of_rotations

	def insert_from_max(self, key, val):
		heigth_changed = False
		new_node = AVLNode(key, val)
		new_node.left = AVLNode(None, None)
		new_node.right = AVLNode(None, None)
		
		if key > self.max:
			new_node.parent = self.max
			self.max.right = new_node
			self.max = new_node
		else:
			node = self.max
			while (node.key > key) and (node.key != self.root.key):
				node = node.parent
			
			while (node.is_real_node()):
				if node.key < key:
					node = node.right
				node = node.left
		
			node = node.parent
			new_node.parent = node
			if (not node.left.is_real_node()) and (not node.right.is_real_node()):
				heigth_changed = True
				self._update_height_and_bf(node)
			if key > node.key:
				node.right = new_node
			else:
				node.left = new_node
		
		return new_node, heigth_changed

	def insert_from_root(self, key, val):
		heigth_changed = False
		new_node = AVLNode(key, val)
		new_node.left = AVLNode(None, None)
		new_node.right = AVLNode(None, None)

		new_node.right.parent = new_node
		new_node.left.parent = new_node
		node = self.root
		
		if not self.root.is_real_node():
			self.root = new_node
			# self.root.left.parent = self.root
			# self.root.right.parent = self.root
			return new_node, heigth_changed
		
		while (node.is_real_node()):
			if node.key < key:
				node = node.right
			node = node.left
		
		node = node.parent
		new_node.parent = node
		if (not node.left.is_real_node()) and (not node.right.is_real_node()):
			heigth_changed = True
			self._update_height_and_bf(node)
		if key > node.key:
			node.right = new_node
		else:
			node.left = new_node

		return new_node, heigth_changed

	def _update_height_and_bf(self, node):
		while (node.parent is not None):
			node.height = max(node.left.heigth, node.right.heigth) + 1
			node.bf = (node.left.heigth - node.right.heigth)

			node = node.parent

	def rotations(self, node):
		changes = 1
		if node.bf == 2:
			if node.left.bf == 1:
				self._right_rotation(node)
			else:
				self._left_rotation(node)
				self._right_rotation(node)
				changes = 2
		else:
			if node.left.bf == 1:
				self._right_rotation(node)
				self._left_rotation(node)
				changes = 2
			else:
				self._left_rotation(node)

		self._update_height_and_bf(node)
		return changes
		
	def _left_rotation(self, node):
		node.left = node.left.right
		node.left.parent = node
		node.left.right = node
		node.left.parent = node.parent 
		node.left.parent.right = node.left
		node.parent = node.left

	def _right_rotation(self, node):
		node.left = node.left.right
		node.left.parent = node
		node.left.right = node
		node.left.parent = node.parent 
		node.left.parent.left = node.left
		node.parent = node.left

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
		return self.tree_size


	"""returns the root of the tree representing the dictionary

	@rtype: AVLNode
	@returns: the root, None if the dictionary is empty
	"""
	def get_root(self):
		return self.root

	"""gets amir's suggestion of balance factor
	@returns: the number of nodes which have balance factor equals to 0 devided by the total number of nodes
	"""
	def get_amir_balance_factor(self):
		return None


	def print_tree(self):
		def _print(node, prefix="", is_left=True):
			if node is not None:
				_print(node.right, prefix+ ("|   " if is_left else "     "), False)
				print(prefix + ("|____" if is_left else "|----") + str(node.key))
				_print(node.left, prefix + ("    " if is_left else "|   "), True)

		_print(self.root)

def check():
	l = [7,6,12,4,10,9,13,18,3]
	t = AVLTree()
	for i in l:
		t.insert(i, "a", "root")
		t.print_tree()
	

check()