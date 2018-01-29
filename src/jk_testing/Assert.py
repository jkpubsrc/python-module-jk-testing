#!/usr/bin/env python3
# -*- coding: utf-8 -*-




class Assert(object):

	@staticmethod
	def isinstance(value, typeOrTypes, message = None, log = None):
		if isinstance(value, typeOrTypes):
			return
		if message is None:
			message = ""
		else:
			message += " ::"
		message = "ASSERTION ERROR :: " + message + " Value is of type " + str(type(value)) + " and not of type " + str(typeOrTypes)
		if log != None:
			log.error(message)
		else:
			print(message)
		raise Exception("Assertion Error")
	#

	@staticmethod
	def l_isinstance(log, value, typeOrTypes, message = None):
		if isinstance(value, typeOrTypes):
			return
		if message is None:
			message = ""
		else:
			message += " ::"
		message = "ASSERTION ERROR :: " + message + " Value is of type " + str(type(value)) + " and not of type " + str(typeOrTypes)
		if log != None:
			log.error(message)
		else:
			print(message)
		raise Exception("Assertion Error")
	#

	@staticmethod
	def isEqual(value, otherValue, message = None, log = None):
		if value == otherValue:
			return
		if message is None:
			message = ""
		else:
			message += " ::"
		message = "ASSERTION ERROR :: " + message + " Value is " + repr(value) + " and not " + repr(otherValue) + " as expected!"
		if log != None:
			log.error(message)
		else:
			print(message)
		raise Exception("Assertion Error")
	#

	@staticmethod
	def l_isEqual(log, value, otherValue, message = None):
		if value == otherValue:
			return
		if message is None:
			message = ""
		else:
			message += " ::"
		message = "ASSERTION ERROR :: " + message + " Value is " + repr(value) + " and not " + repr(otherValue) + " as expected!"
		if log != None:
			log.error(message)
		else:
			print(message)
		raise Exception("Assertion Error")
	#

	@staticmethod
	def isNotEqual(value, otherValue, message = None, log = None):
		if value != otherValue:
			return
		if message is None:
			message = ""
		else:
			message += " ::"
		message = "ASSERTION ERROR :: " + message + " Value is " + repr(value) + " which is not expected!"
		if log != None:
			log.error(message)
		else:
			print(message)
		raise Exception("Assertion Error")
	#

	@staticmethod
	def l_isNotEqual(log, value, otherValue, message = None):
		if value != otherValue:
			return
		if message is None:
			message = ""
		else:
			message += " ::"
		message = "ASSERTION ERROR :: " + message + " Value is " + repr(value) + " which is not expected!"
		if log != None:
			log.error(message)
		else:
			print(message)
		raise Exception("Assertion Error")
	#

	@staticmethod
	def isNone(value, message = None, log = None):
		if value is None:
			return
		if message is None:
			message = ""
		else:
			message += " ::"
		message = "ASSERTION ERROR :: " + message + " Value is not None as expected: " + repr(value)
		if log != None:
			log.error(message)
		else:
			print(message)
		raise Exception("Assertion Error")
	#

	@staticmethod
	def l_isNone(log, value, message = None):
		if value is None:
			return
		if message is None:
			message = ""
		else:
			message += " ::"
		message = "ASSERTION ERROR :: " + message + " Value is not None as expected: " + repr(value)
		if log != None:
			log.error(message)
		else:
			print(message)
		raise Exception("Assertion Error")
	#

	@staticmethod
	def isNotNone(value, message = None, log = None):
		if value is not None:
			return
		if message is None:
			message = ""
		else:
			message += " ::"
		message = "ASSERTION ERROR :: " + message + " Value is None which is not expected: " + repr(value)
		if log != None:
			log.error(message)
		else:
			print(message)
		raise Exception("Assertion Error")
	#

	@staticmethod
	def l_isNotNone(log, value, message = None):
		if value is not None:
			return
		if message is None:
			message = ""
		else:
			message += " ::"
		message = "ASSERTION ERROR :: " + message + " Value is None which is not expected: " + repr(value)
		if log != None:
			log.error(message)
		else:
			print(message)
		raise Exception("Assertion Error")
	#

	@staticmethod
	def isTrue(value, message = None, log = None):
		if value is True:
			return
		if message is None:
			message = ""
		else:
			message += " ::"
		message = "ASSERTION ERROR :: " + message + " Value is not true as expected: " + repr(value)
		if log != None:
			log.error(message)
		else:
			print(message)
		raise Exception("Assertion Error")
	#

	@staticmethod
	def l_isTrue(log, value, message = None):
		if value is True:
			return
		if message is None:
			message = ""
		else:
			message += " ::"
		message = "ASSERTION ERROR :: " + message + " Value is not true as expected: " + repr(value)
		if log != None:
			log.error(message)
		else:
			print(message)
		raise Exception("Assertion Error")
	#

	@staticmethod
	def isFalse(value, message = None, log = None):
		if value is False:
			return
		if message is None:
			message = ""
		else:
			message += " ::"
		message = "ASSERTION ERROR :: " + message + " Value is not false as expected: " + repr(value)
		if log != None:
			log.error(message)
		else:
			print(message)
		raise Exception("Assertion Error")
	#

	@staticmethod
	def l_isFalse(log, value, message = None):
		if value is False:
			return
		if message is None:
			message = ""
		else:
			message += " ::"
		message = "ASSERTION ERROR :: " + message + " Value is not false as expected: " + repr(value)
		if log != None:
			log.error(message)
		else:
			print(message)
		raise Exception("Assertion Error")
	#

#






