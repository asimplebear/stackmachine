


def clean(template):
    '''
    converts readable/editable string with
    comments to whitespace/newlines-free
    uncommented strings.
    '''

    lines = template.split('\n')
    lines = [x.split('//')[0].strip() for x in lines]
    lines = [x for x in lines if x]
    ret = '\n'.join(lines)
    return ret




FUNCTION = '''
@SP
A=M
M=0
@SP
M=M+1
'''
FUNCTION = clean(FUNCTION)

def Function(func, nLocs):
    ret = []

    tag = '({})'.format(func)
    ret.append(tag)


    for i in range(nLocs):
        for cmd in FUNCTION.split('\n'):
            ret.append(cmd)
    return ret




#first {}-format is callee's ARG
#second {}-format is from FUNC_ADDRS
#and gives line where execution starts.
#{{}}-format is for the return address
#gotten by len of asm code so far plus
#len of this code
CALL =\
'''
@{}   //return address (bottom this string)
D=A          // store it
@SP
A=M
M=D
@SP
M=M+1

@LCL//save LCL
D=M
@SP
A=M
M=D
@SP
M=M+1





@ARG//save ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS//save THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT//save THAT
D=M
@SP
A=M
M=D
@SP
M=M+1

@SP//set new LCL
D=M
@LCL
M=D

@{}//set new ARG (nArgs+5)
D=A
@SP
D=M-D
@ARG
M=D

@{}//pass control to func.
0;JMP

//wait here for function to return

({})  //pick up control after return



'''

CALL = clean(CALL)

def Call(func, nArgs, count):

    tag = '{}$ret.{}'.format(func,count)
    ret = CALL.format(tag, int(nArgs)+5, func, tag)
    return ret.split('\n')







RETURN =\
'''
//        R15 = LCL
@LCL
D=M
@R15
M=D

//        R13  = *(R15 - 5) (return addr into R13)
@5
D=A
@R15
A=M-D
D=M
@R13
M=D

//        *ARG = pop()  (place return value for caller)
@SP
A=M-1
D=M
@ARG

A=M ////////









M=D

//   SP = ARG + 1  (put stack pointer back for caller)

@ARG
D=M
@SP
M=D+1

//                 THAT = *(FRAME-1)
@R15
AM=M-1
D=M
@THAT
M=D
//       replace THIS
@R15
AM=M-1
D=M
@THIS
M=D
//      replace ARG
@R15
AM=M-1
D=M
@ARG
M=D
//      replace LCL






@R15
AM=M-1
D=M
@LCL
M=D


//     return to ret addr held in R13
@R13
A=M
0;JMP
'''
RETURN = clean(RETURN)

def Return():
    return RETURN.split('\n')
