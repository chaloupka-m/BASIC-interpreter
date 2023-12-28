#Výrazy
#Instance tříd BracketToken, NegativeExpression, FunctionCall a BinaryExpression jsou uzly v AST
#Funkce log() vrací textový řetězec s vizuální strukturou uzlu -> určený pro výstup na konzoli při testování
#Funkce returnValue() vrací výsledek operace

from error import Error
from lexer import Token
from evaluator import variables
import random
import math

#Výraz, který přistupuje k prvkům pole nebo textového řetězce např.: "String"[0] => "S"
class BracketToken:
	def __init__(self, line, token, value):
		self.line = line
		self.token = token #String, Array nebo Identifier
		self.value = value #Výraz - index

	def log(self):
		return f"{self.token.log()}[{self.value.log()}]"
	
	def returnValue(self):
		if not isinstance(self.value.returnValue(), int):
			e = Error("Expected integer", self.line)
			e.call()
		if self.token.__class__.__name__ == "BracketToken":
			val = self.token.returnValue()
			if isinstance(val, str):
				tokenType = "String"
			elif isinstance(val, int):
				tokenType = "Integer"
			elif isinstance(val, float):
				tokenType = "Float"
			elif isinstance(val, list):
				if self.value.returnValue() >= len(val) or self.value.returnValue() < 0:
					e = Error("Index out of range", self.line)
					e.call()
				return val[self.value.returnValue()]
			self.token = Token(tokenType, val)
		if self.token.tokenType == "String":
			if self.value.returnValue() >= len(self.token.returnValue()) or self.value.returnValue() < 0:
				e = Error("Index out of range", self.line)
				e.call()
			return self.token.returnValue()[self.value.returnValue()]
		if self.token.value in variables.keys():
			if not isinstance(variables[self.token.value], list) and not isinstance(variables[self.token.value], str) :
				e = Error(f"Array {self.token.value} does not exist", self.line)
				e.call()
			if self.value.returnValue() >= len(variables[self.token.value]) or self.value.returnValue() < 0:
				e = Error("Index out of range", self.line)
				e.call()
			return variables[self.token.value][self.value.returnValue()]
		else:
			e = Error(f"Array {self.token.value} does not exist", self.line)
			e.call()

#Výraz obsahující jiný výraz s opačnou hodnotou
class NegativeExpression:
	def __init__(self, line, value):
		self.line = line
		self.value = value

	def log(self):
		return f"-{self.value.log()}"
	
	def returnValue(self):
		if isinstance(self.value.returnValue(), str):
			e = Error("String cannot be negative", self.line)
			e.call()
		if isinstance(self.value.returnValue(), list):
			e = Error("Array connot be negative", self.line)
			e.call()
		return -self.value.returnValue()

