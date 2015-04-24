#!/usr/bin/python
import sys
counter = 0;
st = sys.argv[1]
def SP():
    wf.write("@SP\n")
    wf.write("A=M\n")
    wf.write("M=D\n")
    wf.write("D=A+1\n")
    wf.write("@SP\n")
    wf.write("M=D\n")


def insert(arg, num):

    wf.write("@" + arg)
    wf.write("D=M\n")
    wf.write("A=M\n")
    wf.write("@" + num)
    wf.write("A=A+D\n")
    wf.write("D=M\n")
    SP()


def act(pp,arg,num,func):
    temp = None
    if (arg=="constant"):
        wf.write('@'+num)
        wf.write("D=A\n")
        SP()
    elif (arg=="nothing"):
        if(pp=="push"):
            for i in range(0,int(num)):
                wf.write('@'+num)
                wf.write("D=A\n")
                SP()
        elif(pp=="pop"):
            for i in range(0,int(num)):
                pop(1,"LCL\n",num)
    elif arg in ['local','argument','this','that']:
        if(arg=="local"):
            temp = "LCL\n"
        elif(arg=="argument"):
            temp = "ARG\n"
        elif(arg=="this"):
            temp = "THIS\n"
        elif(arg=="that"):
            temp = "THAT\n"
        if(pp == "push"):
            insert(temp, str(num))
        else:
            pop(1,temp,str(num))
    else:
            if(arg=="pointer"):
                ptr(num,"3")
            elif(arg=="temp"):
                if(int(num)>=8):
                    print("ERROR: push %d is not allowed"%int(num))
                ptr(num,"5")
            elif(arg=="static"):
                func = str(func)+"."+num
                ptr(num,func)
            if(pp == "push"):
                wf.write("A=D\n")
                wf.write("D=M\n")
                SP()
            else:
                pop(2,None,None)

def ptr(arg,st):
    wf.write("@" +st+"\n")
    wf.write("D=A\n")
    wf.write("@" + arg)
    wf.write("D=D+A\n")


def pop(t,arg, num):
    if(t==1):
        wf.write('@'+num)
        wf.write("D=A\n")
        wf.write('@'+arg)
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
    wf.write("@"+c+"%d\n"%counter)
    wf.write("D;J"+c+"\n")
    wf.write("@0\n")
    wf.write("D=A\n")
    wf.write("@SP\n")
    wf.write("A=M\n")
    wf.write("M=D\n")
    wf.write("@END%d\n"%counter)
    wf.write("0;JMP\n")
    wf.write("("+c+"%d)\n"%counter)
    wf.write("@SP\n")
    wf.write("A=M\n")
    wf.write("M=-1\n")
    wf.write("(END%d)\n"%counter)
    wf.write("@SP\n")
    wf.write("M=M+1\n")
    counter=counter+1;
def choose(type):
    if type in ['add', 'sub', 'and','or']:
        b_op(type)
    if type in ['not', 'neg','mult2']:
        u_op(type)
    if type in ['gt','lt','eq']:
        jump(type)

temp = st.split('vm')
wf = open (temp[0]+"asm",'w')
temp = st.split('/')
temp = temp[-1]
temp = temp.split(".")
temp = temp[0]
with open(st,'r') as f:
    for line in f:
        temp1 = line.split('//')
        arr = temp1[0].split(' ')
        if(len(arr)<3):
            choose(arr[0].rstrip())
        elif(len(arr)==3):
            act(arr[0],arr[1],arr[2],temp)
wf.close()
