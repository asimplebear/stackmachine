

#second pass (handle_labels) fills in {}
GOTO = '''\
@{} //goto
0;JMP

'''

def Goto(*vm_line):

    _, label, _, func_name, _, _ = vm_line

    tag = '{}${}'.format(func_name, label)
    return GOTO.format(tag)

#JNE happens iff top of stack has other than zero
IF_GOTO = '''\
@SP //if-goto
AM=M-1
D=M
@{}
D;JNE

'''

def If_Goto(*vm_line):

    _, label, _, func_name, _, _ = vm_line

    tag = '{}${}'.format(func_name, label)
    return IF_GOTO.format(tag)


LABEL = '''({})\n'''
def Label(*vm_line):

    _, label, _, func_name, _,  _ = vm_line

    tag = '{}${}'.format(func_name, label)

    return LABEL.format(tag)



