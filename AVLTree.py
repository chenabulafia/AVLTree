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
		self.height_changed = False

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
		self.root.left = AVLNode(None, None)
		self.root.right = AVLNode(None, None)
		self.max_node = self.root
		self.tree_size = 0
		self.bf0_count = 0


	"""searches for a node in the dictionary corresponding to the key

	@type key: int
	@param key: a key to be searched
	@rtype: AVLNode
	@returns: node corresponding to key
	"""
	def search(self, key: int):
		node = self.root
		while (node.is_real_node()):
			if node.key == key:
				return node
			
			if node.key < key:
				node = node.right
			else:
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
		node = AVLNode(key,val)
		node.left = AVLNode(None,None)
		node.right = AVLNode(None,None)
		if start == "max":
			new_node, height_changed = self.insert_from_max(node)
		elif start == "root":
			new_node, height_changed = self.insert_from_root(node)

		y = new_node.parent
		num_of_rotations = 0
		while (y is not None):
			left_height = y.left.height if y.left and y.left.is_real_node() else -1
			right_height = y.right.height if y.right and y.right.is_real_node() else -1
			y.bf = left_height - right_height
			abs_bf = abs(y.bf)
			if (abs_bf < 2) and (not height_changed):
				return 0
			if (abs_bf < 2) and (height_changed):
				y = y.parent
			if abs_bf >= 2:
				num_of_rotations += self.insert_rotations(y)
				y = y.parent

		return num_of_rotations

	def insert_from_root(self, new_node: AVLNode):
		if (not self.root.is_real_node()):
			self.root = new_node
			self.max_node = new_node
			self.tree_size = 1
			self.bf0_count = 1
			return new_node, False

		self._insert_node(self.root, new_node)
		if self.max_node.key < new_node.key:
			self.max_node = new_node
		
		height_changed = self._update_height_and_bf(new_node)
		return new_node, height_changed

	def insert_from_max(self, new_node: AVLNode):
		if (not self.max_node.is_real_node()):
			self.root = new_node
			self.max_node = new_node
			self.tree_size = 1
			self.bf0_count = 1
			return new_node, False

		if new_node.key > self.max_node.key:
			new_node.parent = self.max_node
			self.max_node.right = new_node
			self.max_node = new_node
		else:
			node = self.max_node
			while (node.key > new_node.key) and (node.key != self.root.key):
				node = node.parent
			
			self._insert_node(node, new_node)
		
		height_changed = self._update_height_and_bf(new_node)
		return new_node, height_changed
	
	def _insert_node(self, start_node: AVLNode, new_node: AVLNode):
		y = None
		x = start_node
		while x is not None and x.is_real_node():
			y = x
			if new_node.key < x.key:
				x = x.left
			else: 
				x = x.right
	
		new_node.parent = y
		new_node.left = AVLNode(None, None)
		new_node.right = AVLNode(None, None)
		new_node.height = 0

		if y is None:
			self.root = new_node
		elif new_node.key < y.key:
			y.left = new_node
		else:
			y.right = new_node
		
		if new_node.key > self.max_node.key:
			self.max_node = new_node

	def _update_height_and_bf(self, node: AVLNode):
		height_changed = False
		current = node
		while current is not None and current.is_real_node():
			old_height = current.height
			left_height = current.left.height if current.left.is_real_node() else -1
			right_height = current.right.height if current.right.is_real_node() else -1
			current.height = 1 + max(left_height,right_height)
			prev_bf = current.bf
			current.bf = left_height - right_height

			self._fix_bf_change(prev_bf, current.bf)

			if current.height != old_height:
				height_changed = True
			current = current.parent
		return height_changed
	
	def _fix_bf_change(self, prev, curr):
		if prev == 0 and curr != 0:
			self.bf0_count -= 1
		if prev != 0 and curr == 0:
			self.bf0_count += 1
			
	def insert_rotations(self, node: AVLNode):
		changes = 1
		if node.bf == 2:
			if node.left.bf == 1:
				self._right_rotation(node)
			elif node.left.bf == -1:
				self._left_rotation(node.left)
				self._right_rotation(node)
				changes = 2
		else:
			if node.right.bf == 1:
				self._right_rotation(node.right)
				self._left_rotation(node)
				changes = 2
			elif node.right.bf == -1:
				self._left_rotation(node)

		self._update_height_and_bf(node)
		return changes
	
	def delete_rotations(self, node: AVLNode):
		changes = 1
		if node.bf == 2:
			if node.left.bf >= 0:
				self._right_rotation(node)
			elif node.left.bf == -1:
				self._left_rotation(node.left)
				self._right_rotation(node)
				changes = 2
		else:
			if node.right.bf == 1:
				self._right_rotation(node.right)
				self._left_rotation(node)
				changes = 2
			elif node.right.bf <= 0:
				self._left_rotation(node)

		self._update_height_and_bf(node)
		return changes

	def _left_rotation(self, x: AVLNode):
		y = x.right
		x.right = y.left
		if y.left and y.left.is_real_node():
			y.left.parent = x
		y.parent = x.parent

		if x.parent is None:
			self.root = y
		elif x == x.parent.left:
			x.parent.left = y
		else:
			x.parent.right = y

		y.left = x
		x.parent = y
		self._update_height_and_bf(x)
		self._update_height_and_bf(y)

	def _right_rotation(self, y: AVLNode):
		x = y.left
		y.left = x.right
		if x.right and x.right.is_real_node():
			x.right.parent = y
		x.parent = y.parent

		if y.parent is None:
			self.root = x
		elif y == y.parent.right:
			y.parent.right = x
		else:
			y.parent.left = x

		x.right = y
		y.parent = x
		self._update_height_and_bf(y)
		self._update_height_and_bf(x)

	"""deletes node from the dictionary

	@type node: AVLNode
	@pre: node is a real pointer to a node in self
	@rtype: int
	@returns: the number of rebalancing operation due to AVL rebalancing
	"""
	def delete(self, node: AVLNode):
		self.tree_size -= 1
		self._delete_node(node)
		height_changed = self._update_height_and_bf(node.parent)
		y = node.parent
		num_of_rotations = 0
		
		while (y is not None):
			left_height = y.left.height if y.left and y.left.is_real_node() else -1
			right_height = y.right.height if y.right and y.right.is_real_node() else -1
			y.bf = left_height - right_height
			abs_bf = abs(y.bf)
			if (abs_bf < 2) and (not height_changed):
				return 0
			if (abs_bf < 2) and (height_changed):
				y = y.parent
			if abs_bf >= 2:
				num_of_rotations += self.delete_rotations(y)
				y = y.parent

		# Clear this node
		node.left = None
		node.right = None
		node.parent = None

		return num_of_rotations

	def _delete_node(self, node: AVLNode):
		if node.key == self.max_node.key:
			pred = self._get_predecessor(node)
			self.max_node = pred

		# Case I - leaf
		if node.height == 0:
			if node.parent.left.key == node.key:
				node.parent.left = AVLNode(None,None)
			elif node.parent.right.key == node.key:
				node.parent.right = AVLNode(None,None)
		
		# Case II - one child in right
		elif (not node.left.is_real_node()) and (node.right.is_real_node()):
			node.right.parent = node.parent
			if node.parent.left.key == node.key:
				node.parent.left = node.right
			elif node.parent.right.key == node.key:
				node.parent.right = node.right

		# Case II - one child in left
		elif (not node.right.is_real_node()) and (node.left.is_real_node()):
			node.left.parent = node.parent
			if node.parent.left.key == node.key:
				node.parent.left = node.left
			elif node.parent.right.key == node.key:
				node.parent.right = node.left

		# Case III - two children
		else:
			suc = self._get_successor(node)
			if suc.parent != node:
				if suc.right.is_real_node():
					suc.right.parent = suc.parent
				if suc.parent.left == suc:
					suc.parent.left = suc.right
				else:
					suc.parent.right = suc.right
				suc.right = node.right
				if suc.right.is_real_node():
					suc.right.parent = suc

			suc.left = node.left
			if suc.left.is_real_node():
				suc.left.parent = suc

			suc.parent = node.parent
			if node.parent is None:
				self.root = suc
			elif node.parent.left == node:
				node.parent.left = suc
			else:
				node.parent.right = suc

			self._update_height_and_bf(suc)

	def _get_successor(self, node: AVLNode):
		if node.right.is_real_node():
			node = node.right
			while node.left.is_real_node():
				node = node.left
			return node
		
		else:
			while not node.right.is_real_node():
				node = node.parent
			return node.right
		
	def _get_predecessor(self, node: AVLNode):
		if node.left.is_real_node():
			node = node.left
			while node.right.is_real_node():
				node = node.right
			return node
		
		else:
			while not node.left.is_real_node():
				node = node.parent
			return node.left

	"""returns an array representing dictionary 

	@rtype: list
	@returns: a sorted list according to key of touples (key, value) representing the data structure
	"""
	def avl_to_array(self):
		return self._rec_to_array(self.root)

	def _rec_to_array(self, node: AVLNode):
		if node is None:
			return []
		return self._rec_to_array(node.left) + [node.key] + self._rec_to_array(node.right)


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
		if self.root.is_real_node():
			return self.root
		return None

	"""gets amir's suggestion of balance factor
	@returns: the number of nodes which have balance factor equals to 0 devided by the total number of nodes
	"""
	def get_amir_balance_factor(self):
		return self.tree_size/self.bf0_count


	def print_tree(self):
		def _print(node, prefix="", is_left=True):
			if node is not None:
				_print(node.right, prefix+ ("|    " if is_left else "    "), False)
				print(prefix + ("|____" if is_left else "|----") + f"{node.key} (bf: {node.bf}, height: {node.height})")
				_print(node.left, prefix + ("    " if is_left else "|   "), True)

		_print(self.root)
