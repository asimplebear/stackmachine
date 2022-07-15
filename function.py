


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
M=M+1   //push 0s for local variable
'''
FUNCTION = clean(FUNCTION)

def Function(func, nLocs):
    ret = []
    #receive control
    tag = '({})'.format(func)
    ret.append(tag)
    #push 0 for each local var
    for i in range(nLocs):
        for cmd in FUNCTION.split('\n'):
            ret.append(cmd)
    return ret



#{return addr}{nArgs+5}{func}{return addr}
#makes frame stack
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
D=A  //  +5 is for THAT,THIS,ARG,LOCAL and ret addr
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
'''
RETURN = clean(RETURN)

def Return():
    return RETURN.split('\n')

