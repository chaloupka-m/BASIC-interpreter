#Error
#Při inicializaci objektu se uchovává chybová zpráva a číslo řádku, na kterém je chyba

import sys

class ErrorException(Exception):
	pass

class Error:
	def __init__(self, message, line):
		self.message = message
		self.line = line

	#Při volání funkce call() se na konzoli objeví chybová hláška a program se ukončí
	def call(self, exit = False):
		if self.line != None:
			print(f"Error: {self.message} on line {self.line}")
		else:
			print(f"Error: {self.message}")
		
		if exit:
			sys.exit()
			
		raise ErrorException()