#Zvolání jedné z vestavěných funkcí	
class FunctionCall:
	def __init__(self, line, functionName, arguments):
		self.line = line
		self.functionName = functionName
		self.arguments = arguments

	def log(self):
		return f"{self.functionName}({', '.join([argument.log() for argument in self.arguments])})"
	
	def returnValue(self):
		if len(self.arguments) == 1:

			argument = self.arguments[0].returnValue()

			#Číselné funkce
			if isinstance(argument, int) or isinstance(argument, float):
				if self.functionName == "RAND":
					return random.random() * argument
				if self.functionName == "ABS":
					if argument < 0:
						return -argument
					return argument
				if self.functionName == "SGN":
					if argument < 0:
						return -1
					elif argument == 0:
						return 0
					else:
						return 1
				if self.functionName == "ROUND":
					return int(round(argument, 0))
				if self.functionName == "FLOOR":
					return math.floor(argument)
				if self.functionName == "SIN":
					return math.sin(argument)
				if self.functionName == "COS":
					return math.cos(argument)
				if self.functionName == "TAN":
					return math.tan(argument)
				if self.functionName == "ATAN":
					return math.atan(argument)
				if self.functionName == "SQR":
					if argument >= 0:
						sqrt = math.sqrt(argument)
						if sqrt % 1 == 0:
							return int(sqrt)
						return sqrt
				if self.functionName == "EXP":
					return math.e ** argument
				if self.functionName == "LOG":
					if argument > 0:
						return math.log(argument)
					
				if argument >= -1 and argument <= 1:
					if self.functionName == "ASIN":
						return math.asin(argument)
					if self.functionName == "ACOS":
						return math.acos(argument)
					
			#Textové funkce
			if isinstance(argument, str) or isinstance(argument, list):
				if self.functionName == "LEN": #Funkce se dá použít i pro práci s poli
					return len(argument)
				
				if isinstance(argument, str):
					if self.functionName == "UPPERCASE":
						return argument.upper()
					if self.functionName == "LOWERCASE":
						return argument.lower()

		#Textové funkce/funkce pro práci s poli
		if len(self.arguments) == 2:
			arg0 = self.arguments[0].returnValue()
			arg1 = self.arguments[1].returnValue()
			if(isinstance(arg0, str) or isinstance(arg0, list)) and isinstance(arg1, int):
				if self.functionName == "LEFT":
					if arg1 > 0:
						return arg0[:arg1]
					return arg0[0:0]
				if self.functionName == "RIGHT":
					if arg1 > 0:
						return arg0[-arg1:]
					return arg0[0:0]

		if len(self.arguments) == 3:
			arg0 = self.arguments[0].returnValue()
			arg1 = self.arguments[1].returnValue()
			arg2 = self.arguments[2].returnValue()
			if(isinstance(arg0, str) or isinstance(arg0, list)) and isinstance(arg1, int) and isinstance(arg2, int):
				if self.functionName == "MID":
					if arg1 >= 0 and arg2 > 0:
						return arg0[arg1:arg1 + arg2]
					return arg0[0:0]

		e = Error(f"Too many and/or wrong types of arguments passed to {self.functionName}", self.line)
		e.call()

#Binární operace - aritmetické, relační a logické
class BinaryExpression:
	def __init__(self, line, left, right, operator):
		self.line = line
		self.left = left
		self.right = right
		self.operator = operator

	def log(self):
		lString = self.left.log()
		rString = self.right.log()

		return f"BinaryExpression({lString} {self.operator} {rString})"
	
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
		lValue = self.left.returnValue()
		rValue = self.right.returnValue()

		if self.operator == "=":
			return self.val(lValue == rValue)
		if self.operator == "<>":
			return self.val(lValue != rValue)
		
		if isinstance(lValue, list) or isinstance(rValue, list):
			e = Error("This operation cannot be performed with Array data type", self.line)
			e.call()

		if self.operator == "+":
			if isinstance(lValue, str) or isinstance(rValue, str):
				return str(lValue) + str(rValue)
			return self.val(lValue + rValue)
		if self.operator == "AND":
			return self.val(lValue and rValue)
		if self.operator == "OR":
			return self.val(lValue or rValue)
		
		if (isinstance(lValue, str) or isinstance(rValue, str)) and type(lValue) != type(rValue):
			e = Error("This operation cannot be performed between different data types", self.line)
			e.call()

		if self.operator == "<":
			return self.val(lValue < rValue)
		if self.operator == ">":
			return self.val(lValue > rValue)
		if self.operator == "<=":
			return self.val(lValue <= rValue)
		if self.operator == ">=":
			return self.val(lValue >= rValue)

		if isinstance(lValue, str) or isinstance(rValue, str):
			e = Error("This operation cannot be performed with String data type", self.line)
			e.call()

		if self.operator == "-":
			return self.val(lValue - rValue)
		if self.operator == "*":
			return self.val(lValue * rValue)
		if self.operator == "/":
			if rValue == 0:
				e = Error("Zero division", self.line)
				e.call()
			return self.val(lValue / rValue)
		if self.operator == "**":
			if lValue == 0 and rValue < 0:
				e = Error("Zero raised to a negative power", self.line)
				e.call()
			return self.val(lValue ** rValue)
		if self.operator == "%":
			if rValue == 0:
				e = Error("Zero division", self.line)
				e.call()
			return self.val(lValue % rValue)