#Error
#Spouští se při chybném uživatelském vstupu

import sys

class ErrorException(Exception):
	pass

class Error:
	#Při inicializaci objektu se uchovává chybová hláška a číslo řádku, na kterém je chyba
	def __init__(self, message, line):
		self.message = message
		self.line = line

	#Vypíše chybovou hlášku a program ukončí
	def call(self, exit = False):
		if self.line != None:
			print(f"Error: {self.message} on line {self.line}")
		else:
			print(f"Error: {self.message}")
		
		if exit:
			sys.exit() #Kompletní ukončení - při spouštění zdrojového kódu ze souboru
			
		raise ErrorException() #Návrat na textové rozhraní