
from .TestResult import TestResult
from .TestCollectionVisualizer import TestCollectionVisualizer
from .TestCaseCollection import TestCaseCollection




class TestResultCollection(object):

	def __init__(self, testCaseCollection:TestCaseCollection, testCollectionVisualizer:TestCollectionVisualizer):
		self.__testCaseCollection = testCaseCollection
		self.__nodeMatrix = testCaseCollection._nodeMatrix
		self.testResults = []
		self.countTestsNotYetPerformed = 0
		self.countTestsSucceeded = 0
		self.countTestsFailed = 0
		self.totalTestDuration = 0
		self.totalTestRuntime = 0
		self.__testCollectionVisualizer = testCollectionVisualizer
	#

	@property
	def countTestsPerformed(self):
		return self.countTestsFailed + self.countTestsSucceeded
	#

	@property
	def _nodeMatrix(self):
		return self.__nodeMatrix
	#

	def createSVG(self):
		return self.__testCollectionVisualizer.createSVG(self)
	#

	def visualize(self, imageViewerPath:str = None):
		return self.__testCollectionVisualizer.visualize(self, imageViewerPath)
	#

#


