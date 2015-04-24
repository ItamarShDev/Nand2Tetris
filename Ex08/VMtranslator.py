#!/usr/bin/python
from __future__ import print_function
import sys
import os
import platform
import string
counter = 0;
st = sys.argv[1]
wf = None
def SP():
    global wf
    wf.write("@SP\n")
    wf.write("A=M\n")
    wf.write("M=D\n")
    wf.write("D=A+1\n")
    wf.write("@SP\n")
    wf.write("M=D\n")


def insert(arg, num):
    global wf
    wf.write("@%s\n"%arg)
    wf.write("D=M\n")
    wf.write("A=M\n")
    wf.write("@%s\n"%num)
    wf.write("A=A+D\n")
    wf.write("D=M\n")
    SP()


def act(pp,arg,num,label):
    global filen
    global wf
    temp = None
    if(pp=="call"):
        call(arg,num, label)
    elif(pp=="function"):
        func(arg,num)
    elif (arg=="constant"):
        wf.write("@"+str(num)+"\n")
        wf.write("D=A\n")
        SP()
    elif arg in ['local','argument','this','that']:
        if(arg=="local"):
            temp = "LCL"
        elif(arg=="argument"):
            temp = "ARG"
        elif(arg=="this"):
            temp = "THIS"
        elif(arg=="that"):
            temp = "THAT"
        elif (arg=="nothing"):
            for i in range(0,num):
                insert("argument","1")
        if(pp == "push"):
            insert(temp, str(num))
        elif(pp=="pop"):
            pop(1,temp,str(num))
    else:
            if(arg=="pointer"):
                ptr(str(num),"3")
            elif(arg=="temp"):
                if(int(num)>=8):
                    print("ERROR: push %d is not allowed\n"%num)
                    exit(1)
                ptr(str(num),"5")
            elif(arg=="static"):
                # label = str(label)+"."+num
                # ptr(str(num),label)
                wf.write("@"+str(filen)+'.'+str(num)+"\n")
                wf.write("D=A\n")
            if(pp == "push"):
                wf.write("A=D\n")
                wf.write("D=M\n")
                SP()
            else:
                pop(2,None,None)

def ptr(arg,st):
    global wf
    wf.write("@"+str(st)+"\n")
    wf.write("D=A\n")
    wf.write("@" + arg+"\n")
    wf.write("D=D+A\n")


def pop(t,arg, num):
    global wf
    if(t==1):
        wf.write('@'+str(num)+"\n")
        wf.write("D=A\n")
        wf.write('@'+str(arg)+"\n")
        wf.write("A=M\n")
        wf.write("D=A+D\n")
    wf.write("@R13\n")
    wf.write("M=D\n")
    wf.write("@SP\n")
    wf.write("A=M-1\n")
    wf.write("D=M\n")
    wf.write("@R13\n")
    wf.write("A=M\n")
    wf.write("M=D\n")
    wf.write("@SP\n")
    wf.write("M=M-1\n")


def b_op(type):
    global wf
    wf.write("@SP\n")
    wf.write("M=M-1\n")
    wf.write("A=M\n")
    wf.write("D=M\n")
    wf.write("A=A-1\n")
    if (type == "or"):
        wf.write("D=M|D\n")
    elif(type=="and"):
        wf.write("D=M&D\n")
    elif(type=="add"):
        wf.write("D=M+D\n")
    elif(type=="sub"):
        wf.write("D=M-D\n")
    wf.write("M=D\n")
    wf.write("D=A+1\n")
    wf.write("@SP\n")
    wf.write("M=D\n")

def u_op(type):
    global wf
    wf.write("@SP\n")
    wf.write("M =M-1\n")
    wf.write("A=M\n")
    if(type=="not"):
        wf.write("M=!M\n")
    elif(type=="neg"):
        wf.write("M=-M\n")
    elif (type=="mult2"):
        wf.write("D=M\n")
        wf.write("M=D+M\n")
    wf.write("D=A+1\n")
    wf.write("@SP\n")
    wf.write("M=D\n")


def jump(c):
    global counter
    global wf
    c= c.upper()
    c.rstrip()
    wf.write("@SP\n")
    wf.write("M=M-1\n")
    wf.write("A=M\n")
    wf.write("D=M\n")
    wf.write("@SP\n")
    wf.write("M=M-1\n")
    wf.write("A=M\n")
    wf.write("D=M-D\n")
    wf.write("@"+c+str(counter)+"\n")
    wf.write("D;J"+c+"\n")
    wf.write("@0\n")
    wf.write("D=A\n")
    wf.write("@SP\n")
    wf.write("A=M\n")
    wf.write("M=D\n")
    wf.write("@END"+str(counter)+"\n")
    wf.write("0;JMP\n")
    wf.write("("+c+str(counter)+")\n")
    wf.write("@SP\n")
    wf.write("A=M\n")
    wf.write("M=-1\n")
    wf.write("(END"+str(counter)+")\n")
    wf.write("@SP\n")
    wf.write("M=M+1\n")
    counter=counter+1;

def choose(type,arg):
    global wf
    if type in ['add', 'sub', 'and','or']:
        b_op(type)
    elif type in ['not', 'neg', 'mult2']:
        u_op(type)
    elif type in ['gt','lt','eq']:
        jump(type)
    elif(type=="label"):
        label(arg)
    elif type in ['if-goto','goto']:
        _if(type,arg)
    elif (type =="return"):
        ret()

def label(arg):
    global wf
    arg= arg.upper()
    if(func_name==""):
        wf.write("(%s)\n"%arg)
    else:
        wf.write("("+func_name+"$"+arg+")\n" )

