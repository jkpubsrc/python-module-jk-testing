


from operator import getitem
import typing





class ExceptionMatcher(object):

	################################################################################################################################
	## Constructor
	################################################################################################################################

	def __init__(self, exceptionClass:typing.Union[str,type], exceptionDataArgs:typing.Union[tuple,list], exceptionDataKWArgs:dict):
		assert isinstance(exceptionClass, (str, type))
		self.__exceptionClass = exceptionClass

		if exceptionDataArgs is not None:
			assert isinstance(exceptionDataArgs, (tuple,list))
			self.__exceptionDataArgs = exceptionDataArgs
		else:
			self.__exceptionDataArgs = None

		if exceptionDataKWArgs is not None:
			assert isinstance(exceptionDataKWArgs, dict)
			self.__exceptionDataKWArgs = exceptionDataKWArgs
		else:
			self.__exceptionDataKWArgs = None
	#

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	################################################################################################################################
	## Helper Methods
	################################################################################################################################

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	def matches(self, ee:Exception):
		if isinstance(self.__exceptionClass, str):
			if ee.__class__.__name__ != self.__exceptionClass:
				return False
		else:
			if ee.__class__ != self.__exceptionClass:
				return False

		if self.__exceptionDataArgs:
			for i, v in enumerate(self.__exceptionDataArgs):
				eev = ee.args[i]
				if eev != v:
					return False

		if self.__exceptionDataKWArgs:
			for k, v in self.__exceptionDataKWArgs.items():
				eev = getattr(ee, k, None)
				if eev != v:
					return False

		return True
	#

#




