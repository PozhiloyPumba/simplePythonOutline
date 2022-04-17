from Python3Lexer import Python3Lexer
from Python3Parser import Python3Parser
from Python3Visitor import Python3Visitor
from antlr4 import *
import sys
import sqlite3


class MyVisitor(Python3Visitor):
    def __init__ (self, filename, connection, cursor) :
        self.filename_ = filename
        self.connect_ = connection
        self.cursor_ = cursor

    def visitFuncdef(self, ctx:Python3Parser.FuncdefContext):   # funcdef
        args = ctx.parameters()

        argNames = 'does not have arguments'
        if args.getChildCount() != 2:
            argNames = ''
            for arg in args.typedargslist().tfpdef():
                argNames += str(arg.NAME ()) + ' '
            argNames = argNames[:-1]
        
        note = '\'' + self.filename_ + "\', \'Function\', \'" + str(ctx.NAME ()) + '\', \'' + (argNames) + '\', ' + str(int (ctx.start.line)) + ', ' + str(ctx.stop.line)    

        request = 'INSERT INTO GlobalObjects VALUES (' +  note + ')'
        self.cursor_.execute(request)
 
        self.connect_.commit()

    def visitClassdef(self, ctx:Python3Parser.ClassdefContext):     # class definition
        note = '\'' + self.filename_ + "\', \'Class\', \'" + str(ctx.NAME ()) + '\', \'\', ' + str(int (ctx.start.line)) + ', ' + str(ctx.stop.line)    
        request = 'INSERT INTO GlobalObjects VALUES (' +  note + ')'
        self.cursor_.execute(request)
 
        self.connect_.commit()

#----------------------------------------------------------------------------

conn = sqlite3.connect("funcAndClass.db")

cursor = conn.cursor ()
cursor.execute("CREATE TABLE GlobalObjects (filename TEXT, type TEXT, name TEXT, args TEXT, beginDef INTEGER, endDef INTEGER)")
conn.commit()

if __name__ == "__main__":
    for inputFile in sys.argv[1:]:
        data = FileStream(inputFile)
        
        lexer = Python3Lexer(data)
        stream = CommonTokenStream(lexer)

        parser = Python3Parser(stream)
        
        tree = parser.file_input()

        visitor = MyVisitor(inputFile, conn, cursor)
        visitor.visit(tree)