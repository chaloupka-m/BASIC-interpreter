#Sémantický analyzátor a interpret (Evaluator)
#Při interpretaci se provádí sémantická analýza - ověřování správnosti datových typů, identifikátorů...
#Interpret provádí samotnou logiku kódu a vykonává jednotlivé instrukce

import os
from time import sleep
import math
from error import Error

variables = {} #Ukládání proměnných
forLoops = {} #Informace o proměnných použitých pro cyklus FOR
subroutines = [] #Aktuálně probíhající subrutiny

class Evaluator:
	def __init__(self, statements):
		self.statements = statements
		self.pos = 0

	#Vyhledá řádku při použití GOTO nebo GOSUB
	def searchLine(self, line, stats, index = 0):
		if len(stats) == 0:
			e = Error(f"There is no line with number {line}", self.lineNumber())
			e.call()
		if line == stats[math.floor(len(stats) / 2)].line:
			return index + math.floor(len(stats) / 2)
		if line < stats[math.floor(len(stats) / 2)].line:
			return self.searchLine(line, stats[:math.floor(len(stats) / 2)], index)
		return self.searchLine(line, stats[math.floor(len(stats) / 2) + 1:], index + math.floor(len(stats) / 2) + 1)

	def lineNumber(self):
		return self.statements[self.pos].line
	
	def currentStatement(self):
		return self.statements[self.pos]
	
	def run(self):
		while self.pos < len(self.statements):
			if not self.evaluate(self.currentStatement()):
				return
			self.pos += 1
	
	def evaluate(self, stat):
		if stat.__class__.__name__ == "lonelyStatement":
			if stat.command == "END":
				return False
			
			elif stat.command == "CLS":
				os.system("cls")

			elif stat.command == "RETURN":
				if len(subroutines) == 0:
					e = Error("There is no running subroutine", self.lineNumber())
					e.call()
				self.pos = subroutines[-1]
				subroutines.pop(-1)
		
		elif stat.__class__.__name__ == "simpleStatement":
			if stat.command == "PRINT":
				logs = ""
				for a in stat.arguments:
					logs += str(a.returnValue())
				print(logs)

			elif stat.command == "LET":
				node = stat.arguments[0]
				newValue = stat.arguments[1].returnValue()
				if isinstance(newValue, list):
					newValue = newValue.copy()

				if node.__class__.__name__ == "BracketToken":
					expr = []
					while node.__class__.__name__ == "BracketToken":
						if not isinstance(node.value.returnValue(), int):
							e = Error("Expected integer", self.lineNumber())
							e.call()
						if node.value.returnValue() < 0:
							e = Error("Index out of range", self.lineNumber())
							e.call()
						expr.insert(0, node.value.returnValue())
						node = node.token
						
					if node.value not in variables.keys():
						e = Error(f"Array {node.value} does not exist", self.lineNumber())
						e.call()

					if not isinstance(variables[node.value], list):
						e = Error(f"{node.value} is not an array", self.lineNumber())
						e.call()

					def setValue(arr, coordinates, newValue):
						while len(arr) <= coordinates[0]:
							arr.append(0)
						if len(coordinates) == 1:
							arr[coordinates[0]] = newValue
						else:
							if not isinstance(arr[coordinates[0]], list):
								arr[coordinates[0]] = []
							setValue(arr[coordinates[0]], coordinates[1:], newValue)

					setValue(variables[node.value], expr, newValue)
				else:	
					variables[node.value] = newValue
			
			elif stat.command == "ARRAY":
				variables[stat.arguments.value] = []
			
			elif stat.command == "INPUT":
				variables[stat.arguments[1].value] = number(input(stat.arguments[0].returnValue()))
			
			elif stat.command == "FOR":
				for a in stat.arguments[1:]:
					if isinstance(a.returnValue(), str):
						e = Error("Unxpected string", self.lineNumber())
						e.call()
					if isinstance(a.returnValue(), list):
						e = Error("Unexpected array", self.lineNumber())
						e.call()
				variables[stat.arguments[0].value] = stat.arguments[1].returnValue()
				forLoops[stat.arguments[0].value] = [self.pos] + [a.returnValue() for a in stat.arguments[2:]]
			
			elif stat.command == "NEXT":
				if not stat.arguments.value in forLoops.keys():
					e = Error("There is no for loop using this variable", self.lineNumber())
					e.call()
				if len(forLoops[stat.arguments.value]) == 3:
					step = forLoops[stat.arguments.value][2]
					if step == 0:
						e = Error("Step cannot be zero", self.lineNumber())
						e.call()
				else:
					step = 1
				if isinstance(variables[stat.arguments.value], str):
					e = Error("Variable used in for loop cannot be string", self.lineNumber())
					e.call()
				if isinstance(variables[stat.arguments.value], list):
					e = Error("Variable used in for loop cannot be array", self.lineNumber())
					e.call()
				if(variables[stat.arguments.value] + step >= forLoops[stat.arguments.value][1] and step < 0) or (variables[stat.arguments.value] + step <= forLoops[stat.arguments.value][1] and step > 0):
					variables[stat.arguments.value] += step
					self.pos = forLoops[stat.arguments.value][0]
			
			elif stat.command == "GOTO":
				if isinstance(stat.arguments.returnValue(), str):
					e = Error("Expected line number", self.lineNumber())
					e.call()
				if isinstance(stat.arguments.returnValue(), float):
					e = Error("Line number cannot be float", self.lineNumber())
					e.call()
				if isinstance(stat.arguments.returnValue(), list):
					e = Error("Unexpected array", self.lineNumber())
					e.call()
				self.pos = self.searchLine(stat.arguments.returnValue(), self.statements) - 1
			
			elif stat.command == "GOSUB":
				if isinstance(stat.arguments.returnValue(), str):
					e = Error("Expected line number", self.lineNumber())
					e.call()
				if isinstance(stat.arguments.returnValue(), float):
					e = Error("Line number cannot be float", self.lineNumber())
					e.call()
				if isinstance(stat.arguments.returnValue(), list):
					e = Error("Unexpected array", self.lineNumber())
					e.call()
				subroutines.append(self.pos)
				self.pos = self.searchLine(stat.arguments.returnValue(), self.statements) - 1
			
			#PAUSE
			else:
				delay = stat.arguments.returnValue()
				if isinstance(delay, str):
					e = Error("Unxpected string", self.lineNumber())
					e.call()
				if isinstance(delay, list):
					e = Error("Unexpected array", self.lineNumber())
					e.call()
				if delay < 0:
					delay = 0
				sleep(delay/1000)
		
		#IF
		else:
			i = 0
			while stat.conditions[i].returnValue() == 0:
				i += 1
				if i == len(stat.conditions):
					break
			if i < len(stat.statements):
				if not self.evaluate(stat.statements[i]):
					return False

		return True

def isNum(num):
	return num in "0123456789"

#Převede uživatelský vstup INPUT na Integer nebo Float, pokud se jedná o číslo
def number(string):
	if string == "":
		return string
	pos = 0
	negative = False
	if string[pos] == "-":
		pos += 1
		negative = True
	if isNum(string[pos]):
		number = 0
		decimal = 0
		decimalPointEndingError = False
		while isNum(string[pos]) or string[pos] == ".":
			if decimal > 0:
				if string[pos] == ".":
					return string
				else:
					decimalPointEndingError = False
					number += int(string[pos]) * 10 ** -decimal
					decimal += 1
			else:
				if string[pos] == ".":
					decimal = 1
					decimalPointEndingError = True
				else:
					number = number * 10 + int(string[pos])
			pos += 1
			if pos == len(string):
				break
		if not decimalPointEndingError:
			if negative:
				return -number
			return number
	return string