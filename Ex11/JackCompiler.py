#!/usr/bin/python
import sys
import xml.etree.ElementTree as tree
import Stack
import os





def keyword():
	global statics
	global fields
	global f_fields
	global f_statics
	o_type = None
	name = tokens.pop()
	if(name=="field"):
		o_type = _type()
		name = tokens.pop()
		f_fields.update({name: fields})
		if(o_type!=None):
			obj.update({name : o_type})
		fields+=1
		t = tokens.peek()
		if(t==';'):
			tokens.pop()
		while(t==','):
			tokens.pop()
			name =tokens.pop()
			f_fields.update({name:fields})
			t = tokens.peek()
			fields+=1
			if(t==';'):
				tokens.pop()
				break
	elif(name== "static"):
		o_type = _type()
		name = tokens.pop()
		f_statics.update({name: statics})
		if(o_type!=None):
			obj.update({name : o_type})
		statics+=1
		t = tokens.peek()
		if(t==';'):
			tokens.pop()
		while(t==','):
			tokens.pop()
			name =tokens.pop()
			f_statics.update({name:statics})
			t = tokens.peek()
			statics+=1
			if(t==';'):
				tokens.pop()
				break
	if(o_type!=None):
		obj.update({name : o_type})

def symbol():
	tokens.pop()

def subroutineCall(type = 0, val = None):
	global vars
	global f_name
	global c_name
	num = 0
	name = c_name
	if(type==0):
		f_name = tokens.pop()
	if(type!=0):
		f_name = val
	temp2 = tokens.pop()
	if(temp2 == '.'):
		if (type!=0):
			name = val
		elif (type==0):
			name = f_name
		f_name = tokens.pop()
		tokens.pop()

	if(temp2 != '.'):
		if f_name in methods:
			wf.write("push pointer 0\n")
			num+=1

	try:
		_obj = obj[name]
		v_name = name
		name = _obj
		num+=1
		try:
			t = f_arg[v_name]
			wf.write("push argument "+str(t)+"\n")
		except:
			try:
				t = f_fields[v_name]
				wf.write("push this "+str(t)+"\n")
			except:
				try:
					t = f_statics[v_name]
					wf.write("push static "+str(t)+"\n")
				except:
					t = vars[v_name]
					wf.write("push local "+str(t)+"\n")
	except:
		None
	temp_name = f_name
	num+= expressionList()
	wf.write("call "+name+"."+temp_name+" "+str(num)+"\n")
	tokens.pop()	

def ret():
	tokens.pop()
	t = tokens.peek()
	if (t!=';'):
		expression()#if its not void
	else:
		wf.write("push constant 0\n") 
	symbol()#semicolon
	wf.write("return\n")

def _while(count):
	tokens.pop()
	symbol()#'('
	wf.write("label WHILE_EXP%d\n" % count)	
	expression()#the term
	wf.write("not\n")
	symbol()#')'
	symbol()#'{'
	wf.write("if-goto WHILE_END%d\n" %count)

	statments(w_count=count+1)#the code
	wf.write("goto WHILE_EXP%d\n" %count)
	wf.write("label WHILE_END%d\n" %count)	
	symbol()#'}'

def do():
	tokens.pop()
	subroutineCall()#What to do
	wf.write("pop temp 0\n")
	symbol()#semicolon

def let():
	global f_arg

	flag = True
	tokens.pop()
	name = tokens.pop()
	t = tokens.peek()
	if (t=='['):
		symbol()#'['
		expression()
		if name in f_fields:
			t = f_fields[name]
			wf.write("push this %s\n"  % str(t))
		else:
			try:
				t = vars[name]
				wf.write("push local %s\n" % str(t))
			except:
				try:
					n = f_statics[name]
					wf.write("push static %s\n" %str(n))
				except:	
					try:
						n = f_arg[name]
						wf.write("push argument %s\n" %str(n))
					except:
						None
		symbol()#']'
		wf.write("add\n")
		flag = False

	symbol()#'='
	expression()

	if not flag:
		wf.write("pop temp 0\n")
		wf.write("pop pointer 1\n")
		wf.write("push temp 0\n")
		wf.write("pop that 0\n")

	if flag:
		if name in f_fields:
			t = f_fields[name]
			wf.write("pop this "+str(t)+"\n")
		else:
			try:
				t = vars[name]
				wf.write("pop local "+str(t)+"\n")
			except:
				try:
					t = f_statics[name]
					wf.write("pop static "+str(t)+"\n" )
				except:	
					try:
						t = f_arg[name]
						wf.write("pop argument "+str(t)+"\n")
					except:
						None
	symbol()#semicolon

