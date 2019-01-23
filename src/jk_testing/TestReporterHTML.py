import os
import sys
import shutil

import jk_logging
import jk_json

from jinja2 import Environment, FileSystemLoader, select_autoescape, Template

from .TestResultCollection import *
from .TestResult import *





class TestReporterHTML(object):

	def __init__(self):
		#self.__staticFilesDir = os.path.join(os.getcwd(), "files")
		self.__staticFilesDir = os.path.join(os.path.dirname(__file__), "data", "html_default", "files")

		#self.__templateDir = os.path.join(os.getcwd(), "templates")
		self.__templateDir = os.path.join(os.path.dirname(__file__), "data", "html_default", "templates")

		self.__env = Environment(
			loader=FileSystemLoader(self.__templateDir),
			autoescape=select_autoescape(["html", "xml"])
		)
		self.__templateTestCase = self.__env.get_template("testcase.html")
		self.__templateOverview = self.__env.get_template("index.html")
	#

	def report(self, testResultCollection:TestResultCollection, outDirPath:str="results"):
		if not os.path.isabs(outDirPath):
			outDirPath = os.path.abspath(outDirPath)

		if not os.path.isdir(outDirPath):
			os.makedirs(outDirPath)
		shutil.rmtree(outDirPath)

		# ----

		shutil.copytree(self.__staticFilesDir, outDirPath)

		# ----

		for testResult in testResultCollection.testResults:
			self.__writeResultFile(testResult, outDirPath)

		self.__writeOverviewFile(testResultCollection, outDirPath)
	#

	def __writeResultFile(self, testResult:TestResult, outDirPath:str):

		jsonTestRecord = {
				"id": "test_" + testResult.name,
				"file": "test_" + testResult.name + ".html",
				"name": testResult.name,
				"timeStamp": testResult.timeStamp,
				"enabledState": str(testResult.enabledState),
				"processingState": str(testResult.processingState),
				"duration": testResult.duration,
				"logBuffer": testResult.logBuffer.getDataAsPrettyJSON(),
				"description": testResult.description,
			}

		content = self.__templateTestCase.render(testRecord=jsonTestRecord)
		filePath = os.path.join(outDirPath, "test_" + testResult.name + ".html")
		print("Writing to: " + filePath)
		with open(filePath, "w") as f:
			f.write(content)
	#

	def __writeOverviewFile(self, testResultCollection:TestResultCollection, outDirPath:str):
		jsonTestRecords = []
		for testResult in testResultCollection.testResults:
			jsonTestRecords.append({
				"id": "test_" + testResult.name,
				"file": "test_" + testResult.name + ".html",
				"name": testResult.name,
				"timeStamp": testResult.timeStamp,
				"enabledState": str(testResult.enabledState),
				"processingState": str(testResult.processingState),
				"duration": testResult.duration,
				"logBuffer": testResult.logBuffer.getDataAsPrettyJSON(),
				"description": testResult.description,
			})

		tempFilePath = testResultCollection.createSVG()
		with open(tempFilePath, "r") as f:
			svgLines = f.readlines()
		os.unlink(tempFilePath)

		while (len(svgLines) > 0) and not svgLines[0].startswith("<svg"):
			del svgLines[0]

		content = self.__templateOverview.render(
			svg="".join(svgLines),
			testRecords=jsonTestRecords,
			summary={
				"countTestsPerformed": testResultCollection.countTestsSucceeded + testResultCollection.countTestsFailed,
				"countTestsNotYetPerformed": testResultCollection.countTestsNotYetPerformed,
				"countTestsSucceeded": testResultCollection.countTestsSucceeded,
				"countTestsFailed": testResultCollection.countTestsFailed,
				"totalTestRuntime": testResultCollection.totalTestRuntime,
				"totalTestDuration": testResultCollection.totalTestDuration,
			}
			)
		filePath = os.path.join(outDirPath, "index.html")
		print("Writing: " + filePath)
		with open(filePath, "w") as f:
			f.write(content)
	#

#








