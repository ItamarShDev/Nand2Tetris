// File name: Quarter.asm

// You should split the Screen to four quarters(left/right and up/down) in the following manner: 
//In an  infinite loop: while no key is pressed,the top left and bottom right are black, 
//and top right and bottom left are white. While any key is pressed, the colors are switched. 

//set color
//@color
//M=-1
//detect key press
//@runs
//M=1
//@select
//M=0
(PRESSED)
	@runnum
	M=1
	@runs
	M=1
	@KBD
	D=M
	@PAINT
	D;JEQ
	@ONE
	D;JNE

(PAINT)
	@select
	M=0
	@runs
	D=M
	@CLR
	D;JEQ
	@PRESSED
	D;JLT
	@color
	M=-1
	@SCREEN
	D=A
	@print
	M=D
	@INIT
	0;JMP
(CLR)
	@runnum
	M=1
	@select
	M=1
	@color
	M=0
	@SCREEN
	D=A
	@print
	M=D
	@16
	D=A
	@print
	M=M+D
	@INIT
	0;JMP

(ONE)
	@runs
	D=M
	@CLR2
	D;JEQ
	@PRESSED
	D;JLT
	@color
	M=-1
	@SCREEN
	D=A
	@print
	M=D
	@16
	D=A
	@print
	M=M+D
	@INIT
	0;JMP
(CLR2)
	@runnum
	M=1
	@color
	M=0
	@SCREEN
	D=A
	@print
	M=D
	@INIT
	0;JMP




(INIT)
	//height
	@128
	D=A
	@height
	M=D

	//width
	@16
	D=A
	@width
	M=D
(P)
	@color
	D=M
	@print
	A=M
	M=D
	@print
	M=M+1
	@width
	M=M-1
	@width
	D=M
	@P
	D;JGT

	@16
	D=A
	@print
	M=M+D
	@width
	M=D
	
	@height
	M=M-1
	@height
	D=M
	@P
	D;JGT
	@16
	D=A
	@print
	M=M-D
	@width
	M=D
	@runnum
	M=M-1
	D=M
	@INIT
	D;JEQ
	@runs
	M=M-1
	@select
	D=M
	@PAINT
	D;JEQ
	@ONE
	D;JNE