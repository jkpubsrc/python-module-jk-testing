



import typing

from .StringUtils import StringUtils






#
# This class adds convenience methods for managing a list of strings.
#
class StringList(list):

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

	def getMaxLineLength(self) -> int:
		return max([
			len(line) for line in self
		])
	#

	def cloneObject(self):
		return StringList(self)
	#

	def padAllLines(self, maxLen:int) -> list:
		return [
			StringUtils.padRight(line, maxLen) for line in self
		]
	#

	def __eq__(self, __o: object) -> bool:
		#return super().__eq__(__o)

		# let's do this comparison manually just to ensure that the check is performed exacly as expected.

		if len(__o) != len(self):
			return False

		for i in range(0, len(self)):
			if self[i] != __o[i]:
				return False

		return True
	#

	################################################################################################################################
	## Static Methods
	################################################################################################################################

	@staticmethod
	def fromSequenceWithTabs(data):
		return StringList([
			line.replace("\t", "    ") for line in data
		])
	#

#







