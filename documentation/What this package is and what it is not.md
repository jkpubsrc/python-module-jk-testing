What this package is and what it is not
=======================================

Short description
-----------------

This is a python package providing support for building simple unint tests.

A unit test is basically a single function. The function contains code you write in order to perform a test on a specific feature of your code.

A set of unit tests will form a test suite. A test driver provided by this package will receive such a test suite and run all tests defined.

Why this testing framework exists
---------------------------------

This package initially evolved out of simple implementations and refactorizations of some testing code for a python module. Over the time this code "grew" as it was improved slightly over time. At some point the code has been factored out into a standalone package, a bit rewritten and documented for public use.

Advantages and limitations
--------------------------

This package provides a very simple way for implementing unit tests. If you need a simple way to perform tests on your code, just implement one or more test functions and you're ready to test. If you do not require more fancy things this test framework will perfectly do the job: Run a bunch of test methods, collect it's output and present a short statistic.

But if you need more fancy things this test framework is probably not what you want. At least not right now though this project will likely grow further and implement more features over time.










