#ARRAY Format: ["Command","Argument"],
#Help Format: Command [Argument] => Description

#MEM 8-bit-num => Store a number in a variable
#LD mem_location => Load a variable into RAM
#SUB 8-bit-num => Subtract the RAM by a number
#STO mem_location => Store the current RAM values into a variable
#OUT => Output the current Ram
#JZ mem_location => Jump to memory location IF Zero flag is set
#JMP mem_location => Jump to a memory location
#HLT => Halt the main clock (ALWAYS USE AT END OF PROGRAM)
#JC mem_location => Jump to memory location IF carry flag is set 

# Change this variable to a file with the code inside it


FILE_CODE = "./examples/255-0.jas" # Print binary values from 11111111 to 00000000
CODE_LINE_EXEC_TIME = 0.1; # Time for each line of code to run (set to 0 for instant, tho not recommended)

#Do not mess with code below ( Unless you know what you're doing. ) 
import os;
import time;
import platform;

class Halt(Exception): pass

locations = []
ptr = "0x00000000"
mem_load = "00000000"
last_out = "No output";
cptr = 0;
flags = [
    False, # Zero Flag
    False # Carry Flag
]
def parseFile(file):
    fileCode = []
    with open(file,"r") as f:
        for line in f.readlines():
            fSplit = line.split(" ")
            if len(fSplit) == 2:
                fileCode.append([fSplit[0],fSplit[1].replace("\n","")])
            else:
                fileCode.append([fSplit[0].replace("\n",""),""])
    return fileCode
commands = parseFile(FILE_CODE)
def countMem():
    num_mem = 0
    for i in xrange(len(commands)):
        if (commands[i][0] == "MEM"):
            num_mem += 1
    return num_mem
def getdisplay():
    disp = "";
    n = 8
    for i in xrange(len(commands)):
        b = bin(i)[2:]
        l = len(b)
        b = str(0) * (n - l) + b
        cmd = commands[i][0]
        subcmd = commands[i][1]
        disp += "0x"+b+" "+cmd+" "+subcmd+"\n"
        locations.append(["0x"+b,commands[i][0],commands[i][1].replace("0x","")])
    return disp;
def getCmdFromPtr(memloc):
    for i in xrange(len(locations)):
        if (locations[i][0] == memloc):
            return locations[i][1]
    return False
def getValFromPtr(memloc):
    for i in xrange(len(locations)):
        if (locations[i][0] == memloc):
            return locations[i][2]
    return False
def debugger_tick(line):
    disp = getdisplay()
    disp = disp.split('\n');
    if platform.system() == "Linux" or platform.system() == "Darwin":
        os.system("clear");
    else:
        os.system("cls");
    print("==MEMORY==\n")
    n = 8
    for i in range(0,len(commands)):
        if (commands[i][0] == "MEM"):
            b = bin(i)[2:]
            l = len(b)
            b = str(0) * (n - l) + b
            subcmd = commands[i][1]
            print "0x"+b+" "+getValFromPtr("0x"+b)
    print("\n==CODE==\n")
    for i in range(0,len(disp)-1):
        if line == i:
            print(disp[i] + " "*(30-len(disp[i])) + "<=");
        else:
            print(disp[i])
    print("\nOutput: {0}".format(last_out))
def setValFromPtr(memloc,val):
    for i in xrange(len(locations)):
        if (locations[i][0] == memloc):
            locations[i][2] = val
def add(x,y):
        maxlen = max(len(x), len(y))

        #Normalize lengths
        x = x.zfill(maxlen)
        y = y.zfill(maxlen)

        result = ''
        carry = 0

        for i in range(maxlen-1, -1, -1):
            r = carry
            r += 1 if x[i] == '1' else 0
            r += 1 if y[i] == '1' else 0

            # r can be 0,1,2,3 (carry + x[i] + y[i])
            # and among these, for r==1 and r==3 you will have result bit = 1
            # for r==2 and r==3 you will have carry = 1

            result = ('1' if r % 2 == 1 else '0') + result
            carry = 0 if r < 2 else 1       

        if carry !=0 : result = '1' + result

        return result.zfill(maxlen)
def sub(s1, s2):
    b = bin(int(s1, 2) - int(s2, 2))[2:]
    l = len(b)
    b = str(0) * (8 - l) + b
    return b
def getLineFromPtr(ptr):
    n = 8
    for i in range(0,len(commands)):
        b = bin(i)[2:]
        l = len(b)
        b = str(0) * (n - l) + b
        if ("0x"+b) == ptr:
            return i;
def output(msg):
    global last_out;
    last_out = msg;
def runCode(cmd,arg):
    global mem_load
    global ptr
    global cptr
    global flags
    
    if mem_load == "000000b1":
        mem_load = "00000000"
    
    if cmd == "JMP":
        ptr = "0x"+arg
        cptr = getLineFromPtr("0x"+arg)
    elif cmd == "JZ" and mem_load == "00000000":
        ptr = "0x"+arg
        cptr = getLineFromPtr("0x"+arg)
    elif cmd == "LD":
        mem_load = getValFromPtr("0x"+arg)
    elif cmd == "OUT":
        output(mem_load + " | " + str(int(mem_load,2)))
    elif cmd == "STO":
        setValFromPtr(arg,mem_load)
    elif cmd == "ADD":
        mem_load = add(mem_load,arg)
    elif cmd == "SUB":
        mem_load = sub(mem_load,arg)
    elif cmd == "HLT":
        raise Halt
    elif cmd == "JC" and flags[1]:
        ptr = "0x"+arg
        cptr = getLineFromPtr("0x"+arg)
    elif cmd == False:
        raise Halt
    ptr = "0x"+add(ptr.replace("0x",""),"00000001")
    cptr += 1;
    return
print("\nRunning Program...")
try:
    while True:
        debugger_tick(cptr);
        runCode(getCmdFromPtr(ptr),getValFromPtr(ptr))
        time.sleep(CODE_LINE_EXEC_TIME)
except:
    pass;
    
# try:
#     while True:
#         runCode(getCmdFromPtr(ptr),getValFromPtr(ptr))
# except:
#     pass
