# Node class containing a collection of edges going in and edges going out - bidirectional in order to implement residual graphs for max flow
# Payload is the wrapper class instance, i.e. student
class node:
	def __init__(self, payload):
		self.data = payload
		self.edgesout = []
		self.edgesin = []

	# Adds an edge out of this node with capacity cap, creates a pseudo back edge with capacity 0
	def add_edge(self, dest, cap):
		e = edge(self, dest, cap)

		self.edgesout.append(e)
		dest.edgesin.append(e)

	# Pushes a flow through a path, updates flow values accordingly
	def push_flow(self, dest, val):
		e, out = self.find_edge(dest)
		if out:
			e.capfor -= val
			e.capback += val
		else:
			e.capback -= val
			e.capfor += val

	# Looks through edges leaving node or entering node for any connection between itself and dest
	def find_edge(self, dest):
		for e in self.edgesout:
			if e.dest == dest:
				return e, True
		for e in self.edgesin:
			if e.orig == dest:
				return e, False
		return None, None

	# Used for BFS, returns all edges that can be traversed in residual graph
	def get_outward_edges(self):
		ret = []
		for e in self.edgesout:
			if e.go_for():
				ret.append((e, True))
		for e in self.edgesin:
			if e.go_back():
				ret.append((e, False))

		return ret

	# Gets all edges with positive flow coming out of column A going to column B for node in column A
	def get_b_matches(self):
		matches = []
		for e in self.edgesout:
			if e.go_back():
				matches.append(e.dest)
		return matches

	# Gets all edges with positive flow coming out of column A going to column B for node in column B
	def get_a_matches(self):
		matches = []
		for e in self.edgesin:
			if e.go_back():
				matches.append(e.orig)
		return matches

	def __repr__(self):
		return str(self.data)