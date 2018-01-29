#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import functools








class requiresVariable(object):

	def __init__(self, varName):
		self.varName = varName
	#

#



class providesVariable(object):

	def __init__(self, varName):
		self.varName = varName
	#

#



class runAfter(object):

	def __init__(self, testName):
		self.testName = testName
	#

#



class requires(object):

	def __init__(self, testName):
		self.testName = testName
	#

#



class runBefore(object):

	def __init__(self, testName):
		self.testName = testName
	#

#









class TestCase(object):

	__VALID_CLASSES = (providesVariable, requiresVariable, runAfter, runBefore, requires)

	def __init__(self, *testAspects):
		# check if test aspects are valid
		for a in testAspects:
			if not isinstance(a, TestCase.__VALID_CLASSES):
				raise Exception("Unknown test aspect: " + str(a))
		# remember them for later
		self.testAspects = testAspects
	#

	def __get__(self, obj, objtype):
		return functools.partial(self.__call__, obj)
	#

	def __call__(self, original_func):
		decorator_self = self
		def TestCaseWrapper(*args, **kwargs):
			if len(args) == 0:
				return (decorator_self.testAspects, original_func.__name__)
			#self.testAspects = decorator_self.testAspects
			else:
				return original_func(*args,**kwargs)
		return TestCaseWrapper
	#

#






