from io import StringIO

class StringBuilder:
	def __init__(self) -> None:
		self.buffer = StringIO()
	
	def append(self, text):
		self.buffer.write(text)
	
	def __str__(self) -> str:
		return self.buffer.getvalue()