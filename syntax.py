#Syntaktický analyzátor (Parser)
#Seřazené tokeny z lexikálního analyzátoru roztřídí do několika derivačních stromů seřazených do pole pomocí algoritmu recursive descent parsing
#Derivační strom uchovává pořadí operací, pole derivačních stromů uchovává pořadí příkazů
#Pole derivačních stromů je předáno sémantickému analyzátoru a samotnému interpretu

from error import Error
from expressions import *
from statements import *
from math import pi, e as euler

class Parser:
	def __init__(self, lexerDict):
		self.lineNumbers = list(lexerDict)
		self.tokens = list(lexerDict.values())
		self.posX = -1
		self.posY = 0
	
	def lineNumber(self):
		return self.lineNumbers[self.posX]
	
	def currentToken(self):
		return self.tokens[self.posX][self.posY]
	
	def nextLine(self):
		if self.posX < len(self.lineNumbers) - 1:
			self.posX += 1
			self.posY = 0
			return True
		return False
	
	def endOfStatementError(self):
		if self.currentToken().tokenType == "EndOfLine":
			e = Error("Unexpected end of statement", self.lineNumber())
			e.call()
	
	def endOfLineError(self, ifStat = False):
		if ifStat:
			return
		if self.currentToken().tokenType != "EndOfLine":
			e = Error("Expected end of line", self.lineNumber())
			e.call()
	
	#Parsování příkazů
	def parseStatement(self, ifStat = False):
		command = self.currentToken()

		if command.tokenType != "Command":
			if ifStat:
				if command.tokenType == "Comment":
					e = Error(f"Unexpected comment", self.lineNumber())
					e.call()
				return simpleStatement("GOTO", self.lineNumber(), self.parseOrLogicalExpression())
			if command.tokenType == "Comment":
				return lonelyStatement(command.value, self.lineNumber())
			e = Error(f"Unknown command: \"{command.value}\"", self.lineNumber())
			e.call()
		
		if command.value in ["CLS", "END", "RETURN"]:
			self.posY += 1
			self.endOfLineError(ifStat)
			return lonelyStatement(command.value, self.lineNumber())
		
		if command.value in ["GOTO", "PAUSE", "GOSUB"]:
			self.posY += 1
			arguments = self.parseOrLogicalExpression()
			self.endOfLineError(ifStat)
			return simpleStatement(command.value, self.lineNumber(), arguments)
		
		if command.value in ["ARRAY", "NEXT"]:
			self.posY += 1
			arguments = self.currentToken()
			if arguments.tokenType != "Identifier":
				e = Error("Expected identifier", self.lineNumber())
				e.call()
			self.posY += 1
			self.endOfLineError(ifStat)
			return simpleStatement(command.value, self.lineNumber(), arguments)
		
		if command.value == "PRINT":
			arguments = []
			while True:
				self.posY += 1
				arguments.append(self.parseOrLogicalExpression())
				if self.currentToken().tokenType != "Semicolon":
					break
			self.endOfLineError(ifStat)
			return simpleStatement(command.value, self.lineNumber(), arguments)

		if command.value == "INPUT":
			self.posY += 1
			arguments = [self.parseOrLogicalExpression()]
			if self.currentToken().tokenType != "Semicolon":
				e = Error("Expected semicolon", self.lineNumber())
				e.call()
			self.posY += 1
			arguments.append(self.currentToken())
			if arguments[1].tokenType != "Identifier":
				e = Error("Expected identifier", self.lineNumber())
				e.call()
			self.posY += 1
			self.endOfLineError(ifStat)
			return simpleStatement(command.value, self.lineNumber(), arguments)
		
		if command.value == "LET":
			self.posY += 1
			arguments = [self.currentToken()]
			if arguments[0].tokenType != "Identifier":
				e = Error("Expected identifier", self.lineNumber())
				e.call()
			self.posY += 1
			while self.currentToken().tokenType == "LeftBracket":
				self.posY += 1
				arguments = [BracketToken(self.lineNumber(), arguments[0], self.parseOrLogicalExpression("RightBracket"))]
				self.posY += 1
			if self.currentToken().tokenType != "EqualSign":
				e = Error("Expected equal sign", self.lineNumber())
				e.call()
			self.posY += 1
			arguments.append(self.parseOrLogicalExpression())
			self.endOfLineError(ifStat)
			return simpleStatement(command.value, self.lineNumber(), arguments)
		
		if command.value == "FOR":
			if not ifStat:
				self.posY += 1
				arguments = [self.currentToken()]
				if arguments[0].tokenType != "Identifier":
					e = Error("Expected identifier", self.lineNumber())
					e.call()
				self.posY += 1
				if self.currentToken().tokenType != "EqualSign":
					e = Error("Expected equal sign", self.lineNumber())
					e.call()
				self.posY += 1
				arguments.append(self.parseOrLogicalExpression())
				if self.currentToken().tokenType != "OtherKeyword" or self.currentToken().value != "TO":
					self.endOfStatementError()
					e = Error(f"Unexpected token: \"{self.currentToken().value}\"", self.lineNumber())
					e.call()
				self.posY += 1
				arguments.append(self.parseOrLogicalExpression())
				t = self.currentToken()
				if t.tokenType == "OtherKeyword" and t.value == "STEP":
					self.posY += 1
					arguments.append(self.parseOrLogicalExpression())
				elif t.tokenType != "EndOfLine":
					e = Error(f"Unexpected token: \"{t.value}\"", self.lineNumber())
					e.call()
				return simpleStatement(command.value, self.lineNumber(), arguments)
			e = Error("Unexpected command: \"FOR\"", self.lineNumber())
			e.call()
		
		if command.value == "IF":
			self.posY += 1
			conditions = [self.parseOrLogicalExpression()]
			if self.currentToken().tokenType != "OtherKeyword" or self.currentToken().value != "THEN":
				self.endOfStatementError()
				e = Error(f"Unexpected token: \"{self.currentToken().value}\"", self.lineNumber())
				e.call()
			self.posY += 1
			self.endOfStatementError()
			statements = [self.parseStatement(True)]
			while self.currentToken().tokenType == "OtherKeyword" and self.currentToken().value == "ELSEIF":
				self.posY += 1
				conditions.append(self.parseOrLogicalExpression())
				if self.currentToken().tokenType != "OtherKeyword" or self.currentToken().value != "THEN":
					self.endOfStatementError()
					e = Error(f"Unexpected token: \"{self.currentToken().value}\"", self.lineNumber())
					e.call()
				self.posY += 1
				self.endOfStatementError()
				statements.append(self.parseStatement(True))
			if self.currentToken().tokenType == "OtherKeyword" and self.currentToken().value == "ELSE":
				self.posY += 1
				self.endOfStatementError()
				statements.append(self.parseStatement(True))
			self.endOfLineError(ifStat)
			return ifStatement(self.lineNumber(), conditions, statements)

	#Parsování výrazů - sestupně podle pořadí operací
	#Logické OR (disjunkce)
	def parseOrLogicalExpression(self, parent = None):
		left = self.parseAndLogicalExpression()
		while self.currentToken().tokenType == "LogicalOperator" and self.currentToken().value == "OR":
			operator = self.currentToken().value
			self.posY += 1
			left = BinaryExpression(self.lineNumber(), left, self.parseAndLogicalExpression(), operator)
		if parent != None and self.currentToken().tokenType != parent:
			e = Error("Unexpected end of expression", self.lineNumber())
			e.call()
		return left
	
	#Logické AND (konjunkce)
	def parseAndLogicalExpression(self):
		left = self.parseRelationalExpression()
		while self.currentToken().tokenType == "LogicalOperator" and self.currentToken().value == "AND":
			operator = self.currentToken().value
			self.posY += 1
			left = BinaryExpression(self.lineNumber(), left, self.parseRelationalExpression(), operator)
		return left
	
	#Relační = <> < > <= >=
	def parseRelationalExpression(self):
		left = self.parseSum()
		while self.currentToken().tokenType in ["RelationalOperator", "EqualSign"]:
			operator = self.currentToken().value
			self.posY += 1
			left = BinaryExpression(self.lineNumber(), left, self.parseSum(), operator)
		return left 

	#Aritmetické + -
	def parseSum(self):
		left = self.parseProduct()
		while self.currentToken().tokenType == "ArithmeticOperator" and self.currentToken().value in ["+", "-"]:
			operator = self.currentToken().value
			self.posY += 1
			left = BinaryExpression(self.lineNumber(), left, self.parseProduct(), operator)
		return left 

	#Aritmetické * / %
	def parseProduct(self):
		left = self.parsePower()
		while self.currentToken().tokenType == "ArithmeticOperator" and self.currentToken().value in ["*", "/", "%"]:
			operator = self.currentToken().value
			self.posY += 1
			left = BinaryExpression(self.lineNumber(), left, self.parsePower(), operator)
		return left 

	#Aritmetické **
	def parsePower(self):
		operands = [self.parseFactor()]
		while self.currentToken().tokenType == "ArithmeticOperator" and self.currentToken().value == "**":
			self.posY += 1
			operands.append(self.parseFactor())
		right = operands[-1]
		for i in range(len(operands) - 2, -1, -1):
			right = BinaryExpression(self.lineNumber(), operands[i], right, "**")
		return right

	#Operandy, výrazy v závorkách, zvolání funkcí, konstanty (PI, E)
	def parseFactor(self):
		if self.currentToken().tokenType == "OtherKeyword":
			if self.currentToken().value == "PI":
				self.posY += 1
				return Token("Float", pi)
			if self.currentToken().value == "E":
				self.posY += 1
				return Token("Float", euler)
		
		if self.currentToken().tokenType == "FunctionName":
			token = self.currentToken()
			self.posY += 1
			
			if self.currentToken().tokenType != "LeftParenthesis":
				if self.currentToken().tokenType == "EndOfLine":
					e = Error("Unexpected end of expression", self.lineNumber())
					e.call()
				e = Error(f"Unexpected token: \"{self.currentToken().value}\"", self.lineNumber())
				e.call()
			arguments = []

			while True:
				self.posY += 1
				arguments.append(self.parseOrLogicalExpression())
				if self.currentToken().tokenType == "RightParenthesis":
					break
				if self.currentToken().tokenType != "Comma":
					if self.currentToken().tokenType == "EndOfLine":
						e = Error("Unexpected end of expression", self.lineNumber())
						e.call()
					e = Error(f"Unexpected token: \"{self.currentToken().value}\"", self.lineNumber())
					e.call()
			self.posY += 1
			return FunctionCall(self.lineNumber(), token.value, arguments)

		if self.currentToken().tokenType in ["Integer", "Float", "String", "Identifier"]:
			token = self.currentToken()
			self.posY += 1
			
			if token.tokenType in ["String", "Identifier"]:
				while self.currentToken().tokenType == "LeftBracket":
					self.posY += 1
					expression = self.parseOrLogicalExpression("RightBracket")
					self.posY += 1
					token = BracketToken(self.lineNumber(), token, expression)
			return token
		
		if self.currentToken().value == "-":
			self.posY += 1

			if self.currentToken().tokenType == "OtherKeyword":
				if self.currentToken().value == "PI":
					self.posY += 1
					return NegativeExpression(self.lineNumber(), Token("Float", pi))
				if self.currentToken().value == "E":
					self.posY += 1
					return NegativeExpression(self.lineNumber(), Token("Float", euler))
			
			if self.currentToken().tokenType == "FunctionName":
				token = self.currentToken()
				self.posY += 1
				if self.currentToken().tokenType != "LeftParenthesis":
					if self.currentToken().tokenType == "EndOfLine":
						e = Error("Unexpected end of expression", self.lineNumber())
						e.call()
					e = Error(f"Unexpected token: \"{self.currentToken().value}\"", self.lineNumber())
					e.call()
				arguments = []
				while True:
					self.posY += 1
					arguments.append(self.parseOrLogicalExpression())
					if self.currentToken().tokenType == "RightParenthesis":
						break
					if self.currentToken().tokenType != "Comma":
						if self.currentToken().tokenType == "EndOfLine":
							e = Error("Unexpected end of expression", self.lineNumber())
							e.call()
						e = Error(f"Unexpected token: \"{self.currentToken().value}\"", self.lineNumber())
						e.call()
				self.posY += 1
				return NegativeExpression(self.lineNumber(), FunctionCall(self.lineNumber(), token.value, arguments))
			
			if self.currentToken().tokenType in ["Integer", "Float", "Identifier"]:
				token = self.currentToken()
				self.posY += 1
				if token.tokenType in ["String", "Identifier"]:
					while self.currentToken().tokenType == "LeftBracket":
						self.posY += 1
						expression = self.parseOrLogicalExpression("RightBracket")
						self.posY += 1
						token = BracketToken(self.lineNumber(), token, expression)
				return NegativeExpression(self.lineNumber(), token)
			
			if self.currentToken().tokenType == "LeftParenthesis":
				self.posY += 1
				expression = self.parseOrLogicalExpression("RightParenthesis")
				self.posY += 1
				return NegativeExpression(self.lineNumber(), expression)
			
			if self.currentToken().tokenType == "EndOfLine":
				e = Error("Unexpected end of expression", self.lineNumber())
				e.call()

			e = Error(f"Unexpected token: \"{self.currentToken().value}\"", self.lineNumber())
			e.call()

		if self.currentToken().tokenType == "LeftParenthesis":
			self.posY += 1
			expression = self.parseOrLogicalExpression("RightParenthesis")
			self.posY += 1
			return expression

		if self.currentToken().tokenType == "EndOfLine":
			e = Error("Unexpected end of expression", self.lineNumber())
			e.call()

		e = Error(f"Unexpected token: \"{self.currentToken().value}\"", self.lineNumber())
		e.call()