def _if(type, arg):
    global wf
    global func_name
    arg=arg.upper()
    func_name= func_name.upper()
    if(type=="if-goto"):
        wf.write("@SP\n")
        wf.write("M=M-1\n")
        wf.write("A=M\n")
        wf.write("D=M\n")
    if(func_name==""):
        wf.write("@%s\n"%arg)
    else:
        wf.write("@"+func_name+"$"+arg+"\n" )
    if(type=="if-goto"):
        wf.write("D;JNE\n")
    elif(type=="goto"):
        wf.write("0;JMP\n")

def func(arg,num):
    global wf
    wf.write("(%s)\n"%arg)
    for i in range(0,int(num)):
        act("push","constant","0", None)

def ret():
    global wf
    # // Save LCL in temp var R13
    wf.write("@LCL\n");
    wf.write("D=M\n");
    wf.write("@R13\n");
    wf.write("M=D\n");
    # // Put the return address *(R13-5) in temp var RET
    wf.write("@5\n");
    wf.write("A=D-A\n");
    wf.write("D=M\n");
    wf.write("@R14\n");
    wf.write("M=D\n");
    # // *ARG = pop()
    wf.write("@SP\n");
    wf.write("M=M-1\n");
    wf.write("A=M\n");
    wf.write("D=M\n")
    wf.write("@ARG\n");
    wf.write("A=M\n");
    wf.write("M=D\n");
    # // SP = ARG + 1
    wf.write("@ARG\n");
    wf.write("D=M\n");
    wf.write("@SP\n");
    wf.write("M=D+1\n");
    # // THAT = *(R13-1)
    wf.write("@R13\n");
    wf.write("A=M-1\n");
    wf.write("D=M\n");
    wf.write("@THAT\n");
    wf.write("M=D\n");
    # // THIS = *(R13-2)
    wf.write("@R13\n");
    wf.write("A=M-1\n");
    wf.write("A=A-1\n");
    wf.write("D=M\n");
    wf.write("@THIS\n");
    wf.write("M=D\n");
    # // ARG = *(R13-3)
    wf.write("@R13\n");
    wf.write("A=M-1\n");
    wf.write("A=A-1\n");
    wf.write("A=A-1\n");
    wf.write("D=M\n");
    wf.write("@ARG\n");
    wf.write("M=D\n");
    # // LCL = *(R13-4)
    wf.write("@R13\n");
    wf.write("A=M-1\n");
    wf.write("A=A-1\n");
    wf.write("A=A-1\n");
    wf.write("A=A-1\n");
    wf.write("D=M\n");
    wf.write("@LCL\n");
    wf.write("M=D\n");
    # // goto R14
    wf.write("@R14\n");
    wf.write("A=M\n");
    wf.write("0;JMP\n");

def call(arg,num,label):
    global counter
    global wf
    # push return-address
    label = "RETURN_ADDRESS_"+ arg + "_" + str(counter)
    wf.write("@" + label+"\n");
    wf.write("D=A\n");
    push();
    # push LCL
    wf.write("@LCL\n");
    wf.write("A=M\n");
    wf.write("D=A\n");
    push();
    # push ARG
    wf.write("@ARG\n");
    wf.write("A=M\n");
    wf.write("D=A\n");
    push();
    # push THIS
    wf.write("@THIS\n");
    wf.write("A=M\n");
    wf.write("D=A\n");
    push();
    # push THAT
    wf.write("@THAT\n");
    wf.write("A=M\n");
    wf.write("D=A\n");
    push();
    # ARG = SP-n-5
    wf.write("@SP\n");
    wf.write("A=M\n");
    for i in  range(0,int(num) + 5):
        wf.write("A=A-1\n");
    wf.write("D=A\n");
    wf.write("@ARG\n");
    wf.write("M=D\n");
    # LCL=SP
    wf.write("@SP\n");
    # wf.write("A=M\n");
    wf.write("D=M\n");
    wf.write("@LCL\n");
    wf.write("M=D\n");
    # goto f
    wf.write("@" + arg + "\n");
    wf.write("0;JMP\n");
    # create label to return to
    wf.write("(" + label + ")\n");
    counter=counter+1;

def push():
    global wf
    wf.write("@SP\n");
    wf.write("A=M\n");
    wf.write("M=D\n");
    wf.write("@SP\n");
    wf.write("M=M+1\n");

def arrange(name):
    global st
    global wf
    global flag
    # temp = st.split('/')
    # temp = temp[-1]
    temp = name.split(".")
    temp = temp[0]
    temp1 = name.split("//")
    temp1[0] =temp1[0].rstrip().strip()
    arr = temp1[0].split(" ")
    if(len(arr)<2):
        choose(arr[0].rstrip(),None)
    elif(len(arr)==2):
        choose(arr[0].rstrip(),arr[1].rstrip())
    elif(len(arr)==3):
        act(arr[0],arr[1],arr[2],temp)

#check the platform
func_name = ""
if (platform.system() == "Linux"):
    fold = "/"
else:
    fold = "\\"
if (st[-1]==fold):
    st = st[:-1]
try:
    flag = sys.argv[2]
except:
    flag = 0

temp = st.split('vm')
wf = open (temp[0]+".asm",'w')
if not flag:
    wf.write("@256\n")
    wf.write("D=A\n")
    wf.write("@SP\n")
    wf.write("M=D\n")
    act("call", "Sys.init", "0", None)
for file in os.listdir(st):
    if file.endswith(".vm"):
        with open(st+fold+file) as f:
            for line in f.readlines():
                # print(line)
                filen = str(file)
                val = arrange(line)

wf.close()

