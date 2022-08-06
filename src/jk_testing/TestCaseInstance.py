


import time
import typing
import collections

import jk_logging
import jk_utils

from .annotations import Description
from .annotations import ProvidesVariable
from .annotations import RaisesException
from .annotations import Requires
from .annotations import RequiresVariable
from .annotations import RunAfter
from .annotations import RunBefore
from .annotations import TestCase

from .impl.ExceptionMatcher import ExceptionMatcher
from .TestContext import TestContext
from .EnumProcessingState import EnumProcessingState
from .EnumEnabledState import EnumEnabledState








class TestCaseInstance(object):

	#
	# Constructor.
	#
	# @param	str testCaseName					The name of a test case.
	# @param	Annotation[] testCaseAspects		A (possibly empty) set of annotations that define the test case in more detail.
	# @param	callable testCaseCallable			The user provided function that implements the test.
	#												This is the function decorated with <c>TestCase</c>.
	# @param	bool bEnabled						A flag that indicates if the test is enabled by default.
	#
	def __init__(self, bIsRoot:bool, testCaseName:str, testCaseAspects:collections.Sequence,
		testCaseCallable:collections.Callable, bEnabledByUser:bool):

		assert isinstance(bIsRoot, bool)

		if bIsRoot:
			# variables with test case definition or user provided data

			self.testCaseAspects = set()
			self.name = ""														# the name of the test
			self.testCaseCallable = None											# the function to execute to perform the test
			self.possibleExceptions = None
			self.variablesProvided = None
			self.description = None

			# variables filled at runtime

			self.enabledState = EnumEnabledState.ENABLED_IN_CONSEQUENCE
			self.processingState = EnumProcessingState.NOT_PROCESSED

		else:
			assert isinstance(testCaseName, str)
			assert isinstance(testCaseAspects, (list, tuple))
			assert callable(testCaseCallable)
			assert isinstance(bEnabledByUser, bool)

			# variables with test case definition or user provided data

			self.testCaseAspects = set(testCaseAspects) if testCaseAspects else set()			# stores all unprocessed dependencies
			self.name = testCaseName													# the name of the test
			self.testCaseCallable = testCaseCallable									# the function to execute to perform the test
			self.possibleExceptions = None
			self.variablesProvided = None
			self.description = None

			for a in self.testCaseAspects:

				if isinstance(a, ProvidesVariable):
					if self.variablesProvided is None:
						self.variablesProvided = []
					self.variablesProvided.append(a.varName)

				elif isinstance(a, RaisesException):
					if self.possibleExceptions is None:
						self.possibleExceptions = []
					self.possibleExceptions.append(ExceptionMatcher(a.exceptionClass, a.exceptionDataArgs, a.exceptionDataKWArgs))

				elif isinstance(a, Description):
					self.description = a.text

			#if self.possibleExceptions != None:
			#	for a in self.possibleExceptions:
			#		self.testCaseAspects.remove(a)

			# variables filled at runtime

			self.enabledState = EnumEnabledState.ENABLED_BY_USER if bEnabledByUser else EnumEnabledState.DISABLED
			self.processingState = EnumProcessingState.NOT_PROCESSED

		# variables filled at runtime

		self.dependsOn = set()		# stores the test cases
		self.requires = set()		# stores the test cases
		self.duration = None
		self.timeStamp = None
	#

	@property
	def isRoot(self):
		return self.testCaseCallable == None
	#

	def __str__(self):
		return self.name
	#

	def __repr__(self):
		return self.name
	#

	def runTest(self, data:dict, variables:dict, log) -> EnumProcessingState:
		nestedLog = log.descend("Running test: " + self.name + "()")

		bSuccess = False
		ctx = TestContext(data, variables, nestedLog)
		self.timeStamp = time.time()
		try:
			ret = self.testCaseCallable(True, ctx)
			self.duration = time.time() - self.timeStamp

			if self.possibleExceptions:
				# the test did not raise an exception!
				nestedLog.error("Test case " + repr(self.name) + " does not raise an exception!")
				self.processingState = EnumProcessingState.FAILED
				bSuccess = False

			else:

				if self.variablesProvided:
					# the test case should provide variables

					self.processingState = EnumProcessingState.SUCCEEDED
					bSuccess = True

					if isinstance(ret, dict):
						# the test case provides a dictionary with data.
						for varNameExpected in self.variablesProvided:
							if varNameExpected in ret:
								nestedLog.notice("Test case " + repr(self.name) + " provides variable " + repr(varNameExpected) + " as specified.")
								variables[varNameExpected] = ret[varNameExpected]
								del ret[varNameExpected]
							else:
								nestedLog.error("Test case " + repr(self.name) + " does not provide variable " + repr(varNameExpected) + " as specified!")
								self.processingState = EnumProcessingState.FAILED_CRITICALLY
								bSuccess = False
					else:
						# the test did not provide variables!
						nestedLog.error("Test case " + repr(self.name) + " does not provide variables!")
						self.processingState = EnumProcessingState.FAILED_CRITICALLY
						bSuccess = False

					if ret:
						nestedLog.warn("Test case " + repr(self.name) + " provides excessive variables: " + repr(list(ret.keys())))

				else:
					# the test case should not provide variables; if it does we ignore them;
					self.processingState = EnumProcessingState.SUCCEEDED
					bSuccess = True

		except Exception as ee:
			self.duration = time.time() - self.timeStamp

			bSuccess = False
			if self.possibleExceptions:
				for exceptionExpected in self.possibleExceptions:
					if exceptionExpected.matches(ee):
						bSuccess = True
						nestedLog.notice("Exception raised as expected: " + repr(ee))
						self.processingState = EnumProcessingState.SUCCEEDED
						break
			if not bSuccess:
				nestedLog.error(ee)
				self.processingState = EnumProcessingState.FAILED

		if bSuccess:
			nestedLog.success("Test passed.")
		else:
			nestedLog.error("TEST FAILED!")

		return self.processingState
	#

#










