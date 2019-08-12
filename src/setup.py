from setuptools import setup


def readme():
	with open("README.rst") as f:
		return f.read()



setup(name="jk_testing",
	version="0.2019.4.14",
	description="This python module provides a simple to use infrastructure for running unit tests.",
	author="Jürgen Knauth",
	author_email="pubsrc@binary-overflow.de",
	license="Apache 2.0",
	url="https://github.com/jkpubsrc/python-module-jk-testing",
	download_url="https://github.com/jkpubsrc/python-module-jk-testing/tarball/0.2019.4.14",
	keywords=[
		"testing", "unittests", "tests"
	],
	packages=[
		"jk_testing"
	],
	install_requires=[
		"jk_logging",
                "jk_temporary",
                "jk_json",
		"graphviz",
		"jinja2",
	],
	classifiers=[			# https://pypi.python.org/pypi?%3Aaction=list_classifiers
		"Development Status :: 4 - Beta",
		"Programming Language :: Python :: 3",
		"Topic :: Software Development :: Testing",
		"License :: OSI Approved :: Apache Software License",
	],
	long_description=readme(),
	zip_safe=False,
	#include_package_data=True,
	#package_data = {
	#	"": [
	#		"data/*",
	#		"data/html_default/*",
	#		"data/html_default/files/*",
	#		"data/html_default/files/images/*",
	#		"data/html_default/templates/*",
	#	]
	#}
)








