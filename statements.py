#Příkazy
#Instance tříd lonelyStatement, simpleStatement a ifStatement jsou uzly AST nebo jejich kořeny seřazenými do pole AST
#Funkce log() vrací textový řetězec s vizuální strukturou uzlu -> určený pro výstup na konzoli při testování

#CLS, END, RETURN, REM
class lonelyStatement:
    def __init__(self, command, line):
        self.command = command
        self.line = line

    def log(self):
        return f"Statement({self.command})"

#GOTO, PAUSE, GOSUB, ARRAY, NEXT, PRINT, INPUT, LET, FOR
class simpleStatement:
    def __init__(self, command, line, arguments):
        self.command = command
        self.line = line
        self.arguments = arguments
    
    def log(self):
        if(isinstance(self.arguments, list)):
            logs = []
            for a in self.arguments:
                logs.append(a.log())
            return f"Statement({self.command}, {', '.join(logs)})"
        return f"Statement({self.command}, {self.arguments.log()})"

#IF
class ifStatement:
    def __init__(self, line, conditions, statements):
        self.line = line
        self.conditions = conditions
        self.statements = statements

    def log(self):
        cLogs = []
        sLogs = []
        for c in self.conditions:
            cLogs.append(c.log())
        for s in self.statements:
            sLogs.append(s.log())
        return f"Statement(IF, [{', '.join(cLogs)}], [{', '.join(sLogs)}])"