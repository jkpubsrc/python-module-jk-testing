

import functools

from .ProvidesVariable import ProvidesVariable
from .RequiresVariable import RequiresVariable
from .RunAfter import RunAfter
from .RunBefore import RunBefore
from .Requires import Requires
from .RaisesException import RaisesException
from .Description import Description





def _appendTo(someItemOrItems, classToWrap, someList):
	if isinstance(someList, tuple):
		someList = list(someList)
	if isinstance(someList, list):
		if isinstance(someItemOrItems, (list, tuple)):
			for x in someItemOrItems:
				someList.append(classToWrap(someItemOrItems))
		else:
			someList.append(classToWrap(someItemOrItems))
		return someList
	else:
		raise ValueError()
#





class TestCase(object):

	################################################################################################################################
	## Constants
	################################################################################################################################

	__VALID_CLASSES = (ProvidesVariable, RequiresVariable, RunAfter, RunBefore, Requires, RaisesException, Description)

	################################################################################################################################
	## Constructor
	################################################################################################################################

	def __init__(self,
			*testAspects,
			**kwargs
		):

		# check if test aspects are valid
		for a in testAspects:
			if not isinstance(a, TestCase.__VALID_CLASSES):
				raise Exception("Unknown test aspect: " + str(a))

		if "requires" in kwargs:
			testAspects = _appendTo(kwargs["requires"], Requires, testAspects)
		if "runBefore" in kwargs:
			testAspects = _appendTo(kwargs["runBefore"], RunBefore, testAspects)
		if "runAfter" in kwargs:
			testAspects = _appendTo(kwargs["runAfter"], RunAfter, testAspects)
		if "requiresVariable" in kwargs:
			testAspects = _appendTo(kwargs["requiresVariable"], RequiresVariable, testAspects)
		if "providesVariable" in kwargs:
			testAspects = _appendTo(kwargs["providesVariable"], ProvidesVariable, testAspects)
		if "description" in kwargs:
			testAspects = _appendTo(kwargs["description"], Description, testAspects)

		# remember them for later
		self.testAspects = testAspects
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

	def __get__(self, obj, objtype):
		return functools.partial(self.__call__, obj)
	#

	def __call__(self, original_func):
		decorator_self = self
		def TestCaseWrapper(*args, **kwargs):
			if isinstance(args[0], bool):
				# function
				assert len(args) >= 1
				args = list(args)
				if args[0]:
					del args[0]
					return original_func(*args,**kwargs)
				else:
					return (decorator_self.testAspects, original_func.__name__)
			else:
				# method
				assert len(args) >= 2
				assert isinstance(args[1], bool)
				args = list(args)
				if args[1]:
					del args[1]
					return original_func(*args,**kwargs)
				else:
					return (decorator_self.testAspects, original_func.__name__)
		return TestCaseWrapper
	#

#




