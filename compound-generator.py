class TreeNode:
	def __init__(self, data, parent = None):
		self.data = data #data being the sugar in this case
		self.children = [] #list to store children tree nodes
		self.parent = parent #place to store parent if applicable
		self.depth = 0 #depth just refers to length of the structure

	def addOdd(self, sugar):
		#root in this case is parent, sugar is potential child
		#odd sugar ruleset
		if sugar == 'GlcA2S':
			if self.data == 'GlcNS' and self.depth == 2 or self.depth == 0: 
			#GlcA2S mostly exists in 3rd position, but can potentially exist in 1st position so we have an edge case for it
				return 1
			else:
				return 0
		elif sugar == 'IdoA':
			if (self.data == 'GlcNS' or self.data == 'GlcNS6S') and self.depth == 2: #IdoA check only happens for 3rd position
				if self.parent.data != 'GlcA2S': 
					return 1
				else:
					return 0
			else:
				return 0
		elif sugar == 'IdoA2S':
			if (self.data == 'GlcNS' or self.data == 'GlcNS6S') and self.depth < (size - 3): #compounds can only end with GlcA
				if self.depth == 2: #to deal with GlcA2S 1st position edge case. We first check if we are at 3rd position
					if self.parent.data != 'GlcA2S': #check if 1st postion is GlcA2S for GlcA2S edge case
						return 1
					else:
						return 0
				else:
					return 1
			else:
				#this entire check is for the edge case where an IdoA2S can potentially transform 2 sites at around 50% yield.
				if (size == 7 or size == 9) and (self.data == 'GlcNS' or self.data == 'GlcNS6S') and self.depth < (size - 1) and self.parent.data != 'GlcA2S' and self.parent.data == 'IdoA2S':
					return 1
				else:
					return 0
		elif sugar == 'GlcA':
			if self.depth == 2: #refer to IdoA2S above for why this exists
				if self.parent.data != 'GlcA2S': #check if 1st position sugar for GlcA2S edge case since it cannot be GlcA-GlcNS-GlcA2S-Tag
					return 1
				else:
					return 0
			else:
				return 1

		else:
			return 0

	def addEven(self, sugar):
		#root in this case is parent, sugar is potential child
		#even sugar ruleset
		if sugar == 'GlcNAc':
			if self.data == 'GlcA':
				return 1
			else:
				return 0
		elif sugar == 'GlcNS':
			if (self.data == 'GlcA' or self.data == 'GlcA2S' or self.data == 'IdoA' or self.data == 'IdoA2S'):
				return 1
			else:
				return 0
		elif sugar == 'GlcNS6S':
			if (self.data == 'GlcA' or (self.data == 'GlcA2S' and self.depth > 3) or self.data == 'IdoA' or self.data == 'IdoA2S'):
				return 1
			else:
				return 0
		elif sugar == 'GlcNAc6S':
			if self.data == 'GlcA':
				return 1
			else:
				return 0
		elif sugar == 'GlcNS6S3S':
			if self.data == 'IdoA2S' and self.checkSulfation():
				return 1
			else:
				return 0

	def checkSulfation(self):
		#Function to through the path to see if there's a GlcNS6S3S
		if self.parent is not None:
			if self.data == 'GlcNS6S3S':
				return 0
			else:
				if self.parent.checkSulfation():
					return 1
		else:
			return 1

	def addChild(self, n):
		self.depth = n
		#determine which sugar to add. the n + 1 is there because we always start with an odd sugar
		if (n + 1) % 2 == 1: #if odd
			for oddSugar in odd:
				if self.addOdd(oddSugar):
					self.children.append(TreeNode(oddSugar, self))
		elif (n + 1) % 2 == 0: #if even
			for evenSugar in even:
				if self.addEven(evenSugar):
					self.children.append(TreeNode(evenSugar, self))
		
	def printTree(self, string = ""):
		#function to print tree in console. 
		if self.children:
			string += self.data + "-"
			for child in self.children:
				child.printTree(string)
		else:
			string += self.data
		if string.split('-').pop() == "":
		#check if last portion of string is ''. Will figure out why it keeps showing up at the end but until then this if statement is to catch it if it happens.
			return 0
		else:
		#only print if  longer than configed size
			if len(string.split('-')) > size:
				stringList = string.split('-')
				reverseList = stringList[::-1]
				print('-'.join(reverseList))

def buildTree(root, n = 0):
	#n represents the level of depth (aka structure length)
	if n == size:
		#ends tree building once n equals sign
		return 0
	else:	
		root.addChild(n)
		for child in root.children:
			buildTree(child, n + 1)
	return root

#odd sugars
odd = ['GlcA2S', 'GlcA', 'IdoA', 'IdoA2S']

#even sugars
even = ['GlcNAc6S', 'GlcNS6S', 'GlcNAc', 'GlcNS', 'GlcNS6S3S']

#config
size = 8 #length of a structure
tag = 'Az' #set initial tag

root = TreeNode(tag)
root = buildTree(root)
root.printTree()