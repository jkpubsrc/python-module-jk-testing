
from NodeMatrix import *









class Node(object):

	def __init__(self, name:str):
		self.name = name
	#

	def __str__(self):
		return self.name
	#

	def __repr__(self):
		return self.name
	#

#

r = Node("R")
a = Node("A")
b = Node("B")
c = Node("C")
d = Node("D")
e = Node("E")
f = Node("F")
g = Node("G")
h = Node("H")
i = Node("I")
j = Node("J")
k = Node("K")
l = Node("L")
m = Node("M")
n = Node("N")
o = Node("O")
p = Node("P")

nodes = [	r, a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p	]
nodeDict = {	node.name: node for node in nodes	}

links = [
	"AB",
	"AE",
	"AC",
	"OG",
	"EF",
	"CF",
	"FK",
	"FL",
	"FI",
	"IJ",
	"IK",
	"KM",
	"FH",
	"HN",
	"NL",
	"LH",	# cycle
	"LP",
	"AH",
]

matrix = NodeMatrix(nodes)
for link in links:
	matrix.set(nodeDict[link[0]], nodeDict[link[1]], True)

resultFile = matrix.convertTo("svg")
subprocess.Popen(["nohup", "/usr/bin/viewnior", resultFile], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

matrix.determineOrder(debugWriteFunction=print)

