import os
import sys
import shutil
import http.server
import socketserver
import webbrowser
import urllib
import posixpath

import jk_logging
import jk_json

from jinja2 import Environment, FileSystemLoader, select_autoescape, Template

from .TestResultCollection import *
from .TestResult import *




class ResultsHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):

	def __init__(self, rootDirPath:str, request, client_address, server):
		self.__rootDirPath = os.path.realpath(rootDirPath)
		super().__init__(request, client_address, server)
	#

	def translate_path(self, path):
		"""Translate a /-separated PATH to the local filename syntax.

		Components that mean special things to the local file system
		(e.g. drive or directory names) are ignored.  (XXX They should
		probably be diagnosed.)

		"""
		# abandon query parameters
		path = path.split('?',1)[0]
		path = path.split('#',1)[0]
		# Don't forget explicit trailing slash when normalizing. Issue17324
		trailing_slash = path.rstrip().endswith('/')
		try:
			path = urllib.parse.unquote(path, errors='surrogatepass')
		except UnicodeDecodeError:
			path = urllib.parse.unquote(path)
		path = posixpath.normpath(path)
		words = path.split('/')
		words = filter(None, words)
		path = self.__rootDirPath
		for word in words:
			if os.path.dirname(word) or word in (os.curdir, os.pardir):
				# Ignore components that are not a simple file/directory name
				continue
			path = os.path.join(path, word)
		if trailing_slash:
			path += '/'
		return path
	#	

#


class ResultsHTTPServer(socketserver.TCPServer):

	allow_reuse_address = True

	def __init__(self, rootDirPath:str):
		super().__init__(("", 9096), ResultsHTTPRequestHandler)
		self.__rootDirPath = rootDirPath
	#

	def finish_request(self, request, client_address):
		"""Finish one request by instantiating RequestHandlerClass."""
		self.RequestHandlerClass(self.__rootDirPath, request, client_address, self)
	#

#



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

	def report(self,
			testResultCollection:TestResultCollection,
			outDirPath:str="results",
			showInWebBrowser:bool=True,
			serveWithWebServer:bool=False,
			webbrowserType:str=None
		):

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

		# ----

		if showInWebBrowser:
			httpd = ResultsHTTPServer(outDirPath)
			print("Running web server. For results see: http://localhost:9096/")
			webbrowser.get(webbrowserType).open("http://localhost:9096/", new=1)
			httpd.serve_forever()
		elif serveWithWebServer:
			httpd = ResultsHTTPServer(outDirPath)
			print("Running web server. For results see: http://localhost:9096/")
			httpd.serve_forever()
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
				"logBuffer": testResult.logBuffer.toJSONPretty()["logData"],
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
				"logBuffer": testResult.logBuffer.toJSONPretty()["logData"],
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








