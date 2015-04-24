// File name: Sort.asm
// Sorts R0 ..... R15 in descending order (4,51,6,12 ===>  51,12,6,4)
// (R0, R1, R2.... refer to RAM[0], RAM[1], and RAM[2]...., respectively.)

//BUUBLE SORT (complex-n^2)
@15
D=A
@times //counter
M=D

(SORT)
	@stop //is sort done?
	M=0
	//set vars
	@15
	D=A
	@count //inner loop counter
	M=D

	@R0//first intteration
	D=A
	@first
	M=D
	@R1//second intteration
	D=A
	@second
	M=D
	//done setting start

(INNERLOOP)
	//do first-second
	//if its GREATER than 0 SWAP  
	@second
	A=M
	D=M
	@first
	A=M
	D=D-M

	@SWAP
	D;JGT

	//first++
	@first
	M=M+1
	//second++
	@second
	M=M+1
	//count--
	@count
	M=M-1
	//if count==0 stop looping
	D=M
	@INNERLOOP
	D;JGT
	//check if all sorted
	@stop
	D=M
	@END
	D;JEQ
	//times--
	@times
	M=M-1
	D=M
	@SORT
	D;JGT

(SWAP)
	//X=a
	@first
	A=M
	D=M

	//Y=a+b
	@second
	A=M
	D=D+M

	//X=Y-a=b
	@first
	A=M
	M=D-M

	//Y=Y-b=a
	@second
	A=M
	M=D-M

	@stop
	M=1

	@INNERLOOP
	0;JMP

	(END)
		@END
		0;JMP