def _if(counter):
	global max_if
	l_count = counter
	max_if+=1
	symbol()
	symbol()#'('
	expression()
	symbol()#')'
	symbol()#'{'
	wf.write("if-goto IF_TRUE%s\n"% str(l_count))
	wf.write("goto IF_FALSE%s\n"% str(l_count))
	wf.write("label IF_TRUE%s\n"% str(l_count))
	if (max_if <= l_count):
		statments(if_count = l_count)
	else:		
		statments(if_count = max_if)
	symbol()#'}'
	t = tokens.peek()
	if (t=='else'):
		t= tokens.pop()
		symbol()#'{'
		wf.write("goto IF_END%d\n"%l_count )
		wf.write("label IF_FALSE%d\n"%l_count)
		if max_if > l_count:
			statments(if_count = max_if)
		else:		
			statments(if_count = l_count)
		wf.write("label IF_END%d\n"%l_count)
		tokens.pop()
	else:	
		wf.write("label IF_FALSE%d\n"%l_count)

def statments(w_count = 0, if_count = 0):
	t = tokens.peek()
	while(t in ['let','if','while','do','return']):	
		if (t=='let'):
			let()
		elif (t=='if'):
			if(if_count>max_if):
				_if(if_count)
			else:
				_if(max_if)
			if_count+=1
		elif (t== 'while'):
			_while(w_count)
			w_count+=1
		elif (t=='do'):
			do()
		elif (t=='return'):
			ret()
		t = tokens.peek() 

def term():
	global f_arg
	t = tokens.peek()
	if (t=='('):
		symbol()
		expression()
		symbol()
	elif t in sc:
		wf.write("push constant %d\n" % len(t))
		wf.write("call String.new 1\n")	
		for i in t:
			wf.write("push constant %d\n" %ord(i))
			wf.write("call String.appendChar 2\n")	

		tokens.pop()		
	elif t in ic:
		wf.write("push constant %s\n" %tokens.pop())	
	elif t in uop:
		temp = tokens.pop()
		term()
		if temp == '~':
			wf.write("not\n")
		elif temp == '-':
			wf.write("neg\n")

	elif t in kwc:
		key = tokens.pop()
		if key == 'this':
			wf.write("push pointer 0\n")
		elif key == 'true':
			wf.write("push constant 0\n")
			wf.write("not\n")
		else:
			wf.write("push constant 0\n") #Null

	else:
		t = tokens.pop()

		t2 = tokens.peek()
		if (t2 == '['):
			symbol()#'['
			expression()
			if t in f_fields:
				wf.write("push this %s\n" %f_fields[t])
			else:
				try:
					t = vars[t]
					wf.write("push local %s\n" %str(t))
				except:
					try:
						wf.write("push static %s\n" %f_statics[t])
					except:	
						None	
			tokens.pop() #pop ]
			wf.write("add\n")
			wf.write("pop pointer 1\n")
			wf.write("push that 0\n")

		elif (t2 == "(" or t2 == '.'):
				subroutineCall(1, t)
		else: 
			try:
				temp = f_arg[t]
				wf.write("push argument %s\n" % str(temp))
			except:
				try:
					temp = vars[t]
					wf.write("push local %s\n" % str(temp))
				except:
					try:
						temp = f_fields[t]
						wf.write("push this %s\n" % str(temp))
					except:
						try:
							temp = f_statics[t]
							wf.write("push static %s\n" % str(temp))
						except:
							None	
	return

def expressionList():
	counter =0
	t = tokens.peek()
	if(t !=')'):
		expression()
		counter +=1
		t = tokens.peek()
	while (t!=')'):
		tokens.pop()
		expression()
		t = tokens.peek()
		counter +=1
	return counter

def expression():
	term()
	t = tokens.peek()
	while t in op:
		_op = tokens.pop()
		term()
		if t == ">":
			wf.write("gt\n")
		elif t == "<":
			wf.write("lt\n")
		elif t == "&":	
			wf.write("and\n")

		else:
			if _op == '+':
				wf.write("add\n")
			elif _op == "-":
				wf.write("sub\n")
			elif _op == "*":
				wf.write("call Math.multiply 2\n")
			elif _op == "/":
				wf.write("call Math.divide 2\n")
			elif _op == "|":
				wf.write("or\n")
			elif _op == "^":
				wf.write("call Math.pow 2\n")
			elif _op == "=":
				wf.write("eq\n") 		

		t = tokens.peek()	

