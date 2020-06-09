#!/usr/bin/env python3
# -*- coding: utf-8 -*-



import time
import collections
import subprocess
import queue
import datetime

import jk_logging

from .Annotations import *
from .TestCaseInstance import *
from .TestCaseCollection import *
from .NodeMatrix import *
from .TestResult import *
from .TestResultCollection import *




getCurrentTimeMillis = lambda: int(round(time.time() * 1000))






class TestDriver(object):

	def __init__(self):
		self.log = jk_logging.ConsoleLogger.create(logMsgFormatter = jk_logging.COLOR_LOG_MESSAGE_FORMATTER)
		self.__data = {}
	#

	@property
	def data(self):
		return self.__data
	#

	#
	# Run tests.
	#
	# @param	tuple<callable,bool>[] testsToRun		Tuples that define which tests to run. Each tuple contains the following entries:
	#													* The test case represented by a function to run.
	#													* A flag indicating if this test case is to be run.
	# @return	tuple<int,int,int,int,TestResult[]>		Returns a tuple of the following structure:
	#													* The number of tests performed (or even attempted to perform).
	#													* The number of tests skipped.
	#													* The number of tests succeeded.
	#													* The number of tests failed.
	#													* list of test result records.
	#
	def runTests(self, testsToRun) -> TestResultCollection:
		log2 = self.log.descend("Compiling test cases")
		testCaseCollection = TestCaseCollection.compile(testsToRun, log2)
		results = TestResultCollection(testCaseCollection, TestCollectionVisualizer())
		if testCaseCollection.isFailed:
			# prepairing tests failed!
			log2.error("Preparations failed!")
			return results
		log2.success("Preparations succeeded.")

		log2 = self.log.descend("Running tests ...")

		variables = {}
		theTestsToRun = testCaseCollection.enabledTestCasesToRunInDefinedOrder
		t0 = datetime.datetime.now()

		for testCaseInstance in theTestsToRun:
			if testCaseInstance.isRoot:
				continue

			logBuffer = jk_logging.BufferLogger.create()
			processingState = testCaseInstance.runTest(self.__data, variables, logBuffer)
			testResult = TestResult(testCaseInstance, logBuffer)
			logBuffer.forwardTo(log2)

			results.testResults.append(testResult)
			if processingState == EnumProcessingState.FAILED:
				results.countTestsFailed += 1
			elif processingState == EnumProcessingState.FAILED_CRITICALLY:
				results.countTestsFailed += 1
				break
			elif processingState == EnumProcessingState.SUCCEEDED:
				results.countTestsSucceeded += 1
			else:
				raise Exception()
			results.totalTestDuration += testResult.duration

		results.totalTestRuntime = (datetime.datetime.now() - t0).total_seconds()

		log2 = self.log.descend("Summary")
		log2.info("Number of tests performed: " + str(results.countTestsPerformed))
		if results.countTestsFailed > 0:
			log2.info("Number of tests succeeded: " + str(results.countTestsSucceeded))
			log2.error("Number of tests failed: " + str(results.countTestsFailed))
		else:
			log2.success("Number of tests succeeded: " + str(results.countTestsSucceeded))
			log2.info("Number of tests failed: " + str(results.countTestsFailed))
		log2.info("Total duration: " + jk_utils.formatTime(results.totalTestRuntime))
		log2.info("Average duration of single test: " + str(round(results.totalTestRuntime * 1000 / results.countTestsPerformed, 1)) + " ms")

		return results
	#

	"""
	def __runTests(self, testsToRun):
		t0 = getCurrentTimeMillis()

		self.log.info("Building list of all tests ...")
		testCaseCollection = TestCaseCollection()
		for testCallable, bEnabled in testsToRun:
			testCaseInstance = self.__parseTestCallable(testCallable, bEnabled)
			testCaseCollection.add(testCaseInstance)

		if not testCaseCollection.prepare(self.log.descend("Preparing test execution ...")):
			self.log.error("Failed to prepare all test cases for execution.")
			return False

		#for testCaseInstance, enabled in testCaseCollection.getTestTasksToProcess():
		#	print("-- " + testCaseInstance.name + " : " + str(enabled))

		t1 = getCurrentTimeMillis()

		testsPerformedList = []
		variables = {}
		countPerformed = 0
		countSkipped = 0
		countSucceeded = 0
		countFailed = 0
		for testCaseInstance, bEnabled in testCaseCollection.getTestTasksToProcess():
			if bEnabled:
				countPerformed += 1
				try:
					blog = jk_logging.BufferLogger.create()
					testCaseInstance.runTest(variables, jk_logging.MulticastLogger.create(self.log, blog))
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
	"""

#






