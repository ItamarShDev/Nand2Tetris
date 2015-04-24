#!/usr/bin/python
import sys
import xml.etree.ElementTree as tree
import Stack


def _write(type,name):
	wf.write('<'+type+'> ')
	wf.write(name)
	wf.write(' </'+type+'> \n')

def token(type,word):
	if(type==1):
		wf.write('<'+word+'>\n')
	elif (type==2):
		wf.write('</'+word+'>\n')

def keyword():
	name = tokens.pop()
	_write("keyword",name)

def symbol():
	t = tokens.pop()
	_write("symbol",t)

def identifier():
	_write("identifier", tokens.pop())

def subroutineCall(type = 0, val = None):
	token(1, "subroutineCall")
	if(type==0):
		temp1 = tokens.pop()
	else:
		temp1 = val
	
	temp2 = tokens.peek()
	if(temp2 != '('):
		_write("identifier", temp1)
		tokens.pop()
		_write("symbol",'.')
		temp1 = tokens.pop()
	token(1, "subroutineName")
	_write("identifier",temp1)
	token(2, "subroutineName")
	symbol()
	expressionList()	
	symbol()
	token(2, "subroutineCall")

def colon(type):
	if (type ==1):
		t = tokens.pop()
		while (t!=';'):
			_write("symbol", t)
			_write("identifier", tokens.pop())
			t = tokens.pop()
		_write("symbol", t)
	elif (type ==2):
		t = tokens.peek()
		while(t!=')'):
			if (t==','):
				symbol()
			_type()
			_write("identifier", tokens.pop())
			t = tokens.peek()
	elif (type==3):
		t = tokens.peek()
		while(t!=')'):
			if (t==','):
				symbol()
				_write("identifier", tokens.pop())

def ret():
	token(1,"returnStatement")
	keyword()#return
	t = tokens.peek()
	if (t!=';'):
		expression()#if its not void
	symbol()#semicolon
	token(2,"returnStatement")

def _while():
	token(1,"whileStatement")
	keyword()#while
	symbol()#'('
	expression()#the term
	symbol()#')'
	symbol()#'{'
	statments()#the code
	symbol()#'}'
	token(2,"whileStatement")

def do():
	token(1,"doStatement")
	keyword()#do
	subroutineCall()#What to do
	symbol()#semicolon
	token(2,"doStatement")

def let():
	token(1,"letStatement")
	keyword()#let
	identifier()#varName
	t = tokens.peek()
	if (t=='['):
		symbol()#'['
		expression()
		symbol()#']'
	symbol()#'='
	expression()
	symbol()#semicolon
	token(2,"letStatement")

def _if():
	token(1,"ifStatement")
	keyword()#if
	symbol()#'('
	expression()
	symbol()#')'
	symbol()#'{'
	statments()
	symbol()#'}'
	t = tokens.peek()
	if (t=='else'):
		keyword()#else
		symbol()#'{'
		statments()
		symbol()#'}'
	token(2,"ifStatement")

def statments():
	token(1,"statements")
	t = tokens.peek() 
	while(t in ['let','if','while','do','return']):	
		token(1,"statement")
		if (t=='let'):
			let()
		elif (t=='if'):
			_if()
		elif (t== 'while'):
			_while()
		elif (t=='do'):
			do()
		elif (t=='return'):
			ret()
		token(2,"statement")
		t = tokens.peek() 
	token(2,"statements")

def term():
	token(1,"term")
	t = tokens.peek()
	if (t=='('):
		symbol()
		expression()
		symbol()
	elif t in sc:
		_write("stringConstant", tokens.pop())
	elif t in ic:
		_write("integerConstant", tokens.pop())
	elif t in uop:
		token(1,"unaryOp")
		symbol()
		token(2, "unaryOp")
		term()

	elif t in kwc:
		token(1,"keywordConstant")
		_write("keyword", tokens.pop())
		token(2,"keywordConstant")
	else:
		t = tokens.pop()
		t2 = tokens.peek()
		if (t2 == '['):
			_write("identifier", t)
			symbol()#'['
			expression()
			symbol()#']'
		elif (t2 == "(" or t2 == '.'):
			subroutineCall(1, t)
		else: 
			_write("identifier", t)
	token(2,"term")

