



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





#second pass (handle_labels) fills in {}
GOTO =\
'''

@{}
0;JMP
'''
GOTO = clean(GOTO)

def Goto(func, label):

    label = '{}${}'.format(func, label)
    return GOTO.format(label).split('\n')

#JNE happens iff top of stack has other than zero
IF_GOTO =\
'''
@SP
AM=M-1
D=M
@{}
D;JNE
'''
IF_GOTO = clean(IF_GOTO)

def If_Goto(func, label):

    label = '{}${}'.format(func, label)
    return IF_GOTO.format(label).split('\n')


LABEL = '''({})'''
def Label(func, label):

    label = '{}${}'.format(func, label)

    return [LABEL.format(label)]



