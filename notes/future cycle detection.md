Determine Order of test cases

collect all nodes that produce variables
	- if two nodes produce the same variable => ERROR
	- create register of varName -> node

collect all nodes that consume variables
	- if a node requests a variable that is not provided => error
	- create dependency for these nodes to the node that produces the variable

complete graph
	pick root node
	insert every node into the graph
		if the node has no predecessor -> put into list of root nodes

detect cycles
	build register for every node: node -> int
	algorithm:
		for all nodes: set node.n = 0

		currentNodes = pick all root nodes (= nodes that have no predecessor)
		i = 1
		while len(currentNodes) > 0:
			nextNodes = []
			for all node in currentNodes:
				if node.n == 0:
					node has not yet been visited; process this node;
					node.n = i
					extend nextNodes with node.children
				elif node.n < i:
					node has already been visited; skip this node;
				else:
					node has already been visited; skip this node;
					=> ERROR: this is a cycle!
			i += 1
			currentNodes = nextNodes

		if nodes have not been marked => ERROR: this is an unrelated cycle!