def expressionList():
	token(1, "expressionList")
	t = tokens.peek()
	if(t !=')'):
		expression()
	t = tokens.peek()
	while (t!=')'):
		symbol()
		expression()
		t = tokens.peek()
				# if t2 in symb:
		# 	symbol()
		# t = tokens.peek()
	token(2, "expressionList")

def expression():
	token(1,"expression")
	term()
	t = tokens.peek()
	if t in op:
		token(1,"op")
		if t == ">":
			_write("symbol"," &gt; ")
			tokens.pop()
		elif t == "<":
			_write("symbol", " &lt; ")
			tokens.pop()
		elif t == "&":	
			_write("symbol", " &amp; ")
			tokens.pop()
		else:
			symbol()#binary operator
		token(2, 'op')
		term()
	token(2,"expression")

def classVarDec():
	token(1,"classVarDec")
	keyword()#static or field must be present 
	_type()#var type
	identifier()#name
	colon(1)#case there is more
	# symbol()#semicolon
	token(2,"classVarDec")

def _type():
	t = tokens.peek()
	if (t=='void'):
		return
	token(1,"type")
	t = tokens.peek()
	if t in ['int', 'char','boolean']:
		_write("keyword",t)
	else:
		_write("identifier", t)
	tokens.pop()
	token(2,"type")
def subroutinName():
	token(1, "subroutineName")
	_write("identifier", tokens.pop())
	token(2,"subroutineName")

def subroutineDec():
	token(1,"subroutineDec")
	_write("keyword",tokens.pop())
	t = tokens.peek()
	_type()
	if (t == 'void'):
		_write("keyword",tokens.pop())
	subroutinName()
	symbol()#'('
	parameterList()
	symbol()#')'
	subroutinBody()
	token(2,"subroutineDec")

def parameterList():
	token(1,"parameterList")
	# _type()#type
	# identifier()#name
	t = tokens.peek()
	while(t!=')'):
		if (t==','):
			symbol()
		_type()
		_write("identifier", tokens.pop())
		t = tokens.peek()
	token(2,"parameterList")

def varDec():
	token(1,"varDec")
	_write("keyword", tokens.pop()) #var
	_type()#type
	identifier()#name
	colon(1)#if theres more
	token(2,"varDec")

def subroutinBody():
	token(1,"subroutineBody")
	symbol()#'{'
	t = tokens.peek()
	while (t=='var'):
		varDec()
		t = tokens.peek()
	statments()#'}'
	symbol()
	token(2,"subroutineBody")

def Class():
	token(1,"class")#open class token
	keyword()#class must be
	identifier()#name of class
	symbol()#'{'
	t = tokens.peek()
	while t in var_types:
		classVarDec()#check for vars
		t = tokens.peek()
	while t in func_types:
		subroutineDec()#check for methods
		t = tokens.peek()
	symbol()
	token(2,"class")#close class token
func_types = ['constructor','function','method']
var_types = ['field', 'static']
types= ['int', 'char','boolean']
symb = ['{','}','(',')','[',']','.',',',';','+','-','*','/','&','|','>','<','=','~']
op = ['+','-','*','/','&','>','<','=','^']
uop = ['-','~']
kwc = ['true', 'false', 'this', 'null']
sc = []
ic = []

st = str(sys.argv[1])#get the name

x = tree.parse(st)
root = x.getroot()

temp = st.split('T.xml')
wf = open(temp[0]+".xml", 'w')

tokens = Stack.Stack()

#insert all to the stack
for child in root:
	tokens.push(child.text.strip())

#search for all stringConstant
for i in root.findall("stringConstant"):
	sc.append(i.text.strip())

#search for all integerConstant
for i in root.findall("integerConstant"):
	ic.append(i.text.strip())

#need to reverse 
tokens.items.reverse()
first_word = tokens.peek()
if(first_word=="class"):
	Class()
else:
	print ("this file has no class")
