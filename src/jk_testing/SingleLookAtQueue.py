
class SingleLookAtQueue(object):

	def __init__(self):
		self.__data = []
		self.__lookedAt = set()
	#

	def add(self, item):
		itemID = id(item)
		if itemID not in self.__lookedAt:
			self.__data.append(item)
			self.__lookedAt.add(itemID)
	#

	def addAll(self, items):
		for item in items:
			itemID = id(item)
			if itemID not in self.__lookedAt:
				self.__data.append(item)
				self.__lookedAt.add(itemID)
	#

	def retrieve(self):
		if self.__data:
			ret = self.__data[0]
			del self.__data[0]
			return ret
		else:
			return None
	#

	def isNotEmpty(self):
		return len(self.__data) > 0
	#

	def isEmpty(self):
		return len(self.__data) == 0
	#

#



