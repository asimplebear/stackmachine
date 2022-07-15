from util import clean



#asm code for operations on the stack
#that do not involve comparison (no conditionals)
ABS_STACK_OPS =\
{'add':
'''
@SP
M=M-1
A=M
D=M
A=A-1
M=D+M''',

'sub':
'''@SP
M=M-1
A=M
D=M
A=A-1
M=M-D''',

'neg':
'''@SP
A=M-1
M=-M''',

'and':
'''@SP
M=M-1
A=M
D=M
A=A-1
M=D&M''',

'or':
'''@SP
M=M-1
A=M
D=M
A=A-1
M=D|M''',


'not':
'''@SP
A=M-1
M=!M'''

}


ABS_STACK_OPS = {op: clean(ABS_STACK_OPS[op])\
                      for op in ABS_STACK_OPS.keys() }
abs_ops = ABS_STACK_OPS.keys()

def Abs_Stack_Ops(operation):
    return ABS_STACK_OPS[operation].split('\n')





#asm code for stack operations that need comparison
#and subsequent conditional jump.  The label tag to
#be possibly jumped to is at end of code, so caller
#can use its current line number for to jump.
COND_STACK_OPS=\
{'eq':
'''

@SP
M=M-1
A=M
D=M
A=A-1
M=M-D
D=M
M=-1
@COND{}
D;JEQ
@SP
A=M-1
M=0
(COND{})
''',



'gt':
'''@SP
M=M-1
A=M
D=M
A=A-1
M=M-D
D=M
M=0
@COND{}
D;JLE
@SP
A=M-1
M=-1
(COND{})''',


'lt':
'''@SP
M=M-1
A=M
D=M
A=A-1
M=M-D //sub
D=M
M=0
@COND{}
D;JGE
@SP
A=M-1
M=-1
(COND{})'''

}

COND_STACK_OPS = {op: clean(COND_STACK_OPS[op])\
                  for op in COND_STACK_OPS.keys()}
cond_ops = COND_STACK_OPS.keys()

def Cond_Stack_Ops(operation, count):
    return COND_STACK_OPS[operation].format(count,count).split('\n')

def Arithmetic(op, count):

    if op in abs_ops:
        ret = ABS_STACK_OPS[op]
        return ret.split('\n')

    if op in cond_ops:
        ret = COND_STACK_OPS[op].format(count, count)
        return ret.split('\n')



