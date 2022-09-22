#stack ops pop two (or one) values, do op and push
#result CONDITIONAL stack ops pop two values,
#compare and push -1 (binary all ones) if compare
#is true or push 0 if false

#asm code for operations on the stack
#that do not involve comparison (no conditionals)
STACK_OPS =\
{'add':
'''
//add
@SP
M=M-1
A=M
D=M
A=A-1
M=D+M

''',

'sub':
'''
//sub
@SP
M=M-1
A=M
D=M
A=A-1
M=M-D

''',

'neg':
'''
//neg
@SP
A=M-1
M=-M

''',

'and':
'''
//and
@SP
M=M-1
A=M
D=M
A=A-1
M=D&M

''',

'or':
'''
//or
@SP
M=M-1
A=M
D=M
A=A-1
M=D|M

''',


'not':
'''
//not
@SP
A=M-1
M=!M

'''

}

#asm code for stack operations that need comparison
#for subsequent if-goto conditional jump.
COND_STACK_OPS=\
{'eq':
'''
//eq
@SP
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
//gt
@SP
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
//lt
@SP
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


