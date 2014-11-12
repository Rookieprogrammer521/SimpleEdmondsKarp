import Queue, copy
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

# Keeps track of the flow on the edge, maintains end points
class edge:
	# flow = capacity_back, capacity = capacity_back + capacity_forward
	def __init__(self, node_from, node_to, cap):
		self.capfor = cap
		self.capback = 0
		self.orig = node_from
		self.dest = node_to

	# Returns if you can go forward on the edge - to destination
	def go_for(self):
		return True if self.capfor > 0 else False

	# Returns if you can go backwards on the edge - to origin
	def go_back(self):
		return True if self.capback > 0 else False

	def __repr__(self):
		return str(self.orig) + ' to ' + str(self.dest)

# Main class defning the graph topology
class flow:
	# Initializes the network flow
	def __init__(self, cap_to_A, A, cap_to_B, B):
		
		# A has to have a param prefs which match up to name param in B
		self.source = source = node("SuperSource")
		self.sink = sink = node("SuperSink")

		self.b_nodes = b_nodes = []
		self.a_nodes = a_nodes = []

		# For every element in B, wrap it into a node, create edges to sink
		for b in B:
			bn = node(b)
			bn.add_edge(sink, cap_to_B)
			self.b_nodes.append(bn)

		# For every element in A, wrap it into a node, create edges from source, set edges to nodes in column B
		for a in A:
			n = node(a)
			self.a_nodes.append(n)
			source.add_edge(n, cap_to_A)

			for pref in a.prefs:
				b = self.find_in_b(pref, b_nodes)
				if b:
					n.add_edge(b, 1)

	def __repr__(self):		
		print self.source
		for e in self.source.edgesout:
			print '\t', 'to', e.dest, str(e.capback)+'/'+str(e.capback + e.capfor)

		for a in self.a_nodes:
			print a
			for e in a.edgesout:
				print '\t', 'to', e.dest, str(e.capback)+'/'+str(e.capback + e.capfor)
		
		for b in self.b_nodes:
			print b
			for e in b.edgesout:
				print '\t', 'to', e.dest, str(e.capback)+'/'+str(e.capback + e.capfor)


		return "----"

	# Find elements in b_nodes
	def find_in_b(self, value, b_nodes):
		for b in b_nodes:
			if value == b.data.name:
				return b
		return None

	# push flow through the path - no error checking, assumed path is legitimate, which is ensured by the BFS
	def push_flow(self, path, val):
		for i in range(len(path)-1):
			orig = path[i]
			dest = path[i+1]

			orig.push_flow(dest, val)

	# Finds shortest path through the residual graph, keeps track of length and path taken
	def BFS(self):
		q = Queue.Queue()
		q.put((self.source, 0, [self.source]))
		visited = []
		visited.append(self.source)

		while not q.empty():
			cur = q.get()

			if cur[0] == self.sink:
				return cur[1], cur[2]
			for (e,out) in cur[0].get_outward_edges():
				if out:
					if e.dest not in visited:
						path = list(cur[2])
						path.append(e.dest)
						q.put((e.dest, cur[1]+1, path))
						visited.append(e.dest)
				else:
					if e.orig not in visited:
						path = list(cur[2])
						path.append(e.orig)
						q.put((e.orig, cur[1]+1, path))
						visited.append(e.orig)

		return None

	# Runs Edmonds-Karp by finding the shortest path, pushign a flow of 1 through it until no more paths exist in the residual graph from s to t
	# Terminates in O(m^2 n), look up wiki for proof
	def get_max_flow(self):
		path = self.BFS()
		while path != None:
			self.push_flow(path[1], 1)
			path = self.BFS()

	# Returns list of all elements from column A with their matchings
	def get_all_a_matches(self):
		a_matches = {}
		for a in self.a_nodes:
			matches = a.get_b_matches()
			a_matches[a.data] = matches

		return a_matches

	# Returns list of all elements from column B with their matchings
	def get_all_b_matches(self):
		b_matches = {}
		for b in self.b_nodes:
			matches = b.get_a_matches()
			b_matches[b.data] = matches

		return b_matches

	# Returns max flow, i.e. how many assignments were successful, how many matches there are
	def max_flow_value(self):
		count = 0
		for e in self.source.edgesout:
			if e.go_back:
				count += 1
		return count