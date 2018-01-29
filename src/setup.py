from setuptools import setup


def readme():
	with open('README.rst') as f:
		return f.read()


setup(name='jk_testing',
	version='0.2018.1.29',
	description='This python module provides a simple to use infrastructure for running unit tests.',
	author='Jürgen Knauth',
	author_email='pubsrc@binary-overflow.de',
	license='Apache 2.0',
	url='https://github.com/jkpubsrc/python-module-jk-testing',
	download_url='https://github.com/jkpubsrc/python-module-jk-testing/tarball/0.2018.1.29',
	keywords=[
		"testing", "unittests", "tests"
	],
	packages=[
		'jk_testing'
	],
	install_requires=[
		"jk_logging",
	],
	include_package_data=True,
	classifiers=[			# https://pypi.python.org/pypi?%3Aaction=list_classifiers
		"Development Status :: 4 - Beta",
		"Programming Language :: Python :: 3",
		"Topic :: Software Development :: Testing",
		"License :: OSI Approved :: Apache Software License",
	],
	long_description=readme(),
	zip_safe=False)

