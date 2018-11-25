# JackAssembly

Change the variable FILE_CODE to a file that contains the "Jack Assembly" code inside of it.

COMMANDS: 

-MEM 8-bit-num => Store a number in a variable
-LD mem_location => Load a variable into RAM
-SUB 8-bit-num => Subtract the RAM by a number
-STO mem_location => Store the current RAM values into a variable
-OUT => Output the current Ram
-JZ mem_location => Jump to memory location IF Zero flag is set
-JMP mem_location => Jump to a memory location
-HLT => Halt the main clock (ALWAYS USE AT END OF PROGRAM)
-JC mem_location => Jump to memory location IF carry flag is set 
