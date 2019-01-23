#!/usr/bin/python3


import os
import shutil



if os.path.isdir("jk_testing/data"):
	shutil.rmtree("jk_testing/data")
shutil.copytree("staticfiles", "jk_testing/data")
for root, dirs, files in os.walk("jk_testing/data"):
	for f in files:
		os.chmod(os.path.join(root, f), 0o664)





