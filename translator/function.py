
PUSH_ZERO =\
'''
@SP //push {}-th of {} zeros for local segment in {}
A=M
M=0
@SP
M=M+1
'''
#FUNCTION = clean(FUNCTION)

def Function(*vm_line):


    _, func_name, nLocs, _, _, _ = vm_line

    ret = []
    #receive control
    tag = '({})\n'.format(func_name)
    ret.append(tag)
    #push 0 for each local var
    for i in range(int(nLocs)):
        ret.append(PUSH_ZERO.format(i+1, nLocs, func_name))
    return ''.join(ret) + '\n'



#{return addr}{nArgs+5}{func}{return addr}
#makes frame stack
CALL =\
'''
@{}          //return address (bottom this string)
D=A          // store it
@SP
A=M
M=D
@SP
M=M+1
@LCL         //save LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG         //save ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS        //save THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT        //save THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP          //set new LCL
D=M
@LCL
M=D
@{}          //set new ARG (nArgs+5)
D=A   // +5 is for THAT,THIS,ARG,LOCAL and ret addr
@SP
D=M-D
@ARG
M=D
@{}         //pass control to func.
0;JMP
//wait here for function to return
({})  //pick up control after return

'''

#CALL = clean(CALL)

def Call(*vm_line):

    _, func_name, nArgs, _, count, _ = vm_line

    tag = '{}$ret.{}'.format(func_name, count)
    ret = CALL.format(tag, int(nArgs)+5, func_name, tag)

    return ret


RETURN =\
'''
@LCL     //return
D=M
@R15
M=D       //  R15 = LCL
@5
D=A
@R15
A=M-D
D=M
@R13
M=D       // R13  = *(R15 - 5) (return addr into R13)
@SP
A=M-1
D=M
@ARG
A=M
M=D // *ARG = pop()  (place return value for caller)
@ARG
D=M
@SP
M=D+1 //SP = ARG + 1(put stack pointer back for caller)
//         THAT = *(FRAME-1) (FRAME is funcs LCL)
@R15       //walking back R15 thru THIS, THAT etc
AM=M-1     //decr and also look there
D=M
@THAT
M=D        //THAT is restored
//       restore THIS
@R15
AM=M-1
D=M
@THIS
M=D
//      restore ARG
@R15
AM=M-1
D=M
@ARG
M=D
//      restore LCL
@R15
AM=M-1
D=M
@LCL
M=D
//     return to ret addr held in R13
@R13
A=M
0;JMP
//end asm for return
'''

def Return(*vm_line):

    return RETURN

