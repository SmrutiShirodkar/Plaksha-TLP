	.data
base:	.word 	1
binary: .word	0
fo:	.word	0

	LW:r1, fo(r0)
	ADDI:r2,r0,75
	MOVI2FP:f1,r2
	LW:r3, binary(r0)
	LW:r4, base(r0)
	MOVI2FP:f2,r4
	MOVI2FP:f5,r3
while:	AND:f3,f1,#1
	MULTF:f4,f3,f2
	ADDF:f5,f5,f4
	DIVF:f1,f1,#2
	MULTF:f2,f2,#10
	BNEZ:f2, count
	BNEZ:f1, while

count:	ADDI:r1,r1,#1
	J:while

	SW:3000(r0),r1
	trap 0
