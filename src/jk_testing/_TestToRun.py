


import typing





#
# This class represents a test that might need to be performed. This class is an internal data structure for managing the test cases.
#
class _TestToRun(object):

	################################################################################################################################
	## Constructor
	################################################################################################################################

	#
	# Constructor method.
	#
	def __init__(self,
			testCallable:typing.Callable,
			bEnabled:bool
		):

		assert callable(testCallable)
		assert isinstance(bEnabled, bool)

		# ----
		
		self.testCallable:typing.Callable = testCallable			# theCallable
		self.bEnabled:bool = bEnabled
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

#



