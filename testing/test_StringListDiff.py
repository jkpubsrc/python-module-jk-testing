#!/usr/bin/python3



from jk_testing.utils.StringList import StringList
from jk_testing.utils.StringListDiff import StringListDiff




listA = StringList([
	"foo",
	"bar",
	"foobar",
])

listB = StringList([
	"foo",
	"bar",
	"fooBAR",
])

diff = StringListDiff("listA", listA, "listB", listB)

print()
diff.dump()
print()

print(diff.areAllLinesEqual)












































