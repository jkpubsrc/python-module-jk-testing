#!/usr/bin/env python3


from jk_testing import *





@TestCase()
def testCaseZero(ctx):
	ctx.log.notice("We're doing some special tests here ...")
#



@TestCase(
	runAfter="testCaseZero",
	description="This is test A",
)
def testCaseA(ctx):
	ctx.log.notice("We're doing some tests here ...")
#



@TestCase(
	runBefore="testCaseA",
)
def testCaseB(ctx):
	ctx.log.notice("We're doing some other tests here ...")
#



@TestCase(
	requires="testCaseB",
	providesVariable="xx",
)
def testCaseC(ctx):
	ctx.log.notice("We're doing some special tests here ...")
	return {
		"xx": "abc"
	}
#



@TestCase(
	RaisesException(FileNotFoundError, filename="xxx.xx"),
	requiresVariable="xx",
)
def testCaseD(ctx):
	ctx.log.notice("We're doing some special tests here ...")
	with open("xxx.xx", "r") as f:
		pass
#



@TestCase(
	RaisesException(FileNotFoundError, filename="xxx.xx"),
	requiresVariable="xx",
)
def testCaseD2(ctx):
	pass
#



@TestCase()
def testCaseE(ctx):
	ctx.log.notice("äöüßÄÖÜ ...")
	with open("xxx.xx", "r") as f:
		pass
#














testDriver = TestDriver()
testDriver.data["abc"] = "abc"

results = testDriver.runTests([
	(testCaseZero, False),
	(testCaseA, True),
	(testCaseB, False),
	(testCaseC, False),
	(testCaseD2, True),
	(testCaseD, True),
	(testCaseE, True),
])

reporter = TestReporterHTML()
reporter.report(results)















