import os
import sys
import subprocess

from .TestCaseInstance import *
from .NodeMatrix import NodeMatrix




class TestCollectionVisualizer(object):

	IMAGE_VIEWER_CANDIDATES = [
		"/usr/bin/viewnior",		# viewnior: https://siyanpanayotov.com/project/viewnior
		"/usr/bin/nomacs",			# nomacs: https://nomacs.org/
		"/usr/bin/geeqie",			# geeqie: http://geeqie.org/
		"/usr/bin/mirageiv",		# mirageiv: http://mirageiv.sourceforge.net/
		"/usr/bin/eom",				# eye of mate
		"/usr/bin/eog",				# eye of gnome
		"/usr/bin/feh",				# feh: https://feh.finalrewind.org/
		"/usr/bin/display",			# fallback
	]

	def __init__(self):
		pass
	#

	#
	# Determine the color a node should have during visualization
	#
	# @return	str bgColor			The background color selected (or <c>None</c>)
	# @return	str textColor		The text color selected (or <c>None</c>)
	# @return	str lineColor		The foreground color selected (or <c>None</c>)
	#
	def __calcNodeColorCallback(self, testCaseInstance:TestCaseInstance):
		if testCaseInstance.isRoot:
			# test is root
				# bgColor: light blue
				# textColor: dark blue
				# lineColor: dark blue
			return "#f0f0ff", "#f0f0ff", "#d0d0f0"

		if testCaseInstance.processingState == EnumProcessingState.NOT_PROCESSED:
			if testCaseInstance.enabledState == EnumEnabledState.ENABLED_BY_USER:
				# test enabled by user
					# bgColor: light green
					# textColor: dark green
					# lineColor: dark green
				return "#e0ffe0", "#40a040", "#40a040"
			elif testCaseInstance.enabledState == EnumEnabledState.ENABLED_IN_CONSEQUENCE:
				# test enabled in consequence
					# bgColor: light grayish green
					# textColor: dark grayish green
					# lineColor: dark grayish green
				return "#e0f0e0", "#80a080", "#80a080"
			elif testCaseInstance.enabledState == EnumEnabledState.DISABLED:
				# test disabled
					# bgColor: light gray
					# textColor: gray
					# lineColor: gray
				return "#e0e0e0", "#909090", "#909090"
			else:
				raise Exception()
		elif testCaseInstance.processingState == EnumProcessingState.SUCCEEDED:
			# succeeded
				# bgColor: dark green
				# textColor: white
				# lineColor: white
			return "#008000", "#ffffff", "#ffffff"
		elif testCaseInstance.processingState == EnumProcessingState.FAILED:
			# test failed
				# bgColor: dark red
				# textColor: white
				# lineColor: white
			return "#800000", "#ffffff", "#ffffff"
		elif testCaseInstance.processingState == EnumProcessingState.FAILED_CRITICALLY:
			# test failed
				# bgColor: dark red
				# textColor: white
				# lineColor: white
			return "#800000", "#ffffff", "#ffffff"
		else:
			raise Exception() 
	#

	def createSVG(self, collection):
		return collection._nodeMatrix.convertTo("svg", nodeColoringCallback=self.__calcNodeColorCallback)
	#

	def visualize(self, collection, imageViewerPath:str = None):
		if imageViewerPath is None:
			for filePath in TestCollectionVisualizer.IMAGE_VIEWER_CANDIDATES:
				if os.path.isfile(filePath):
					imageViewerPath = filePath
					break
		else:
			assert isinstance(imageViewerPath, str)

		if imageViewerPath is None:
			raise Exception("Autodetection of suitable image viewer failed!")
		elif os.path.isfile(imageViewerPath):
			resultFilePath = collection._nodeMatrix.convertTo("svg", nodeColoringCallback=self.__calcNodeColorCallback)
			subprocess.Popen(["nohup", imageViewerPath, resultFilePath], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
		else:
			raise Exception("No such image viewer: " + str(imageViewerPath))
	#

#


