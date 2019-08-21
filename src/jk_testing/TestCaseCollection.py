#!/usr/bin/env python3
# -*- coding: utf-8 -*-



import time
import collections
import typing

import jk_logging

from .Annotations import *
from .TestCaseInstance import *
from .NodeMatrix import *
from .SingleLookAtQueue import *





class TestCaseCollection(object):

	def __init__(self,
		allTestCases:typing.Sequence,
		nodeMatrix:NodeMatrix,
		rootNode:TestCaseInstance,
		enabledTestCasesToRunInDefinedOrder:typing.Sequence):

		assert isinstance(allTestCases, (tuple, list, set))
		assert isinstance(nodeMatrix, NodeMatrix)
		assert isinstance(rootNode, TestCaseInstance)
		assert isinstance(enabledTestCasesToRunInDefinedOrder, (tuple, list))

		self.__allTestCases = allTestCases
		self.__nodeMatrix = nodeMatrix
		self.__rootNode = rootNode
		self.__enabledTestCasesToRunInDefinedOrder = enabledTestCasesToRunInDefinedOrder
	#

	@property
	def _nodeMatrix(self):
		return self.__nodeMatrix
	#

	@property
	def isFailed(self):
		return self.__enabledTestCasesToRunInDefinedOrder is None
	#

	@property
	def isReady(self):
		return self.__enabledTestCasesToRunInDefinedOrder is not None
	#

	@property
	def allTestCases(self):
		return self.__allTestCases
	#

	@property
	def enabledTestCasesToRunInDefinedOrder(self):
		return self.__enabledTestCasesToRunInDefinedOrder
	#

	#
	# Derives test case instances from the function.
	#
	@staticmethod
	def __parseTestCallable(theCallable:collections.Callable, bEnabled:bool) -> TestCaseInstance:
		if not callable(theCallable):
			raise Exception("Not a callable: " + repr(theCallable))
		assert isinstance(bEnabled, bool)

		bIsObject = True
		orgObj = None
		try:
			theCallable.__name__ == "TestCaseWrapper"
			bIsObject = False
		except:
			pass

		if bIsObject:
			orgObj = theCallable
			theCallable = theCallable.__call__

		if theCallable.__name__ == "TestCaseWrapper":
			testCaseAspects, testCaseName = theCallable(False)

			if bIsObject:
				newTestCaseName = None
				try:
					newTestCaseName = orgObj.name()
				except:
					pass
				if newTestCaseName is None:
					try:
						newTestCaseName = orgObj.name
					except:
						pass
				if newTestCaseName:
					testCaseName = newTestCaseName
				else:
					objName = theCallable.__class__.__name__
					if testCaseName == "__call__":
						testCaseName = objName
					else:
						testCaseName = objName + "." + testCaseName

			return TestCaseInstance(False, testCaseName, testCaseAspects, theCallable, bEnabled)
		else:
			# NOTE: we accept methods as well that are not a test case
			# TODO: is that reasonable?
			testCaseName = str(theCallable.__name__)
			return TestCaseInstance(False, testCaseName, None, theCallable, bEnabled)
	#

	#
	# This method creates a test case collection. While doing so various checks are performed, required test cases
	# will get enabled that might not have been enabled yet and cycles are detected. The order in which the tests
	# can be run will be determined.
	#
	# @param		list testsToRunTuples	A list of test functions to execute or a list of tuples with test functions and boolean enabled/disabled flag.
	# @return		TestCaseCollection		Returns a test case collection object. Please note that if cycles are detected
	#										a test case collection will be returned as well which then will be marked as
	#										being erroneous. Use <c>testCaseCollection.isReady</c> or
	#										<c>testCaseCollection.isFailed</c> to detect this.
	#
	@staticmethod
	def compile(testsToRunTuples:list, log = None):
		if len(testsToRunTuples) == 0:
			raise Exception("No tests specified!")

		if isinstance(testsToRunTuples, (tuple, list)):
			if callable(testsToRunTuples[0]):
				testsToRunTuples = [ (x, True) for x in testsToRunTuples ]

		# build all test case instances

		if log:
			log.info("Creating test case instances ...")

		allTestCases = []
		allTestCasesByName = {}
		allTestCasesByProvidedVariables = {}
		for testCallable, bEnabled in testsToRunTuples:
			testCaseInstance = TestCaseCollection.__parseTestCallable(testCallable, bEnabled)
			if testCaseInstance.name in allTestCasesByName:
				raise Exception("Duplicate test cases: " + testCaseInstance.name)
			allTestCasesByName[testCaseInstance.name] = testCaseInstance
			allTestCases.append(testCaseInstance)
			for aspect in testCaseInstance.testCaseAspects:
				if isinstance(aspect, ProvidesVariable):
					if aspect.varName in allTestCasesByProvidedVariables:
						raise Exception("Two test cases provide the same variable " + repr(aspect.varName) + ": "
							+ repr(testCaseInstance.name) + " and " + repr(allTestCasesByProvidedVariables[aspect.varName].name))
					allTestCasesByProvidedVariables[aspect.varName] = testCaseInstance

		# add all test cases to the graph

		log2 = log.descend("Building graph of test cases ...") if log else None

		rootNode = TestCaseInstance(True, None, None, None, None)
		nodeMatrix = NodeMatrix()
		nodeMatrix.addNode(rootNode)
		nodeMatrix.addNodes(allTestCases)
		for i in range(0, len(allTestCases)):
			nodeMatrix.set(rootNode, allTestCases[i], True)

		# add all dependencies to the graph

		testCasesToActivate = SingleLookAtQueue()
		for a in allTestCases:
			for aspect in a.testCaseAspects:

				# A.runBefore(B) =>		A -> B
				if isinstance(aspect, RunBefore):
					b = allTestCasesByName.get(aspect.testName, None)
					if b is None:
						if log2:
							log2.error("Test case '" + testCaseInstance.name + "' refers to a non-existing test case named '" + aspect.testName + "'!")
						return False
					if log2:
						log2.notice("Constraint: Test case " + repr(a.name) + " should run before test case " + repr(b.name) + ".")
					nodeMatrix.set(a, b, True)

				# A.runAfter(B) =>		B -> A
				elif isinstance(aspect, RunAfter):
					b = allTestCasesByName.get(aspect.testName, None)
					if b is None:
						if log2:
							log2.error("Test case '" + testCaseInstance.name + "' refers to a non-existing test case named '" + aspect.testName + "'!")
						return False
					if log2:
						log2.notice("Constraint: Test case " + repr(a.name) + " should run after test case " + repr(b.name) + ".")
					nodeMatrix.set(b, a, True)

				# A.requires(B) =>		B -> A
				elif isinstance(aspect, Requires):
					b = allTestCasesByName.get(aspect.testName, None)
					if b is None:
						if log2:
							log2.error("Test case '" + testCaseInstance.name + "' refers to a non-existing test case named '" + aspect.testName + "'!")
						return False
					if log2:
						log2.notice("Constraint: Test case " + repr(a.name) + " requires success of prior test case " + repr(b.name) + ".")
					nodeMatrix.set(b, a, True)
					a.dependsOn.add(b)
					a.requires.add(b)
					testCasesToActivate.add(b)

				elif isinstance(aspect, ProvidesVariable):
					pass

				# A.requiresVariable(varName) =>		B -> A
				elif isinstance(aspect, RequiresVariable):
					b = allTestCasesByProvidedVariables.get(aspect.varName, None)
					if b is None:
						if log2:
							log2.error("Test case '" + testCaseInstance.name + "' refers to variable named '" + a.varName + "' which no test case provides!")
						return False
					if log2:
						log2.notice("Constraint: Test case " + repr(a.name) + " requires variable created by test case " + repr(b.name) + ".")
					nodeMatrix.set(b, a, True)
					a.dependsOn.add(b)
					a.requires.add(b)
					testCasesToActivate.add(b)

				# ignore
				elif isinstance(aspect, RaisesException):
					pass

				# ignore
				elif isinstance(aspect, Description):
					pass

				else:
					raise Exception()

		# clean excessive root node connections

		if log:
			log.notice("Removing excessive nodes previously introduced for building the graph ...")

		TestCaseCollection.__cleanExcessiveRootNodeConnections(nodeMatrix)

		# determine the order of processing; we need to do this now as further processing requires to definitively have no cycles

		log2 = log.descend("Calculating order of tests ...") if log else None

		try:
			allTestCases = nodeMatrix.determineOrder()
		except GraphCycleError as ee:
			if log2:
				log2.error("Cycle detected at test case: " + ee.data.name)
			return TestCaseCollection(allTestCases, nodeMatrix, rootNode, None)

		#log.notice("Total number of test cases: " + str(len(allTestCases)))

		# activate test cases scheduled for activation; recursively enable test cases as necessary

		log2 = log.descend("Activating disabled test cases that are required ...") if log else None

		while testCasesToActivate.isNotEmpty():
			testCaseInstance = testCasesToActivate.retrieve()
			if testCaseInstance.enabledState == EnumEnabledState.DISABLED:
				testCaseInstance.enabledState = EnumEnabledState.ENABLED_IN_CONSEQUENCE
				testCasesToActivate.addAll(testCaseInstance.requires)
				if log2:
					log2.notice("Enabling: " + testCaseInstance.name)

		# collect all enabled test cases

		if log:
			log.info("Preparing everything to return the results ...")

		enabledTestCasesToRunInDefinedOrder = [
			testCaseInstance for testCaseInstance in allTestCases
				if testCaseInstance.enabledState in [ EnumEnabledState.ENABLED_BY_USER, EnumEnabledState.ENABLED_IN_CONSEQUENCE ]
		]

		#rootNode.enabledState = EnumEnabledState.DISABLED
		#enabledTestCasesToRunInDefinedOrder.remove(rootNode)

		# return TestCaseCollection-object

		return TestCaseCollection(allTestCases, nodeMatrix, rootNode, enabledTestCasesToRunInDefinedOrder)
	#

	@staticmethod
	def __cleanExcessiveRootNodeConnections(nodeMatrix:NodeMatrix):
		allNodes = nodeMatrix.nodes()
		rootNode = allNodes[0]
		allNodesExceptRoot = nodeMatrix.nodes()[1:]

		for node in allNodesExceptRoot:
			allIncomingNodes = nodeMatrix.getIncoming(node)
			allIncomingNodes.remove(rootNode)
			if len(allIncomingNodes) > 0:
				nodeMatrix.set(rootNode, node, False)
	#

#


