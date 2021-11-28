


import typing
import jk_terminal_essentials

from .StringList import StringList
from .StringUtils import StringUtils





class StringListDiff(object):

	################################################################################################################################
	## Constructor
	################################################################################################################################

	def __init__(self, leftCaption:str, leftLines:StringList, rightCaption:str, rightLines:StringList, comparatorFunc = None) -> None:
		assert isinstance(leftCaption, str)
		assert isinstance(leftLines, StringList)
		assert isinstance(rightCaption, str)
		assert isinstance(rightLines, StringList)

		self.__left = leftLines.cloneObject()
		self.__leftNumberOfLines = len(self.__left)
		self.__leftColumnWidth = max(self.__left.getMaxLineLength(), len(leftCaption))
		self.__leftCaption = leftCaption

		self.__right = rightLines.cloneObject()
		self.__rightNumberOfLines = len(self.__right)
		self.__rightColumnWidth = max(self.__right.getMaxLineLength(), len(rightCaption))
		self.__rightCaption = rightCaption

		self.__maxLines = max(len(leftLines), len(rightLines))

		while len(self.__left) < self.__maxLines:
			self.__left.append(None)
		while len(self.__right) < self.__maxLines:
			self.__right.append(None)

		# ----

		if comparatorFunc is None:
			comparatorFunc = self.__compare

		self.__comparisonResults = []
		self.__finalResult = self.__leftNumberOfLines == self.__rightNumberOfLines
		for i in range(0, self.__maxLines):
			b = comparatorFunc(self.__left[i], self.__right[i])
			if not b:
				self.__finalResult = False
			self.__comparisonResults.append(b)
	#

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	@property
	def areAllLinesEqual(self) -> bool:
		return self.__finalResult
	#

	################################################################################################################################
	## Helper Methods
	################################################################################################################################

	def __compare(self, lineA:typing.Union[str,None], lineB:typing.Union[str,None]) -> bool:
		if lineA is None:
			if lineB is None:
				return True
			else:
				return False
		else:
			if lineB is None:
				return False
			else:
				return lineA == lineB
	#

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	def __bool__(self) -> bool:
		return self.__finalResult
	#

	def __len__(self):
		return self.__maxLines
	#

	def __getitem__(self, index):
		assert isinstance(index, int)
		return (
			self.__comparisonResults[index],
			self.__left[index]		if index < self.__leftNumberOfLines		else None,
			self.__right[index]		if index < self.__rightNumberOfLines	else None,
		)
	#

	def __iter__(self):
		for i in range(0, self.__maxLines):
			yield self.__getitem__(i)
	#

	def dump(self, bColor:bool = True):
		_exEQ = ( " | ", " | ", " |\n" )
		_exNE = ( "X> ", " X ", " <X\n" )
		midLineLength = len(_exNE[1]) + self.__leftColumnWidth + self.__rightColumnWidth
		topbar = " /=" + "=" * midLineLength + "=\\"
		midbar = " |-" + "-" * self.__leftColumnWidth + "---" + "-" * self.__rightColumnWidth + "-|"
		bottombar = " \\=" + "=" * midLineLength + "=/"
		if bColor:
			_colHead = ( jk_terminal_essentials.BGCOLOR_DARK_GRAY + jk_terminal_essentials.FGCOLOR_WHITE, jk_terminal_essentials.STYLE_RESET )
			_colEQ = ( jk_terminal_essentials.BGCOLOR_DARK_GRAY + jk_terminal_essentials.FGCOLOR_WHITE, jk_terminal_essentials.STYLE_RESET )
			_colNE = ( jk_terminal_essentials.BGCOLOR_RED + jk_terminal_essentials.FGCOLOR_BLACK, jk_terminal_essentials.STYLE_RESET )
		else:
			_colHead = ( "", "" )
			_colEQ = ( "", "" )
			_colNE = ( "", "" )

		output = [
			topbar, "\n",
			_exEQ[0],
				StringUtils.padRight(_colHead[0] + self.__leftCaption + _colHead[1], self.__leftColumnWidth, slen=len(self.__leftCaption)),
				_exEQ[1],
				StringUtils.padRight(_colHead[0] + self.__rightCaption + _colHead[1], self.__rightColumnWidth, slen=len(self.__rightCaption)),
				_exEQ[2],
			midbar, "\n",
		]

		i = 0
		for bIsEqual in self.__comparisonResults:
			markers = _exEQ if bIsEqual else _exNE
			colors = _colEQ if bIsEqual else _colNE
			leftLine = self.__left[i] if i < self.__leftNumberOfLines else ""
			rightLine = self.__right[i] if i < self.__rightNumberOfLines else ""

			output.append(markers[0])
			output.append(
				StringUtils.padRight(colors[0] + leftLine + colors[1], self.__leftColumnWidth, slen=len(leftLine))
			)
			output.append(markers[1])
			output.append(
				StringUtils.padRight(colors[0] + rightLine + colors[1], self.__rightColumnWidth, slen=len(rightLine))
			)
			output.append(markers[2])
			i += 1

		output.append(bottombar)
	
		print("".join(output))
	#

#







