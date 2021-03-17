


import os

from .AssertionException import AssertionException







class AssertX(object):

	################################################################################################################################
	## Constructor
	################################################################################################################################

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	################################################################################################################################
	## Helper Methods
	################################################################################################################################

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	################################################################################################################################
	## Public Static Methods
	################################################################################################################################

	@staticmethod
	def dirExists(dirPath:str, message = None, log = None, identifier:str = None):
		bSuccess = isinstance(dirPath, str) and os.path.isdir(dirPath)

		if not bSuccess:
			if message is None:
				message = ""
			else:
				message += " :: "
			message = "ASSERTION ERROR :: " + message + "Directory does not exist: " + repr(dirPath)
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
	def fileExists(filePath:str, message = None, log = None, identifier:str = None):
		bSuccess = isinstance(filePath, str) and os.path.isfile(filePath)

		if not bSuccess:
			if message is None:
				message = ""
			else:
				message += " :: "
			message = "ASSERTION ERROR :: " + message + "File does not exist: " + repr(filePath)
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