def classVarDec():
		keyword()#static or field must be kept

def _type():
	t = tokens.peek()
	if (t=='void'):
		return
	o_type = None
	if t in ['int', 'char','boolean']:
		tokens.pop()
	else:
		o_type = tokens.pop()
	return o_type


def subroutinName():
	global f_name
	f_name = tokens.pop()

def subroutineDec():
	global f_type
	global f_name
	f_type = tokens.pop()
	tokens.pop()
	f_name = tokens.pop()
	symbol()
	parameterList()
	symbol()#')'
	subroutinBody()

def parameterList():
	global f_arg
	f_arg = {}
	arg_count = 0
	t = tokens.peek()
	while(t!=')'):
		if (t==','):
			symbol()
		tokens.pop()
		f_arg.update({tokens.pop() : arg_count})
		arg_count+=1
		t = tokens.peek()

def varDec():
	global obj
	global vars
	global var_count
	tokens.pop() #pop 'var'
	type = _type()#type
	name = tokens.pop()
	t = tokens.peek()
	if(t==';'):
		if (type !=None):
			obj.update({name : type })
 
		vars.update({name :var_count })
		t= tokens.pop()
		var_count+=1


	while (t==','):
		if (type !=None):
			obj.update({name : type })
		vars.update({name :var_count })
		var_count+=1
		t= tokens.pop()
		if (t==';'):
			break
		name = tokens.pop()


def subroutinBody():
	global c_name
	global f_name
	global vars
	global f_type
	global var_count
	global max_if
	max_if=0
	var_count = 0
	symbol()#'{'
	t = tokens.peek()
	vars = {}
	while (t=='var'):
		varDec()
		t = tokens.peek()
	t = tokens.peek()

	wf.write("function %s.%s %d\n" %(c_name, f_name, len(vars)))

	if (f_type=="constructor"):
		wf.write("push constant " + str(len(f_fields))+"\n") 
		wf.write("call Memory.alloc 1\n")
		wf.write("pop pointer 0\n")
	if (f_type == "method"):
		wf.write("push argument 0\n")
		wf.write("pop pointer 0\n")
		for i in f_arg.items():
			f_arg[i[0]] = i[1] + 1

	statments()
	symbol()

def Class():
	global c_name
	global f_arg
	tokens.pop()
	c_name = tokens.pop()
	symbol()#'{'
	t = tokens.peek()
	while t in var_types:
		classVarDec()#check for vars
		t = tokens.peek()
	t= tokens.peek()
	while t in func_types:
		subroutineDec()#check for methods
		t = tokens.peek()
	symbol()


func_types = ['constructor','function','method']
var_types = ['field', 'static']
types= ['int', 'char','boolean']
symb = ['{','}','(',')','[',']','.',',',';','+','-','*','/','&','|','>','<','=','~']
op = ['+','-','*','/','&','>','<','=','^', '|']
uop = ['-','~']
kwc = ['true', 'false', 'this', 'null']

st = str(sys.argv[1])#get the name
for file in os.listdir(st):
	if file.endswith('T.xml'):
		x = tree.parse(st+file)
		root = x.getroot()
		filen = str(file)
		temp = filen.split('T.xml')
		wf = open(st+temp[0]+".vm", 'w')
		tokens = Stack.Stack()
		tokens1 = Stack.Stack()
		fields = 0
		var_count = 0
		statics = 0
		max_if =0
		sc = []
		ic = []
		f_statics = {}
		f_fields = {}
		f_arg = {}
		vars = {}
		methods = []
		functions = {}
		c_name = ""
		f_type = ""
		f_name = ""
		obj = {} 
		
		#insert all to the stack
		for child in root:
			tokens1.push(child.text.strip())
			temp = child.text[1:-1]
			tokens.push(temp)
			#search for all stringConstant
		for i in root.findall("stringConstant"):
			temp = i.text[1:-1]
			sc.append(temp)

			#search for all integerConstant
		for i in root.findall("integerConstant"):
			ic.append(i.text.strip())
			#need to reverse 
		tokens.items.reverse()
		tokens1.items.reverse()
		temp = tokens1.pop()
		while (1):
			if (temp == "method"):
				tokens1.pop()
				methods.append(tokens1.pop())
			try:
				temp = tokens1.pop()
			except:
				break
		first_word = tokens.peek()
		if(first_word=="class"):
			Class()
		else:
			print ("this file has no class")
