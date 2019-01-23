#!/usr/bin/python3



try:
	with open("xxxxxxxx.txt", "r") as f:
		pass
	print("success")
except Exception as ee:
	print("err")
	print(type(ee))
	print(ee.args)
	print(dir(ee))







