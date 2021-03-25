



import jk_terminal_essentials

from .SimpleTextLineOutputBuffer import SimpleTextLineOutputBuffer






class OutputComparison(object):

	################################################################################################################################
	## Constructor
	################################################################################################################################

	#
	# Constructor method.
	#
	def __init__(self):
		self.buf1intro = SimpleTextLineOutputBuffer()
		self.buf1 = SimpleTextLineOutputBuffer()
		self.buf2intro = SimpleTextLineOutputBuffer()
		self.buf2 = SimpleTextLineOutputBuffer()
	#

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	################################################################################################################################
	## Helper Methods
	################################################################################################################################

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	def dump(self) -> bool:
		wbuf1 = max(self.buf1intro.width, self.buf1.width)
		wbuf2 = max(self.buf2intro.width, self.buf2.width)
		totalWidth = 4 + 3 + wbuf1 + 3 + wbuf2 + 2

		_colFrame = jk_terminal_essentials.FGCOLOR_LIGHT_CYAN

		print()
		print(_colFrame + "=" * totalWidth + jk_terminal_essentials.STYLE_RESET)

		for rowNo in range(max(self.buf1intro.height, self.buf2intro.height)):
			t1 = self.buf1intro.get(rowNo)
			t2 = self.buf2intro.get(rowNo)
			s = [
				"    ",

				_colFrame,
				" | ",
				jk_terminal_essentials.STYLE_RESET,

				t1,
				" " * (wbuf1 - len(t1)),

				_colFrame,
				" | ",
				jk_terminal_essentials.STYLE_RESET,

				t2,
				" " * (wbuf2 - len(t2)),

				_colFrame,
				" |",
				jk_terminal_essentials.STYLE_RESET,
			]
			print("".join(s))

		s = [
			_colFrame,
			"    ",
			" | ",
			"~" * wbuf1,
			" | ",
			"~" * wbuf2,
			" |",
			jk_terminal_essentials.STYLE_RESET,
		]
		print("".join(s))

		bHadErrors = False
		for rowNo in range(max(self.buf1.height, self.buf2.height)):
			t1 = self.buf1.get(rowNo)
			t2 = self.buf2.get(rowNo)
			bEq = t1 == t2
			if not bEq:
				bHadErrors = True

			s = [
				jk_terminal_essentials.FGCOLOR_LIGHT_YELLOW,
				str(rowNo).rjust(4, " "),

				_colFrame,
				" | ",

				jk_terminal_essentials.BGCOLOR_DARK_GRAY if bEq else jk_terminal_essentials.BGCOLOR_RED,
				jk_terminal_essentials.FGCOLOR_LIGHT_GREEN if bEq else jk_terminal_essentials.FGCOLOR_WHITE,
				t1,
				jk_terminal_essentials.STYLE_RESET,
				" " * (wbuf1 - len(t1)),

				_colFrame,
				" | ",

				jk_terminal_essentials.BGCOLOR_DARK_GRAY if bEq else jk_terminal_essentials.BGCOLOR_RED,
				jk_terminal_essentials.FGCOLOR_LIGHT_GREEN if bEq else jk_terminal_essentials.FGCOLOR_WHITE,
				t2,
				jk_terminal_essentials.STYLE_RESET,
				" " * (wbuf2 - len(t2)),

				_colFrame,
				" |",
				jk_terminal_essentials.STYLE_RESET,
			]
			print("".join(s))

		print(_colFrame + "=" * totalWidth + jk_terminal_essentials.STYLE_RESET)
		print()

		return bHadErrors
	#

	def compare(self) -> bool:
		for rowNo in range(max(self.buf1.height, self.buf2.height)):
			t1 = self.buf1.get(rowNo)
			t2 = self.buf2.get(rowNo)
			bEq = t1 == t2
			if not bEq:
				return True

		return False
	#

#
















