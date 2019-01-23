import os
import shutil
from setuptools import setup


def readme():
	with open('README.rst') as f:
		return f.read()


if os.path.isdir("jk_testing/data"):
	shutil.rmtree("jk_testing/data")
shutil.copytree("staticfiles", "jk_testing/data")
for root, dirs, files in os.walk("jk_testing/data"):
	for f in files:
		os.chmod(os.path.join(root, f), 0o664)

setup(name='jk_testing',
	version='0.2019.1.22',
	description='This python module provides a simple to use infrastructure for running unit tests.',
	author='Jürgen Knauth',
	author_email='pubsrc@binary-overflow.de',
	license='Apache 2.0',
	url='https://github.com/jkpubsrc/python-module-jk-testing',
	download_url='https://github.com/jkpubsrc/python-module-jk-testing/tarball/0.2019.1.22',
	keywords=[
		"testing", "unittests", "tests"
	],
	packages=[
		'jk_testing'
	],
	install_requires=[
		"jk_logging",
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
	package_data = {
		"": [
			"data/*",
			"data/html_default/*",
			"data/html_default/files/*",
			"data/html_default/files/images/*",
			"data/html_default/templates/*",
		]
	}
)

shutil.rmtree("jk_testing/data")







