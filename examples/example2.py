#!/usr/bin/python3


import os

import jk_testing
import jk_json






class TestSetup(object):

	def __init__(self, name):
		self.__name = name
	#

	def name(self):
		return self.__name
	#

	@jk_testing.TestCase()
	def __call__(self, ctx):
		raise Exception()
	#

#


testDriver = jk_testing.TestDriver()

results = testDriver.runTests([
	(TestSetup("abc-test"), True),
])

reporter = jk_testing.TestReporterHTML()
reporter.report(results, showInWebBrowser=True)









