from jk_logging import BufferLogger, EnumLogLevel

from .TestCaseInstance import TestCaseInstance, EnumEnabledState, EnumProcessingState





class TestResult(object):

	def __init__(self, testCaseInstance:TestCaseInstance, logBuffer:BufferLogger):
		self.name = testCaseInstance.name
		self.timeStamp = testCaseInstance.timeStamp
		self.enabledState = testCaseInstance.enabledState
		self.processingState = testCaseInstance.processingState
		self.duration = testCaseInstance.duration
		self.logBuffer = logBuffer
		self.description = testCaseInstance.description
	#

#













