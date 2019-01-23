#!/usr/bin/env python3
# -*- coding: utf-8 -*-



import time
import collections

import jk_logging

from .Annotations import *
from .TestCaseInstance import *






class TestCaseCollection(object):

	def __init__(self):
		self._allTestCasesByName = {}					# stores names of test cases => test case records
		self._allTestCasesByProvidedVariables = {}		# stores variable names provided by test cases => test case records
		self._allTestCasesAdded = []					# stores test case records
		self._orderOfProcessing = None					# stores all test case records in the order the test cases need to be processed
	#

	#
	# Is the collection prepaired for processing? "Prepaired" means: The dependencies are analysed and the processing order is calculated.
	#
	@property
	def isPrepared(self):
		return self._orderOfProcessing != None
	#

	#
	# Use this test case to the list of test cases.
	#
	def add(self, testCaseInstance):
		assert isinstance(testCaseInstance, TestCaseInstance)

		self._allTestCasesByName[testCaseInstance.name] = testCaseInstance
		self._allTestCasesAdded.append(testCaseInstance)

		for a in testCaseInstance.testCaseAspects:
			if isinstance(a, providesVariable):
				if a.varName in self._allTestCasesByProvidedVariables:
					raise Exception("Test case '" + testCaseInstance.name + "' provides variable '" + a.varName + "' while test case '"
						+ self._allTestCasesByProvidedVariables[a.varName].name + "' already provides variable '" + a.varName + "'!")
				self._allTestCasesByProvidedVariables[a.varName] = testCaseInstance

		# now we are no longer prepared.
		self._unprepare()
	#

	#
	# Retreive the (ordered) list of test tasks to process.
	#
	# @return	TestCaaseInstance[] testCaseInstances		Returns the list of test tasks to process. If the collection is not prepaired, <c>None</c> is returned.
	#
	def getTestTasksToProcess(self):
		if self._orderOfProcessing is None:
			return None
		return list(self._orderOfProcessing)
	#

	def _unprepare(self):
		for testCaseInstance in self._allTestCasesAdded:
			testCaseInstance.reset()
		self._orderOfProcessing = None
	#

	#
	#
	#
	def __buildTestCaseGraph(self, log):
		# 1) set dependencies:
		#		A.runBefore(B)			->  B.dependencies.add(A)
		#		A.runAfter(B)			->  A.dependencies.add(B)
		#		A.requires(B)			->  A.requires.add(B)
		#		A.requiresVariable(xyz)	->  B.dependencies.add(A) where B provides xyz
		for testCaseInstance in self._allTestCasesAdded:
			for a in testCaseInstance.testCaseAspects:

				if isinstance(a, runBefore):
					b = self._allTestCasesByName.get(a.testName, None)
					if b is None:
						log.error("Test case '" + testCaseInstance.name + "' refers to a non-existing test case named '" + a.testName + "'!")
						return False
					testCaseInstance.dependencies.add(a.name)

				elif isinstance(a, runAfter):
					b = self._allTestCasesByName.get(a.testName, None)
					if b is None:
						log.error("Test case '" + testCaseInstance.name + "' refers to a non-existing test case named '" + a.testName + "'!")
						return False
					b.dependencies.add(testCaseInstance.name)

				elif isinstance(a, requires):
					b = self._allTestCasesByName.get(a.testName, None)
					if b is None:
						log.error("Test case '" + testCaseInstance.name + "' refers to a non-existing test case named '" + a.testName + "'!")
						return False
					b.dependencies.add(testCaseInstance.name)
					b.requires.add(testCaseInstance.name)
					testCaseInstance.requires.add(b.name)

				elif isinstance(a, requiresVariable):
					b = self._allTestCasesByProvidedVariables.get(a.varName, None)
					if b is None:
						log.error("Test case '" + testCaseInstance.name + "' refers to variable named '" + a.varName + "' which no test case provides!")
						return False
					testCaseInstance.dependencies.add(b.name)
					testCaseInstance.requires.add(b.name)
	#

	#
	# This method precompiles all test cases in order to execute them later as required.
	#
	def prepare(self, log):
		self.__buildTestCaseGraph(log)

		# 2) check for cycles and determine order of test case execution
		notYetProcessed = list(self._allTestCasesAdded)
		alreadyProcessedNames = set()
		orderOfProcessing = []
		while notYetProcessed:
			notYetProcessedRemaining = []
			for x in notYetProcessed:
				testCaseInstance, bEnabled = x
				if testCaseInstance.areAllDependenciesMet(alreadyProcessedNames):
					alreadyProcessedNames.add(testCaseInstance.name)
					orderOfProcessing.append(x)
				else:
					notYetProcessedRemaining.append(x)
			if len(notYetProcessedRemaining) == len(notYetProcessed):
				# all items have unmet dependencies!
				log.error("Cyclic dependencies detected! The following test cases are involved in this cycle:")
				for x in notYetProcessed:
					testCaseInstance, bEnabled = x
					log.error("Test case '" + testCaseInstance.name + "' depends on: " + repr(testCaseInstance.dependencies))
				return False
			notYetProcessed = notYetProcessedRemaining

		# 3) check if all test cases are enabled that produce output required by other test cases.
		testCaseList = list(orderOfProcessing)
		testCaseList.reverse()						# the last test case will be put first. we process the list in reverse order.
		for x in testCaseList:
			testCaseInstance, bEnabled = x
			if bEnabled:
				print("Test case instance: " + testCaseInstance.name)
				for referringTestCaseName in testCaseInstance.requires:
					print("\tRequires: " + referringTestCaseName)
					self.__enableTestCaseAndPredecessors(referringTestCaseName, testCaseInstance.name, log)

		# we end up here if everything went well.
		self._orderOfProcessing = orderOfProcessing
		return True
	#

	def __enableTestCaseAndPredecessors(self, testCaseName, requiredByTestCaseName, log):
		x = self._allTestCasesByName[testCaseName]
		testCaseInstance, bEnabled = x
		if not bEnabled:
			x[1] = True
			log.notice("Enabling test case '" + testCaseInstance.name + "' as test case '" + requiredByTestCaseName + "' (and maybe other test cases) depends on it.")

		print("Test case instance: " + testCaseInstance.name)
		for referringTestCaseName in testCaseInstance.requires:
			print("\tRequires: " + referringTestCaseName)
			self.__enableTestCaseAndPredecessors(referringTestCaseName, testCaseName, log)
	#

#









