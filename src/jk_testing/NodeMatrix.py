import os
import sys
import subprocess

import copy
import graphviz

import jk_temporary




class GraphCycleError(Exception):

	def __init__(self, data):
		self.data = data
	#

#



class NodeMatrix(object):

	def __init__(self, nodeObjs = None):
		self.__nodeObjs = []
		self.__nodeObjIDsToIndex = {}
		self.__statusNodeProcessed = []
		self.__statusIncomingNodesToProcess = []
		self.__countIncomingNodes = []
		self.__countOutgoingNodes = []
		self.__matrix = []
		self.__count = 0

		if nodeObjs:
			self.addNodes(nodeObjs)
	#

	@property
	def size(self):
		return self.__count
	#

	def nodes(self):
		return tuple(self.__nodeObjs)
	#

	def addNode(self, nodeObj):
		assert nodeObj is not None

		self.__nodeObjIDsToIndex[id(nodeObj)] = self.__count
		self.__nodeObjs.append(nodeObj)
		self.__statusNodeProcessed.append(False)
		self.__statusIncomingNodesToProcess.append(0)
		self.__countIncomingNodes.append(0)
		self.__countOutgoingNodes.append(0)

		for row in self.__matrix:
			row.append(False)
		self.__count += 1
		newRow = [ False ] * self.__count
		self.__matrix.append(newRow)
	#

	def addNodes(self, nodeObjs):
		assert isinstance(nodeObjs, (tuple, list))

		countAdditional = len(nodeObjs)
		if countAdditional == 0:
			return

		for nodeObj in nodeObjs:
			assert nodeObj is not None

		i = 0
		for nodeObj in nodeObjs:
			self.__nodeObjIDsToIndex[id(nodeObj)] = self.__count + i
			i += 1
		self.__nodeObjs.extend(nodeObjs)
		self.__statusIncomingNodesToProcess.extend([ 0 ] * len(nodeObjs))
		self.__statusNodeProcessed.extend([ True ] * len(nodeObjs))
		self.__countIncomingNodes.extend([ 0 ] * len(nodeObjs))
		self.__countOutgoingNodes.extend([ 0 ] * len(nodeObjs))

		for row in self.__matrix:
			for j in range(0, countAdditional):
				row.append(False)
		self.__count += countAdditional
		for j in range(0, countAdditional):
			newRow = [ False ] * self.__count
			self.__matrix.append(newRow)
	#

	def set(self, fromNode, toNode, bHasEdge:bool):
		assert fromNode is not None
		assert toNode is not None
		assert isinstance(bHasEdge, bool)

		nFrom = self.__nodeObjIDsToIndex[id(fromNode)]
		#nFrom = self.__nodeObjs.index(fromNode)
		nTo = self.__nodeObjIDsToIndex[id(toNode)]
		#nTo = self.__nodeObjs.index(toNode)

		bAlreadyHasEdge = self.__matrix[nFrom][nTo]
		if bAlreadyHasEdge == bHasEdge:
			return

		self.__matrix[nFrom][nTo] = bHasEdge
		if bHasEdge:
			self.__countIncomingNodes[nTo] += 1
			self.__countOutgoingNodes[nFrom] += 1
		else:
			self.__countIncomingNodes[nTo] -= 1
			self.__countOutgoingNodes[nFrom] -= 1
	#

	def get(self, fromNode, toNode):
		assert fromNode is not None
		assert toNode is not None

		nFrom = self.__nodeObjIDsToIndex[id(fromNode)]
		#nFrom = self.__nodeObjs.index(fromNode)
		nTo = self.__nodeObjIDsToIndex[id(toNode)]
		#nTo = self.__nodeObjs.index(toNode)

		return self.__matrix[nFrom][nTo]
	#

	#
	# Analyses the graph. Detect cylces and determine the order of execution.
	#
	# If a cycle is detected a <c>GraphCycleError</c> is raised. The argument for the exception is the node that has been identified
	# as part of a cycle.
	#
	# @param		callable debugWriteFunction		A function to invoke to output debug messages.
	#												<c>None</c> is specified by default in order to deactivate this feature.
	#												For example you can use <c>print</c> as argument here to write to STDOUT.
	# @return		obj[]		Returns the node objects in the correct order (if no error occurred).
	#
	def determineOrder(self, debugWriteFunction=None):
		bNodeCompleted = [ False ] * self.__count
		nIncomingEdgesLeft = copy.deepcopy(self.__countIncomingNodes)
		nodeValues = [ None ] * self.__count
		indicesOfNodesNotYetProcessed = set(range(0, self.__count))

		listOfRootNodes = self.__getNodeIndicesWithoutIncomingEdges()
		if len(listOfRootNodes) == 0:
			raise Exception("No root node(s)!")

		currentGen = listOfRootNodes
		orderIndex = 1
		retDict = {}
		while len(currentGen) > 0:
			if debugWriteFunction:
				debugWriteFunction("Now processing this generation of nodes: " + str(self.__i2n(currentGen)))
			nextGen = set()
			for n in currentGen:
				currentNode = self.__nodeObjs[n]
				if debugWriteFunction:
					debugWriteFunction("\tLooking at node: " + str(currentNode) + ", index " + str(n))
				if bNodeCompleted[n]:
					if debugWriteFunction:
						debugWriteFunction("\t\tNode is already completed. Skipping")
					#raise GraphCycleError(currentNode)
				elif nIncomingEdgesLeft[n] > 0:
					if debugWriteFunction:
						debugWriteFunction("\t\tNode has more than one unprocessed incoming edges. Skipping.")
					pass
				else:
					# this is the last edge: process this node
					if debugWriteFunction:
						debugWriteFunction("\t\tNode has zero unprocessed incoming edges => Now procesing this node.")
					nodeValues[n] = orderIndex
					if debugWriteFunction:
						debugWriteFunction("\t\tMarking node as completed: " + str(currentNode))
					bNodeCompleted[n] = True
					outgoingNodeIndices = self.__getOutgoingIndices(currentNode)
					if debugWriteFunction:
						debugWriteFunction("\t\tNode has outgoing edges to nodes: " + str(self.__i2n(outgoingNodeIndices)))
					for i in outgoingNodeIndices:
						nextGen.add(i)
						if debugWriteFunction:
							debugWriteFunction("\t\tReducing unprocessed edge count of node " + str(self.__nodeObjs[i])
								+ " from " + str(nIncomingEdgesLeft[i]) + " to " + str(nIncomingEdgesLeft[i] - 1)) 
						nIncomingEdgesLeft[i] -= 1
					retDict[orderIndex] = currentNode
					orderIndex += 1
					indicesOfNodesNotYetProcessed.remove(n)
			currentGen = nextGen

		if indicesOfNodesNotYetProcessed:
			# there are unprocessed nodes. that means: we did not reach all nodes! => cycle
			for i in indicesOfNodesNotYetProcessed:
				if nIncomingEdgesLeft[i] > 0:
					raise GraphCycleError(self.__nodeObjs[i])

		return [ retDict[i] for i in range(1, self.__count + 1) ]
	#

	def __i2n(self, indices):
		return [ self.__nodeObjs[i] for i in indices ]
	#

	def getNodesWithoutIncomingEdges(self):
		ret = []

		for n in range(0, self.__count):
			bHasIncoming = False
			for i in range(0, self.__count):
				if self.__matrix[i][n]:
					bHasIncoming = True
					break
			if not bHasIncoming:
				ret.append(self.__nodeObjs[n])

		return ret
	#

	def __getNodeIndicesWithoutIncomingEdges(self):
		ret = []

		for n in range(0, self.__count):
			bHasIncoming = False
			for i in range(0, self.__count):
				if self.__matrix[i][n]:
					bHasIncoming = True
					break
			if not bHasIncoming:
				ret.append(n)

		return ret
	#

	def getNodesWithoutOutgoingEdges(self):
		ret = []

		for n in range(0, self.__count):
			row = self.__matrix[n]
			bHasOutgoing = False
			for i in range(0, self.__count):
				if row[i]:
					bHasOutgoing = True
					break
			if not bHasOutgoing:
				ret.append(self.__nodeObjs[n])

		return ret
	#

	def __getNodeIndicesWithoutOutgoingEdges(self):
		ret = []

		for n in range(0, self.__count):
			row = self.__matrix[n]
			bHasOutgoing = False
			for i in range(0, self.__count):
				if row[i]:
					bHasOutgoing = True
					break
			if not bHasOutgoing:
				ret.append(n)

		return ret
	#

	def getOutgoing(self, fromNode):
		assert fromNode is not None

		# n = self.__nodeObjs.index(fromNode)
		n = self.__nodeObjIDsToIndex[id(fromNode)]

		ret = []
		row = self.__matrix[n]
		for i in range(0, self.__count):
			if row[i]:
				ret.append(self.__nodeObjs[i])
		return ret
	#

	def __getOutgoingIndices(self, fromNode):
		assert fromNode is not None

		# n = self.__nodeObjs.index(fromNode)
		n = self.__nodeObjIDsToIndex[id(fromNode)]

		ret = []
		row = self.__matrix[n]
		for i in range(0, self.__count):
			if row[i]:
				ret.append(i)
		return ret
	#

	def getIncoming(self, toNode):
		assert toNode is not None

		# n = self.__nodeObjs.index(toNode)
		n = self.__nodeObjIDsToIndex[id(toNode)]

		ret = []
		for i in range(0, self.__count):
			if self.__matrix[i][n]:
				ret.append(self.__nodeObjs[i])
		return ret
	#

	def __getIncomingIndices(self, toNode):
		assert toNode is not None

		# n = self.__nodeObjs.index(toNode)
		n = self.__nodeObjIDsToIndex[id(toNode)]

		ret = []
		for i in range(0, self.__count):
			if self.__matrix[i][n]:
				ret.append(i)
		return ret
	#

	def convertTo(self, targetFormat:str, nodeColoringCallback = None):
		return _NODE_MATRIX_CONVERTER.convert(self, targetFormat, nodeColoringCallback=nodeColoringCallback)
	#

