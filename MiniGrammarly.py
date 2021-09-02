import re
from enum import Enum
from utils import StringBuilder

class Locale(Enum):
	Norwegian = 1
	US = 2

class NumberLocalization:
	"""
	Locale-specific formatting of numbers
	"""
	def __init__(self, original: Locale, destination: Locale) -> None:
		"""Construct a NumberLocalization instance
		original -- The original locale
		destination -- The destination locale
		"""
		self.original = original
		self.destination = destination

		if self.original == Locale.US:
			self.original_thousand_separator = ","
			self.original_decimal_separator = "."
			self.pattern = "\d+(,\d{3})*(.\d+)?"
		else:
			self.original_thousand_separator = "."
			self.original_decimal_separator = ","			
			self.pattern = "\d+(.\d{3})*(,\d+)?"

		if self.destination == Locale.US:
			self.destination_thousand_separator = ","
			self.destination_decimal_separator = "."
		else:
			self.destination_thousand_separator = "."
			self.destination_decimal_separator = ","
	
	def findAllNumbers(self, text: str):
		for i in re.finditer(self.pattern, text, re.S):
			print(i)

	def convert(self, text) -> str:
		"""
		Find and convert all the numbers
		"""

		sb = StringBuilder()
		curr = 0

		for i in re.finditer(self.pattern, text, re.S):
			# Append the previous text
			sb.append(text[curr: i.start()])

			# Formatting
			temp_old = i.group(0)
			decimal_separator_pos = temp_old.find(self.original_decimal_separator)
			
			if decimal_separator_pos >= 0:
				temp_new = temp_old[0:decimal_separator_pos].replace(self.original_thousand_separator, self.destination_thousand_separator) + \
					self.destination_decimal_separator + temp_old[decimal_separator_pos + 1:]
			else:
				temp_new = temp_old.replace(self.original_thousand_separator, self.destination_thousand_separator)

			sb.append(temp_new) # Append the formatted number
			curr = i.end() # Update curr

		# Append the left over text
		sb.append(text[curr:])
		
		return sb

class MiniGrammarly:
	data = [		
		#("\n\n", "\n"), # Double newlines
		("[‘’“”❮❯‹›]|«\s*|\s*»","\""), # Quotation Marks: Left+Right Single, L+R Double, L+R Pointing Double Angle, Heavy L+R Pointing Angle Quotation Mark Ornament, Single Left+Right Pointing Angle
		("(?i)covid","COVID"), # covid, Covid, coVID 
		("(?i)v\wc(\s*|\W)xin","vaccine"), # Vắc-xin, Vac-xin, vac xin, vắc xin, vacxin, vac    xin, vắcxin	
		("\s*,\s*(?!\d)", ", "), # Hello , world. Hello  ,   world. Hello ,world. Hello, world. Hello,world. 10,000
		("\s{2,}", " "), # Double spaces. Ex. Hello   world.
		]
	
	def check(self, instr: str):
		"""
		Scan and correct grammar errors
		
		Params:
		instr: str
			String to check
		"""
		# Dictionary
		for a, b in self.data:
			instr = re.sub(a, b, instr)
		
		# Number Localization
		nlc = NumberLocalization(Locale.Norwegian, Locale.US)
		return nlc.convert(instr).__str__()

def test():
	in_str = "Today, 10.000.999,22 nguoi chet vi covid-19 ,    du da chich vac xin 8.000,3 lieu"
	f = MiniGrammarly()
	print(f.check(in_str))

def test2():
	in_str = "Today, 10.000.999,22 nguoi chet vi covid-19 ,    du da chich vac xin 8.000,3 lieu"
	f = NumberLocalization(Locale.Norwegian, Locale.US)
	out_str = f.convert(in_str)
	print(in_str)
	print(out_str)

def main():
	result = ""
	f = open("raw_input.txt")
	
	grammarly = MiniGrammarly()
	for line in f:
		result += grammarly.check(line)
		# print(doc_format.format(line))

	print(result)

	# Write to file
	fw = open("formatted_input.txt", "w")
	fw.write(result)
	fw.close()
	
if __name__ == "__main__":
	main()
	# test()
	# test2()
	# testStringBuilder()
