#stack ops pop two (or one) values, do op and push
#result CONDITIONAL stack ops pop two values,
#compare and push -1 (binary all ones) if compare
#is true or push 0 if false

#asm code for operations on the stack
#that do not involve comparison (no conditionals)
STACK_OPS =\
{'add':
'''
@SP //add
M=M-1
A=M
D=M
A=A-1
M=D+M

''',

'sub':
'''
@SP //sub
M=M-1
A=M
D=M
A=A-1
M=M-D

''',

'neg':
'''
@SP //neg
A=M-1
M=-M

''',

'and':
'''
@SP //and
M=M-1
A=M
D=M
A=A-1
M=D&M

''',

'or':
'''
@SP //or
M=M-1
A=M
D=M
A=A-1
M=D|M

''',


'not':
'''
@SP //not
A=M-1
M=!M

'''

}

#asm code for stack operations that need comparison
#for subsequent if-goto conditional jump.
COND_STACK_OPS=\
{'eq':
'''
@SP //eq
M=M-1
A=M
D=M
A=A-1
M=M-D
D=M
M=-1
@{}
D;JEQ
@SP
A=M-1
M=0
({})

''',



'gt':
'''
@SP //gt
M=M-1
A=M
D=M
A=A-1
M=M-D
D=M
M=0
@{}
D;JLE
@SP
A=M-1
M=-1
({})

''',


'lt':
'''
@SP //lt
M=M-1
A=M
D=M
A=A-1
M=M-D
D=M
M=0
@{}
D;JGE
@SP
A=M-1
M=-1
({})

'''

}


STACK_OPS.update(COND_STACK_OPS)

def Arithmetic(*vm_line):


    op, _, _, _, count, Xxx = vm_line

    lab = '{}$COND.{}'.format(Xxx, count)

    return STACK_OPS[op].format(lab, lab)