#



class _GraphVizConverter(object):

	@property
	def formats(self):
		return [ "png", "svg", "dot" ]
	#

	def convert(self, nodeMatrix:NodeMatrix, targetFormat:str, tempDirPath:str, nodeColoringCallback):
		assert isinstance(nodeMatrix, NodeMatrix)
		assert isinstance(targetFormat, str)
		assert isinstance(tempDirPath, str)

		ret = [
			"strict digraph {",
			"\trankdir=LR;"
			#"\trankdir=TB;"
		]

		ret.append("")

		allNodes = nodeMatrix.nodes()

		for n, node in enumerate(allNodes):
			s = "\t" + str(n) + " [ label=\"" + str(node) + "\""
			if nodeColoringCallback:
				bgColor, textColor, lineColor = nodeColoringCallback(node)
				if bgColor:
					s += " style=filled fillcolor=\"" + bgColor + "\""
				if textColor:
					s += " fontcolor=\"" + textColor + "\""
				if lineColor:
					s += " color=\"" + lineColor + "\""
			s += " ]"
			ret.append(s)

		ret.append("")

		for nFrom, fromNode in enumerate(allNodes):
			toNodes = nodeMatrix.getOutgoing(fromNode)
			for toNode in toNodes:
				nTo = allNodes.index(toNode)
				ret.append("\t" + str(nFrom) + " -> " + str(nTo))

		ret.append("}")
		graphVizSource = "\n".join(ret)
		tmpFilePath = jk_temporary.createTempFilePath(baseDirPath=tempDirPath, postfix=".dot")
		with open(tmpFilePath, "w") as f:
			f.write(graphVizSource)

		if targetFormat == "dot":
			return tmpFilePath
		else:
			resultFilePath = graphviz.render("dot", targetFormat, tmpFilePath)
			os.unlink(tmpFilePath)
			return resultFilePath
	#

#



class NodeMatrixConverterMgr(object):

	def __init__(self, tempDirPath:str = "/tmp"):
		if tempDirPath:
			assert isinstance(tempDirPath, str)
			assert os.path.isdir(tempDirPath)
			self.__tempDirPath = tempDirPath
		else:
			self.__tempDirPath = "/tmp"

		self.__formatMap = {}
	#

	def register(self, converter):
		for outputFormat in converter.formats:
			if outputFormat not in self.__formatMap:
				self.__formatMap[outputFormat] = converter
	#

	def convert(self, nodeMatrix:NodeMatrix, targetFormat:str, nodeColoringCallback = None):
		assert isinstance(nodeMatrix, NodeMatrix)
		assert isinstance(targetFormat, str)
		if nodeColoringCallback:
			assert callable(nodeColoringCallback)

		converter = self.__formatMap.get(targetFormat, None)
		if converter:
			return converter.convert(nodeMatrix, targetFormat, self.__tempDirPath, nodeColoringCallback)
		else:
			raise Exception("No conveter available for format: " + targetFormat)
	#

#



_NODE_MATRIX_CONVERTER = NodeMatrixConverterMgr()
_NODE_MATRIX_CONVERTER.register(_GraphVizConverter())





