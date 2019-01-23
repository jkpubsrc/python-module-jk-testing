#!/usr/bin/env python3
# -*- coding: utf-8 -*-



class AssertionException(Exception):

	def __init__(self, message):
		super().__init__(message)
	#

#





class _Assert(object):

	def __init__(self, log):
		if callable(log):
			self.__log = log
		else:
			self.__log = log
	#

	def isInstance(self, value, typeOrTypes, message = None):
		Assert.l_isInstance(self.__log, value, typeOrTypes, message)
	#

	def isEqual(self, value, otherValue, message = None):
		Assert.l_isEqual(self.__log, value, otherValue, message)
	#

	def isNotEqual(self, value, otherValue, message = None):
		Assert.l_isNotEqual(self.__log, value, otherValue, message)
	#

	def isNone(self, value, message = None):
		Assert.l_isNone(self.__log, value, message)
	#

	def isNotNone(self, value, message = None):
		Assert.l_isNotNone(self.__log, value, message)
	#

	def isTrue(self, value, message = None):
		Assert.l_isTrue(self.__log, value, message)
	#

	def isFalse(self, value, message = None):
		Assert.l_isFalse(self.__log, value, message)
	#

#










class Assert(object):

	@staticmethod
	def createCustomAssert(log):
		return _Assert(log)
	#

	"""
	@staticmethod
	def getAllBaseClasses(cls):
		# TODO: convert this to an iteration
		c = list(cls.__bases__)
		for base in c:
			c.extend(getAllBaseClasses(base))
		return c
	#
	"""

	@staticmethod
	def isInstance(value, typeOrTypes, message = None, log = None):
		if isinstance(value, typeOrTypes):
			return
		if issubclass(type(value), typeOrTypes):
			return
		if message is None:
			message = "ASSERTION ERROR"
		else:
			message += " ::"
		message = "ASSERTION ERROR :: " + message + " Value is of type " + str(type(value)) + " and not of type " + str(typeOrTypes)
		if log != None:
			if callable(log):
				log(message)
			else:
				log.error(message)
		else:
			print(message)
		raise AssertionException(message)
	#

	@staticmethod
	def l_isInstance(log, value, typeOrTypes, message = None):
		if isinstance(value, typeOrTypes):
			return
		if message is None:
			message = "ASSERTION ERROR"
		else:
			message += " ::"
		message = "ASSERTION ERROR :: " + message + " Value is of type " + str(type(value)) + " and not of type " + str(typeOrTypes)
		if log != None:
			if callable(log):
				log(message)
			else:
				log.error(message)
		else:
			print(message)
		raise AssertionException(message)
	#

	@staticmethod
	def isEqual(value, otherValue, message = None, log = None):
		if value == otherValue:
			return
		if message is None:
			message = "ASSERTION ERROR"
		else:
			message += " ::"
		message = "ASSERTION ERROR :: " + message + " Value is " + repr(value) + " and not " + repr(otherValue) + " as expected!"
		if log != None:
			if callable(log):
				log(message)
			else:
				log.error(message)
		else:
			print(message)
		raise AssertionException(message)
	#

	@staticmethod
	def l_isEqual(log, value, otherValue, message = None):
		if value == otherValue:
			return
		if message is None:
			message = "ASSERTION ERROR"
		else:
			message += " ::"
		message = "ASSERTION ERROR :: " + message + " Value is " + repr(value) + " and not " + repr(otherValue) + " as expected!"
		if log != None:
			if callable(log):
				log(message)
			else:
				log.error(message)
		else:
			print(message)
		raise AssertionException(message)
	#

	@staticmethod
	def isNotEqual(value, otherValue, message = None, log = None):
		if value != otherValue:
			return
		if message is None:
			message = "ASSERTION ERROR"
		else:
			message += " ::"
		message = "ASSERTION ERROR :: " + message + " Value is " + repr(value) + " which is not expected!"
		if log != None:
			if callable(log):
				log(message)
			else:
				log.error(message)
		else:
			print(message)
		raise AssertionException(message)
	#

	@staticmethod
	def l_isNotEqual(log, value, otherValue, message = None):
		if value != otherValue:
			return
		if message is None:
			message = "ASSERTION ERROR"
		else:
			message += " ::"
		message = "ASSERTION ERROR :: " + message + " Value is " + repr(value) + " which is not expected!"
		if log != None:
			if callable(log):
				log(message)
			else:
				log.error(message)
		else:
			print(message)
		raise AssertionException(message)
	#

	@staticmethod
	def isNone(value, message = None, log = None):
		if value is None:
			return
		if message is None:
			message = "ASSERTION ERROR"
		else:
			message += " ::"
		message = "ASSERTION ERROR :: " + message + " Value is not None as expected: " + repr(value)
		if log != None:
			if callable(log):
				log(message)
			else:
				log.error(message)
		else:
			print(message)
		raise AssertionException(message)
	#

	@staticmethod
	def l_isNone(log, value, message = None):
		if value is None:
			return
		if message is None:
			message = "ASSERTION ERROR"
		else:
			message += " ::"
		message = "ASSERTION ERROR :: " + message + " Value is not None as expected: " + repr(value)
		if log != None:
			if callable(log):
				log(message)
			else:
				log.error(message)
		else:
			print(message)
		raise AssertionException(message)
	#

	@staticmethod
	def isNotNone(value, message = None, log = None):
		if value is not None:
			return
		if message is None:
			message = "ASSERTION ERROR"
		else:
			message += " ::"
		message = "ASSERTION ERROR :: " + message + " Value is None which is not expected: " + repr(value)
		if log != None:
			if callable(log):
				log(message)
			else:
				log.error(message)
		else:
			print(message)
		raise AssertionException(message)
	#

	@staticmethod
	def l_isNotNone(log, value, message = None):
		if value is not None:
			return
		if message is None:
			message = "ASSERTION ERROR"
		else:
			message += " ::"
		message = "ASSERTION ERROR :: " + message + " Value is None which is not expected: " + repr(value)
		if log != None:
			if callable(log):
				log(message)
			else:
				log.error(message)
		else:
			print(message)
		raise AssertionException(message)
	#

	@staticmethod
	def isTrue(value, message = None, log = None):
		if value is True:
			return
		if message is None:
			message = "ASSERTION ERROR"
		else:
			message += " ::"
		message = "ASSERTION ERROR :: " + message + " Value is not true as expected: " + repr(value)
		if log != None:
			if callable(log):
				log(message)
			else:
				log.error(message)
		else:
			print(message)
		raise AssertionException(message)
	#

	@staticmethod
	def l_isTrue(log, value, message = None):
		if value is True:
			return
		if message is None:
			message = "ASSERTION ERROR"
		else:
			message += " ::"
		message = "ASSERTION ERROR :: " + message + " Value is not true as expected: " + repr(value)
		if log != None:
			if callable(log):
				log(message)
			else:
				log.error(message)
		else:
			print(message)
		raise AssertionException(message)
	#

	@staticmethod
	def isFalse(value, message = None, log = None):
		if value is False:
			return
		if message is None:
			message = "ASSERTION ERROR"
		else:
			message += " ::"
		message = "ASSERTION ERROR :: " + message + " Value is not false as expected: " + repr(value)
		if log != None:
			if callable(log):
				log(message)
			else:
				log.error(message)
		else:
			print(message)
		raise AssertionException(message)
	#

	@staticmethod
	def l_isFalse(log, value, message = None):
		if value is False:
			return
		if message is None:
			message = "ASSERTION ERROR"
		else:
			message += " ::"
		message = "ASSERTION ERROR :: " + message + " Value is not false as expected: " + repr(value)
		if log != None:
			if callable(log):
				log(message)
			else:
				log.error(message)
		else:
			print(message)
		raise AssertionException(message)
	#

#






