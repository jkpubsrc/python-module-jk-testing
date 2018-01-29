#!/usr/bin/env python3
# -*- coding: utf-8 -*-



import time
import collections

import jk_logging

from .Annotations import *






getCurrentTimeMillis = lambda: int(round(time.time() * 1000))





class TestCaseInstance(object):

	def __init__(self, testCaseMetaData, testCaseName, testCaseCallable):
		self.testCaseMetaData = testCaseMetaData if testCaseMetaData else ()		# stores all unprocessed dependencies
		self.name = testCaseName													# the name of the test
		self.testCaseCallable = testCaseCallable									# the function to execute to perform the test

		self.dependencies = set()					# stores the names of the test cases this test depends on; this is a weak constraint, indicating a specific order of test cases
		self.requires = set()						# stores the names of the test cases this test depends on; this is a strong constraint, requiring the prior success of specific test cases
	#

	def areAllDependenciesMet(self, namesOfAllTestCasesAlreadyProcessed):
		for d in self.dependencies:
			if d not in namesOfAllTestCasesAlreadyProcessed:
				return False
		return True
	#

	def runTest(self, globalVars, log):
		print("-")
		print()
		#print(test)
		nestedLog = log.descend("Running test: " + self.name + "()")
		self.testCaseCallable(globalVars, nestedLog)
		nestedLog.success("Tests passed.")
		print()
		print("-")
	#

#





class TestCaseEntirety(object):

	__DEFAULT_NONE_TUPLE = (None, None)

	def __init__(self):
		self._allTestCasesByName = {}					# stores names of test cases => test case records
		self._allTestCasesByProvidedVariables = {}		# stores variable names provided by test cases => test case records
		self._allTestCasesAdded = []					# stores test case records
		self._orderOfProcessing = None					# stores all test case records in the order the test cases need to be processed
	#

	@property
	def isPrepared(self):
		return self._orderOfProcessing != None
	#

	#
	# Use this method to append test cases. This method collects all necessary information from the test case description/meta data in order to perform
	# determine the test case order later.
	#
	def add(self, testCaseInstance, bEnabled = True):
		assert isinstance(testCaseInstance, TestCaseInstance)
		assert isinstance(bEnabled, bool)

		x = [testCaseInstance, bEnabled]
		self._allTestCasesByName[testCaseInstance.name] = x
		self._allTestCasesAdded.append(x)
		for a in testCaseInstance.testCaseMetaData:
			if isinstance(a, providesVariable):
				if a.varName in self._allTestCasesByProvidedVariables:
					raise Exception("Test case '" + testCaseInstance.name + "' provides variable '" + a.varName + "' while test case '"
						+ self._allTestCasesByProvidedVariables[a.varName].name + "' already provides variable '" + a.varName + "'!")
				self._allTestCasesByProvidedVariables[a.varName] = x

		# now we are no longer prepared.
		self._unprepare()
	#

	def getTestTasksToProcess(self):
		if self._orderOfProcessing is None:
			return None
		return list(self._orderOfProcessing)
	#

	def _unprepare(self):
		for testCaseInstance, bEnabled in self._allTestCasesAdded:
			testCaseInstance.dependencies.clear()
		self._orderOfProcessing = None
	#

	#
	# This method precompiles all test cases in order to execute them later as required.
	#
	def prepare(self, log):
		# 1) transform:
		#		A.runBefore(B)			->  B.dependencies.add(A)
		#		A.runAfter(B)			->  B.dependencies.add(A)
		#		A.requiresVariable(xyz)	->  B.dependencies.add(A) where B provides xyz
		for testCaseInstance, bEnabled in self._allTestCasesAdded:
			for a in testCaseInstance.testCaseMetaData:
				if isinstance(a, runBefore):
					b, _bEnabled = self._allTestCasesByName.get(a.testName, TestCaseEntirety.__DEFAULT_NONE_TUPLE)
					if b is None:
						log.error("Test case '" + testCaseInstance.name + "' refers to a non-existing test case named '" + a.testName + "'!")
						return False
					testCaseInstance.dependencies.add(a.testName)
				elif isinstance(a, runAfter):
					b, _bEnabled = self._allTestCasesByName.get(a.testName, TestCaseEntirety.__DEFAULT_NONE_TUPLE)
					if b is None:
						log.error("Test case '" + testCaseInstance.name + "' refers to a non-existing test case named '" + a.testName + "'!")
						return False
					b.dependencies.add(testCaseInstance.name)
				elif isinstance(a, requires):
					b, _bEnabled = self._allTestCasesByName.get(a.testName, TestCaseEntirety.__DEFAULT_NONE_TUPLE)
					if b is None:
						log.error("Test case '" + testCaseInstance.name + "' refers to a non-existing test case named '" + a.testName + "'!")
						return False
					b.dependencies.add(testCaseInstance.name)
					testCaseInstance.requires.add(b.name)
				elif isinstance(a, requiresVariable):
					b, _bEnabled = self._allTestCasesByProvidedVariables.get(a.varName, TestCaseEntirety.__DEFAULT_NONE_TUPLE)
					if b is None:
						log.error("Test case '" + testCaseInstance.name + "' refers to variable named '" + a.varName + "' which no test case provides!")
						return False
					testCaseInstance.dependencies.add(b.name)
					testCaseInstance.requires.add(b.name)

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
				for referringTestCaseName in testCaseInstance.requires:
					self.__enableTestCaseAndPredecessors(referringTestCaseName, log)

		# we end up here if everything went well.
		self._orderOfProcessing = orderOfProcessing
		return True
	#

	def __enableTestCaseAndPredecessors(self, testCaseName, log):
		x = self._allTestCasesByName[testCaseName]
		testCaseInstance, bEnabled = x
		if not bEnabled:
			x[1] = True
			log.notice("Enabling test case '" + testCaseInstance.name + "' as test case '" + testCaseName + "' (and maybe other test cases) depends on it.")
		for referringTestCaseName in testCaseInstance.requires:
			self.__enableTestCaseAndPredecessors(referringTestCaseName, log)
	#

