#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import jk_testing






@jk_testing.TestCase()
def testCaseA(globalVars, log):
	log.notice("We're doing some tests here ...")
#



@jk_testing.TestCase(
	jk_testing.runBefore("testCaseA")
)
def testCaseB(globalVars, log):
	log.notice("We're doing some other tests here ...")
#



@jk_testing.TestCase(
	jk_testing.requires("testCaseB")
)
def testCaseC(globalVars, log):
	log.notice("We're doing some special tests here ...")
#











testDriver = jk_testing.TestDriver()
testDriver.runTests([
	(testCaseA, True),
	(testCaseB, False),
	(testCaseC, True),
])






