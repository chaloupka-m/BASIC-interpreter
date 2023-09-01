import sys
import os
from lexer import Lexer
from syntax import Parser
from evaluator import Evaluator, number
from error import Error, ErrorException

commands = ["END", "LIST", "RUN", "CLS", "NEW"]
argumentCommands = ["DEL", "OPEN"]

openedFile = ""

def sortCode(dict):
	keys = list(dict)
	keys.sort()
	sortedDict = {i: dict[i] for i in keys}
	return sortedDict

def writeFile(filename, content):
	global openedFile

	file = open(filename, "w", encoding="utf-8")

	openedFile = filename

	for i in range(len(content)):
		text = content[i]
		if i < len(content) - 1:
			text += "\n"
		file.write(text)
	file.close()

def loadFile(filename, exit = False):
	global openedFile

	try:
		file = open(filename, "r", encoding="utf-8")
	except:
		e = Error("File not found", None)
		if exit:
			e.call(True)
		print(f"Error: {e.message}")
		return {}

	openedFile = filename
	codeFile = {}
	for code in file:
		code = code.replace("\n", "")
		if code == "":
			continue
		try:
			lexer = Lexer(code)
		except ErrorException:
			sys.exit()
		codeFile[lexer.line] = code
	
	return sortCode(codeFile)

def editor():
	global openedFile

	codeFile = {}
	while True:
		code = input("> ")
		
		if code == "":
			continue

		codeArr = code.split()
		codeFile = sortCode(codeFile)
		values = list(codeFile.values())
		
		if codeArr[0].upper() in commands:
			if len(codeArr) > 1:
				e = Error("Too many arguments", None)
				print(f"Error: {e.message}")
				continue

			code = code.upper()

			if code == "END":
				sys.exit()
			
			if code == "LIST":
				for i in values:
					print(i)
			
			elif code == "RUN":
				try:
					interpret(values)
				except ErrorException:
					continue
			
			elif code == "CLS":
				os.system("cls")
			
			elif code == "NEW":
				codeFile = {}
				openedFile = ""

		elif codeArr[0].upper() in argumentCommands:
			if len(codeArr) > 2:
				e = Error("Too many arguments", None)
				print(f"Error: {e.message}")
				continue

			if len(codeArr) == 1:
				e = Error("Expected argument", None)
				print(f"Error: {e.message}")
				continue

			codeArr[0] = codeArr[0].upper()

			if codeArr[0] == "DEL":
				line = number(codeArr[1])
				if line in list(codeFile):
					codeFile.pop(line)

			elif codeArr[0] == "OPEN":
				filename = codeArr[1]
				if filename[-4:] != ".txt":
					filename += ".txt"
				codeFile = loadFile(f"Programy BASIC\{filename}")

		elif codeArr[0].upper() == "SAVE":
			if len(codeArr) == 1:
				if openedFile != "":
					writeFile(openedFile, list(codeFile.values()))
				else:
					e = Error("Expected filename", None)
					print(f"Error: {e.message}")

			elif len(codeArr) == 2:
				filename = codeArr[1]
				if filename[-4:] != ".txt":
					filename += ".txt"
				writeFile(f"Programy BASIC\{filename}", list(codeFile.values()))

			else:
				e = Error("Too many arguments", None)
				print(f"Error: {e.message}")

		else:
			try:
				lexer = Lexer(code)
			except ErrorException:
				continue
			else:
				codeFile[lexer.line] = code
				
def interpret(file):
	lexerDict = {}
	for code in file:
		lexer = Lexer(code)
		tokenArr = []
		while True:
			token = lexer.nextToken()
			tokenArr.append(token)
			if(token.tokenType == "Comment"):
				lexerDict[lexer.line] = tokenArr
				break
			if(token.tokenType == "EndOfLine"):
				if len(tokenArr) > 1:
					lexerDict[lexer.line] = tokenArr
				elif lexer.line != None:
					e = Error("Expected command", lexer.line)
					e.call()
				break	

	### print("LEXER:")
	### for number in lexerDict:
	### 	print("Line number: ", number)
	### 	for item in lexerDict[number]:
	### 		print(item.tokenType, item.value)

	parser = Parser(lexerDict)
	statements = []

	### print("PARSER:")
	while parser.nextLine():
		statement = parser.parseStatement()
		statements.append(statement)
		### print(statement.log())

	evaluator = Evaluator(statements)

	### print("\nEVALUATOR:")
	evaluator.run()

if __name__ == "__main__":
	if len(sys.argv) > 2:
		e = Error("Too many arguments", None)
		e.call(True)

	if len(sys.argv) == 2:
		codeFile = loadFile(sys.argv[1], True)
		try:
			interpret(list(codeFile.values()))
		except ErrorException:
			sys.exit()

	elif len(sys.argv) == 1:
		editor()