#







TestResult = collections.namedtuple("TestResult", [ "name", "testCaseInstance", "logBuffer", "bResult"])




class TestDriver(object):

	def __init__(self):
		self.log = jk_logging.ConsoleLogger.create(logMsgFormatter = jk_logging.COLOR_LOG_MESSAGE_FORMATTER)
	#

	#
	# Run tests.
	#
	# @param	tuple<str,bool>[] testsToRun			Tuples that define which tests to run. Each tuple contains the following entries:
	#													* The name of the test case.
	#													* A flag indicating if this test case is to be run.
	# @return	tuple<int,int,int,int,TestResult[]>		Returns a tuple of the following structure:
	#													* The number of tests performed (or even attempted to perform).
	#													* The number of tests skipped.
	#													* The number of tests succeeded.
	#													* The number of tests failed.
	#													* list of test result records.
	#
	def runTests(self, testsToRun):
		t0 = getCurrentTimeMillis()

		self.log.info("Building list of all tests ...")
		testCaseEntirety = TestCaseEntirety()
		for test, bEnabled in testsToRun:
			if not callable(test):
				raise Exception("Not a callable: " + repr(test))
			testCaseMetaData = None
			testCaseName = str(test.__name__)
			if test.__name__ == "TestCaseWrapper":			# note: we accept methods as well that are not a test case
				testCaseMetaData, testCaseName = test()
			testCaseEntirety.add(TestCaseInstance(testCaseMetaData, testCaseName, test), bEnabled)

		if not testCaseEntirety.prepare(self.log.descend("Preparing test execution ...")):
			self.log.error("Failed to prepare all test cases for execution.")
			return False

		#for testCaseInstance, enabled in testCaseEntirety.getTestTasksToProcess():
		#	print("-- " + testCaseInstance.name + " : " + str(enabled))

		t1 = getCurrentTimeMillis()

		testsPerformedList = []
		globalVars = {}
		countPerformed = 0
		countSkipped = 0
		countSucceeded = 0
		countFailed = 0
		for testCaseInstance, bEnabled in testCaseEntirety.getTestTasksToProcess():
			if bEnabled:
				countPerformed += 1
				try:
					blog = jk_logging.BufferLogger.create()
					testCaseInstance.runTest(globalVars, jk_logging.MulticastLogger.create(self.log, blog))
					testsPerformedList.append(TestResult(testCaseInstance.name, testCaseInstance, blog, True))
					countSucceeded += 1
				except Exception as e:
					if e.__class__.__name__ == "_ExceptionInChildContextException":
						testsPerformedList.append(TestResult(testCaseInstance.name, testCaseInstance, blog, False))
						countFailed += 1
					else:
						raise
			else:
				countSkipped += 1

		t2 = getCurrentTimeMillis()

		# ----

		print()
		print()
		myLog = self.log.descend("Summary")
		myLog.info(str(t1 - t0) + " ms used to prepare and schedule the tests.")
		myLog.info(str(t2 - t1) + " ms used to run the tests.")
		myLog.info(str(countPerformed) + " tests attempted (= active tests).")
		myLog.info(str(countSucceeded) + " tests succeeded.")
		myLog.info(str(countFailed) + " tests failed.")
		myLog.info(str(countSkipped) + " tests skipped (= inactive tests).")

		return (countPerformed, countSkipped, countSucceeded, countFailed, testsPerformedList)
	#

#






