


import re

from .AssertionException import AssertionException







class _Assert(object):

	def __init__(self, log):
		if callable(log):
			self.__log = log
		else:
			self.__log = log
	#

	def isIn(self, value, valueList, message = None):
		Assert.l_isIn(self.__log, value, valueList, message)
	#

	def isNotIn(self, value, valueList, message = None):
		Assert.l_isNotIn(self.__log, value, valueList, message)
	#

	def raisesException(self, function, arguments, message = None):
		Assert.l_raisesException(self.__log, function, arguments, message)
	#

	def isCallable(self, value, message = None):
		Assert.l_isCallable(self.__log, value, message)
	#

	def isInstance(self, value, typeOrTypes, message = None):
		Assert.l_isInstance(self.__log, value, typeOrTypes, message)
	#

	def isRegExMatch(self, value, regexPattern, message = None):
		Assert.l_isRegExMatch(self.__log, value, regexPattern, message)
	#

	def isEqual(self, value, otherValue, message = None):
		Assert.l_isEqual(self.__log, value, otherValue, message)
	#

	def isGreater(self, value, otherValue, message = None):
		Assert.l_isGreater(self.__log, value, otherValue, message)
	#

	def isGreaterOrEqual(self, value, otherValue, message = None):
		Assert.l_isGreaterOrEqual(self.__log, value, otherValue, message)
	#

	def isSmaller(self, value, otherValue, message = None):
		Assert.l_isSmaller(self.__log, value, otherValue, message)
	#

	def isSmallerOrEqual(self, value, otherValue, message = None):
		Assert.l_isSmallerOrEqual(self.__log, value, otherValue, message)
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

	def isNotNoneOrEmpty(self, value, message = None):
		Assert.l_isNotNoneOrEmpty(self.__log, value, message)
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
	def isIn(value, valueList, message = None, log = None, identifier:str = None):
		bSuccess = value in valueList

		if not bSuccess:
			if message is None:
				message = ""
			else:
				message += " :: "
			message = "ASSERTION ERROR :: " + message + "Value is " + repr(value) + " so value is not an element of list " + repr(valueList) + "!"
			if identifier:
				message = "<" + identifier + "> " + message
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
	def l_isIn(log, value, valueList, message = None, identifier:str = None):
		bSuccess = value in valueList

		if not bSuccess:
			if message is None:
				message = ""
			else:
				message += " :: "
			message = "ASSERTION ERROR :: " + message + "Value is " + repr(value) + " so value is not an element of list " + repr(valueList) + "!"
			if identifier:
				message = "<" + identifier + "> " + message
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
	def isNotIn(value, valueList, message = None, log = None, identifier:str = None):
		bSuccess = value not in valueList

		if not bSuccess:
			if message is None:
				message = ""
			else:
				message += " :: "
			message = "ASSERTION ERROR :: " + message + "Value is " + repr(value) + " so value is not an element of list " + repr(valueList) + "!"
			if identifier:
				message = "<" + identifier + "> " + message
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
	def l_isNotIn(log, value, valueList, message = None, identifier:str = None):
		bSuccess = value not in valueList

		if not bSuccess:
			if message is None:
				message = ""
			else:
				message += " :: "
			message = "ASSERTION ERROR :: " + message + "Value is " + repr(value) + " so value is not an element of list " + repr(valueList) + "!"
			if identifier:
				message = "<" + identifier + "> " + message
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
	def raisesException(function, arguments, message = None, log = None, identifier:str = None):
		bSuccess = True
		try:
			function(*arguments)
			bSuccess = False
		except Exception as ee:
			pass

		if not bSuccess:
			if message is None:
				message = ""
			else:
				message += " :: "
			message = "ASSERTION ERROR :: " + message + "No exception was raised!"
			if identifier:
				message = "<" + identifier + "> " + message
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
	def l_raisesException(log, function, arguments, message = None, identifier:str = None):
		bSuccess = True
		try:
			function(*arguments)
			bSuccess = False
		except Exception as ee:
			pass

		if not bSuccess:
			if message is None:
				message = ""
			else:
				message += " :: "
			message = "ASSERTION ERROR :: " + message + "No exception was raised!"
			if identifier:
				message = "<" + identifier + "> " + message
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
	def isCallable(value, message = None, log = None, identifier:str = None):
		if callable(value):
			return
		if message is None:
			message = ""
		else:
			message += " :: "
		message = "ASSERTION ERROR :: " + message + "Value is not a callable but of type " + str(value)
		if identifier:
			message = "<" + identifier + "> " + message
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
	def l_isCallable(log, value, message = None, identifier:str = None):
		if callable(value):
			return
		if message is None:
			message = ""
		else:
			message += " :: "
		message = "ASSERTION ERROR :: " + message + "Value is not a callable but of type " + str(value)
		if identifier:
			message = "<" + identifier + "> " + message
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
	def isInstance(value, typeOrTypes, message = None, log = None, identifier:str = None):
		if isinstance(value, typeOrTypes):
			return
		if issubclass(type(value), typeOrTypes):
			return
		if message is None:
			message = "ASSERTION ERROR"
		else:
			message += " ::"
		message = "ASSERTION ERROR :: " + message + " Value is of type " + str(type(value)) + " and not of type " + str(typeOrTypes)
		if identifier:
			message = "<" + identifier + "> " + message
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
	def l_isInstance(log, value, typeOrTypes, message = None, identifier:str = None):
		if isinstance(value, typeOrTypes):
			return
		if message is None:
			message = "ASSERTION ERROR"
		else:
			message += " ::"
		message = "ASSERTION ERROR :: " + message + " Value is of type " + str(type(value)) + " and not of type " + str(typeOrTypes)
		if identifier:
			message = "<" + identifier + "> " + message
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
	def isEqual(value, otherValue, message = None, log = None, identifier:str = None):
		if value == otherValue:
			return
		if message is None:
			message = "ASSERTION ERROR"
		else:
			message += " ::"
		message = "ASSERTION ERROR :: " + message + " Value is " + repr(value) + " and not " + repr(otherValue) + " as expected!"
		if identifier:
			message = "<" + identifier + "> " + message
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
	def l_isEqual(log, value, otherValue, message = None, identifier:str = None):
		if value == otherValue:
			return
		if message is None:
			message = "ASSERTION ERROR"
		else:
			message += " ::"
		message = "ASSERTION ERROR :: " + message + " Value is " + repr(value) + " and not " + repr(otherValue) + " as expected!"
		if identifier:
			message = "<" + identifier + "> " + message
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
	def isRegExMatch(value, regexPattern, message = None, log = None, identifier:str = None):
		m = re.match(regexPattern, value)
		if m:
			return
		if message is None:
			message = "ASSERTION ERROR"
		else:
			message += " ::"
		message = "ASSERTION ERROR :: " + message + " Value is " + repr(value) + " which does not match " + repr(regexPattern) + " as expected!"
		if identifier:
			message = "<" + identifier + "> " + message
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
	def l_isRegExMatch(log, value, regexPattern, message = None, identifier:str = None):
		m = re.match(regexPattern, value)
		if m:
			return
		if message is None:
			message = "ASSERTION ERROR"
		else:
			message += " ::"
		message = "ASSERTION ERROR :: " + message + " Value is " + repr(value) + " which does not match " + repr(regexPattern) + " as expected!"
		if identifier:
			message = "<" + identifier + "> " + message
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
	def isNotEqual(value, otherValue, message = None, log = None, identifier:str = None):
		if value != otherValue:
			return
		if message is None:
			message = "ASSERTION ERROR"
		else:
			message += " ::"
		message = "ASSERTION ERROR :: " + message + " Value is " + repr(value) + " which is not expected!"
		if identifier:
			message = "<" + identifier + "> " + message
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
	def l_isNotEqual(log, value, otherValue, message = None, identifier:str = None):
		if value != otherValue:
			return
		if message is None:
			message = "ASSERTION ERROR"
		else:
			message += " ::"
		message = "ASSERTION ERROR :: " + message + " Value is " + repr(value) + " which is not expected!"
		if identifier:
			message = "<" + identifier + "> " + message
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
	def isGreater(value, otherValue, message = None, log = None, identifier:str = None):
		if value > otherValue:
			return
		if message is None:
			message = "ASSERTION ERROR"
		else:
			message += " ::"
		message = "ASSERTION ERROR :: " + message + " Value is " + repr(value) + " which not greater than " + repr(otherValue) + " as expected!"
		if identifier:
			message = "<" + identifier + "> " + message
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
	def l_isGreater(log, value, otherValue, message = None, identifier:str = None):
		if value > otherValue:
			return
		if message is None:
			message = "ASSERTION ERROR"
		else:
			message += " ::"
		message = "ASSERTION ERROR :: " + message + " Value is " + repr(value) + " which not greater than " + repr(otherValue) + " as expected!"
		if identifier:
			message = "<" + identifier + "> " + message
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
	def isGreaterOrEqual(value, otherValue, message = None, log = None, identifier:str = None):
		if value >= otherValue:
			return
		if message is None:
			message = "ASSERTION ERROR"
		else:
			message += " ::"
		message = "ASSERTION ERROR :: " + message + " Value is " + repr(value) + " which not greater or equal to " + repr(otherValue) + " as expected!"
		if identifier:
			message = "<" + identifier + "> " + message
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
	def l_isGreaterOrEqual(log, value, otherValue, message = None, identifier:str = None):
		if value >= otherValue:
			return
		if message is None:
			message = "ASSERTION ERROR"
		else:
			message += " ::"
		message = "ASSERTION ERROR :: " + message + " Value is " + repr(value) + " which not greater or equal to " + repr(otherValue) + " as expected!"
		if identifier:
			message = "<" + identifier + "> " + message
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
	def isSmaller(value, otherValue, message = None, log = None, identifier:str = None):
		if value < otherValue:
			return
		if message is None:
			message = "ASSERTION ERROR"
		else:
			message += " ::"
		message = "ASSERTION ERROR :: " + message + " Value is " + repr(value) + " which not smaller than " + repr(otherValue) + " as expected!"
		if identifier:
			message = "<" + identifier + "> " + message
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
	def l_isSmaller(log, value, otherValue, message = None, identifier:str = None):
		if value < otherValue:
			return
		if message is None:
			message = "ASSERTION ERROR"
		else:
			message += " ::"
		message = "ASSERTION ERROR :: " + message + " Value is " + repr(value) + " which not smaller than " + repr(otherValue) + " as expected!"
		if identifier:
			message = "<" + identifier + "> " + message
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
	def isSmallerOrEqual(value, otherValue, message = None, log = None, identifier:str = None):
		if value <= otherValue:
			return
		if message is None:
			message = "ASSERTION ERROR"
		else:
			message += " ::"
		message = "ASSERTION ERROR :: " + message + " Value is " + repr(value) + " which not smaller or equal to " + repr(otherValue) + " as expected!"
		if identifier:
			message = "<" + identifier + "> " + message
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
	def l_isSmallerOrEqual(log, value, otherValue, message = None, identifier:str = None):
		if value <= otherValue:
			return
		if message is None:
			message = "ASSERTION ERROR"
		else:
			message += " ::"
		message = "ASSERTION ERROR :: " + message + " Value is " + repr(value) + " which not smaller or equal to " + repr(otherValue) + " as expected!"
		if identifier:
			message = "<" + identifier + "> " + message
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
	def isNone(value, message = None, log = None, identifier:str = None):
		if value is None:
			return
		if message is None:
			message = "ASSERTION ERROR"
		else:
			message += " ::"
		message = "ASSERTION ERROR :: " + message + " Value is not None as expected: " + repr(value)
		if identifier:
			message = "<" + identifier + "> " + message
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
	def l_isNone(log, value, message = None, identifier:str = None):
		if value is None:
			return
		if message is None:
			message = "ASSERTION ERROR"
		else:
			message += " ::"
		message = "ASSERTION ERROR :: " + message + " Value is not None as expected: " + repr(value)
		if identifier:
			message = "<" + identifier + "> " + message
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
	def isNotNone(value, message = None, log = None, identifier:str = None):
		if value is not None:
			return
		if message is None:
			message = "ASSERTION ERROR"
		else:
			message += " ::"
		message = "ASSERTION ERROR :: " + message + " Value is None which is not expected: " + repr(value)
		if identifier:
			message = "<" + identifier + "> " + message
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
	def l_isNotNone(log, value, message = None, identifier:str = None):
		if value is not None:
			return
		if message is None:
			message = "ASSERTION ERROR"
		else:
			message += " ::"
		message = "ASSERTION ERROR :: " + message + " Value is None which is not expected: " + repr(value)
		if identifier:
			message = "<" + identifier + "> " + message
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
	def isNotNoneOrEmpty(value, message = None, log = None, identifier:str = None):
		if value:
			return
		if message is None:
			message = "ASSERTION ERROR"
		else:
			message += " ::"
		message = "ASSERTION ERROR :: " + message + " Value is None or empty which is not expected: " + repr(value)
		if identifier:
			message = "<" + identifier + "> " + message
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
	def l_isNotNoneOrEmpty(log, value, message = None, identifier:str = None):
		if value:
			return
		if message is None:
			message = "ASSERTION ERROR"
		else:
			message += " ::"
		message = "ASSERTION ERROR :: " + message + " Value is None or empty which is not expected: " + repr(value)
		if identifier:
			message = "<" + identifier + "> " + message
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
	def isTrue(value, message = None, log = None, identifier:str = None):
		if value is True:
			return
		if message is None:
			message = "ASSERTION ERROR"
		else:
			message += " ::"
		message = "ASSERTION ERROR :: " + message + " Value is not true as expected: " + repr(value)
		if identifier:
			message = "<" + identifier + "> " + message
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
	def l_isTrue(log, value, message = None, identifier:str = None):
		if value is True:
			return
		if message is None:
			message = "ASSERTION ERROR"
		else:
			message += " ::"
		message = "ASSERTION ERROR :: " + message + " Value is not true as expected: " + repr(value)
		if identifier:
			message = "<" + identifier + "> " + message
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
	def isFalse(value, message = None, log = None, identifier:str = None):
		if value is False:
			return
		if message is None:
			message = "ASSERTION ERROR"
		else:
			message += " ::"
		message = "ASSERTION ERROR :: " + message + " Value is not false as expected: " + repr(value)
		if identifier:
			message = "<" + identifier + "> " + message
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
	def l_isFalse(log, value, message = None, identifier:str = None):
		if value is False:
			return
		if message is None:
			message = "ASSERTION ERROR"
		else:
			message += " ::"
		message = "ASSERTION ERROR :: " + message + " Value is not false as expected: " + repr(value)
		if identifier:
			message = "<" + identifier + "> " + message
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






