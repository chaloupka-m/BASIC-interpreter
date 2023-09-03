#Lexikální analyzátor (Lexer)
#Rozdělí vstupní zdrojový text na tokeny - klíčová slova, operátory, identifikátory, názvy funkcí, čísla, textové řetězce...
#Seřazené tokeny jsou poté předány syntaktickému analyzátoru

from error import Error
from evaluator import variables

#Příkazy
commands = ["PRINT", "INPUT", "CLS", "IF", "END", "LET", "GOTO", "FOR", "NEXT", "PAUSE", "GOSUB", "REM", "RETURN", "ARRAY"]

#Logické operátory
logicalOperators = ["AND", "OR"]

#Názvy funkcí
functionNames = ["RAND", "ABS", "SGN", "ROUND", "FLOOR", "SIN", "COS", "TAN", "ASIN", "ACOS", "ATAN", "SQR", "EXP", "LOG", "LEN", "UPPERCASE", "LOWERCASE", "LEFT", "RIGHT", "MID"]

#Ostatní klíčová slova
otherKeywords = ["THEN", "ELSEIF", "ELSE", "TO", "STEP", "PI", "E"]

def isChar(char):
	return char.lower() in "abcdefghijklmnopqrstuvwxyz_"
	
def isNum(num):
	return num in "0123456789"

#Tokeny jsou výstupem lexikálního analyzátoru
#Operandy jsou uchovávány i nadále jako instance třídy Token a jsou listy v AST
class Token:
	def __init__(self, tokenType, value):
		self.tokenType = tokenType
		self.value = value

	def log(self):
		return f"{self.tokenType}({self.value})"
	
	#Vrátí Integer pokud je value celé číslo (ale uložené v paměti jako Float)
	def val(self, value):
		if not isinstance(value, float):
			if isinstance(value, bool):
				if value:
					return 1
				return 0
			return value
		if value % 1 == 0:
			return int(value)
		return value	
	
	def returnValue(self):
		if self.tokenType != "Identifier":
			return self.val(self.value)
		if self.value in variables.keys():
			return self.val(variables[self.value])
		return 0

class Lexer:
	def __init__(self, text):
		self.text = text + "\n"
		self.pos = -1
		self.line = self.lineNumber()

	def currentChar(self):
		return self.text[self.pos]
	
	#Vrátí číslo řádku - nutné před každým příkazem
	def lineNumber(self):
		self.pos += 1

		#Ignoruje mezery nebo odsazení
		while self.currentChar() in [" ", "\t"]:
			self.pos += 1

		#Ignoruje prázdný řádek
		if self.currentChar() == "\n":
			self.pos -= 1
			return None

		#Řádek, který nezačíná číslem řádky vypíše chybovou hlášku
		if not isNum(self.currentChar()):
			e = Error("Expected line number", None)
			e.call()
		
		line = 0
		while isNum(self.currentChar()):
			line = line * 10 + int(self.currentChar())
			self.pos += 1
		self.pos -= 1
		return line
		
	def nextToken(self):
		self.pos += 1

		#Konec řádku
		if self.currentChar() == "\n":
			return Token("EndOfLine", "\n")

		#Mezery nebo odsazení
		elif self.currentChar() in [" ", "\t"]:
			return self.nextToken()

		#Operátory
		#Aritmetické + - * / ** %
		#Relační <> < > <= >=
        #Přiřazovací a relační = (EqualSign)
		elif self.currentChar() == "+":
			return Token("ArithmeticOperator", "+")
		elif self.currentChar() == "-":
			return Token("ArithmeticOperator", "-")
		elif self.currentChar() == "*":
			self.pos += 1
			if self.currentChar() == "*":
				return Token("ArithmeticOperator", "**")
			self.pos -= 1
			return Token("ArithmeticOperator", "*")
		elif self.currentChar() == "/":
			return Token("ArithmeticOperator", "/")
		elif self.currentChar() == "%":
			return Token("ArithmeticOperator", "%")
		elif self.currentChar() == "=":
			return Token("EqualSign", "=")
		elif self.currentChar() == "<":
			self.pos += 1
			if self.currentChar() == "=":
				return Token("RelationalOperator", "<=")
			elif self.currentChar() == ">":
				return Token("RelationalOperator", "<>")
			self.pos -= 1
			return Token("RelationalOperator", "<")
		elif self.currentChar() == ">":
			self.pos += 1
			if self.currentChar() == "=":
				return Token("RelationalOperator", ">=")
			self.pos -= 1
			return Token("RelationalOperator", ">")

		#Závorky ( ) [ ]
		elif self.currentChar() == "(":
			return Token("LeftParenthesis", "(")
		elif self.currentChar() == ")":
			return Token("RightParenthesis", ")")
		elif self.currentChar() == "[":
			return Token("LeftBracket", "[")
		elif self.currentChar() == "]":
			return Token("RightBracket", "]")

		#Oddělovače ; ,
		elif self.currentChar() == ";":
			return Token("Semicolon", ";")
		elif self.currentChar() == ",":
			return Token("Comma", ",")

		#Klíčová slova, identifikátory, logické operátory, názvy funkcí
		elif isChar(self.currentChar()):
			word = ""
			while isChar(self.currentChar()) or isNum(self.currentChar()):
				word += self.currentChar().upper()
				self.pos += 1
			self.pos -= 1
			if word in commands:
				if word == "REM":
					return Token("Comment", word)
				return Token("Command", word)
			elif word in logicalOperators:
				return Token("LogicalOperator", word)
			elif word in functionNames:
				return Token("FunctionName", word)
			elif word in otherKeywords:
				return Token("OtherKeyword", word)
			return Token("Identifier", word)

		#Čísla - Integer, Float
		elif isNum(self.currentChar()):
			number = 0
			decimal = 0
			decimalPointEndingError = False
			while isNum(self.currentChar()) or self.currentChar() == ".":
				if decimal > 0:
					if self.currentChar() == ".":
						e = Error("Unexpected character: \".\"", self.line)
						e.call()
					else:
						decimalPointEndingError = False
						number += int(self.currentChar()) * 10 ** -decimal
						decimal += 1
				else:
					if self.currentChar() == ".":
						decimal = 1
						decimalPointEndingError = True
					else:
						number = number * 10 + int(self.currentChar())
				self.pos += 1
			self.pos -= 1
			if not decimalPointEndingError:
				if decimal == 0:
					return Token("Integer", number)
				else:
					return Token("Float", number)
			e = Error("Unexpected character: \".\"", self.line)
			e.call()

		#Textové řetězce - String
		elif self.currentChar() == "\"":
			quote = self.currentChar()
			openString = True
			string = ""
			self.pos += 1
			while self.currentChar() not in ["\n", "\x00"]:
				if self.currentChar() == quote:
					openString = False
					break
				string += self.currentChar()
				self.pos += 1
			if openString:
				e = Error("Expected end of string", self.line)
				e.call()
			return Token("String", string)

		#Nepoužívané symboly
		e = Error(f"Unexpected character \"{self.currentChar()}\"", self.line)
		e.call()