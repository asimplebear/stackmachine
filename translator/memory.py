from util import clean

#maximum for index on direct adressing push and pop.
SEG_OFFSET_LIMITS = {
'temp': 12-5,
'static': 255 - 16,
'constant': 32767 - 0,
'pointer': 4 - 3
}


OFFSET_ER = '''\
\n\nfrom memory.py:
memory segment {} needs offset between 0 and {}
'''
def segment_offset_limits(trans):
    '''
    decorates push and pop commands to catch
    trying to access outside a segment.
    '''
    def ret(*x):

        _, seg, ind, _, _, _ = x

        if not seg in SEG_OFFSET_LIMITS.keys():
            return trans(*x)

        lim = SEG_OFFSET_LIMITS[seg]
        if 0 <= int(ind) <= lim:
            return trans(*x)
        else:
            msg = OFFSET_ER.format(seg, lim)
            return Exception(msg)

    return ret


#{memory_segment_name: (starting mem addr, A or M)
# A is address and M is memory in that address.
# A accesses address holding pointer to segment.
# M accesses location of begging of segment
SEG_DESC = {

'local':(1, 'M'),
'argument': (2, 'M'),
'this': (3, 'M'),
'that': (4, 'M'),
#'constant': (0, 'A')
'temp': (5, 'A'),
#'static': (16, 'A'),
'pointer': (3, 'A')

}


PUSH_FROM_D = '''
@SP   //push whatever's on D onto stack
A=M
M=D
@SP
M=M+1

'''

def push_indirect(seg, ind):

    seg_num = SEG_DESC[seg][0]
    ret = '''
@{}      //starting mem addr of seg
D=M      //
@{}      //offset
A=A+D
D=M

'''
    ret = ret.format(seg_num, ind)
    ret = ret + PUSH_FROM_D
    return ret


def push_direct(seg, ind):

    seg_num = SEG_DESC[seg][0]
    j = seg_num + int(ind)
    ret = '@{}\nD=M'
    ret = ret.format(j)
    ret = ret + PUSH_FROM_D
    return ret


def push_constant(ind):

    ret = '@{}\nD=A'.format(ind)
    ret = ret + PUSH_FROM_D
    return ret

def push_static(file_name, ind):

    ret = '\n@{}.{}\nD=M'
    ret = ret.format(file_name, ind)
    ret = ret + PUSH_FROM_D
    return ret


@segment_offset_limits
def Push(*vm_line):

    _, seg, ind, _, _, Xxx = vm_line

    if seg in ['local', 'argument', 'this', 'that']:
        ret = push_indirect(seg, ind)
    elif seg in ['temp', 'pointer']:
        ret = push_direct(seg, ind)
    elif 'constant' == seg:
        ret = push_constant(ind)
    elif 'static' == seg:
        ret = push_static(Xxx, ind)
    else:
        input('memory.py Push')
    return ret



#assuming D holds address to pop to
POP_TO_D ='''
@R13     //
M=D        //R13 holds adrress to pop to
@SP
M=M-1
@SP        //stack pointer decremented
A=M
D=M        // D holds the pop payload
@R13
A=M       //looking at target memory
M=D

'''

def pop_indirect(seg, ind):

    seg_num = SEG_DESC[seg][0]
    ret = '''\
@{}
D=M
@{}
D=D+A

'''
    ret = ret.format(seg_num, ind)
    ret = ret + POP_TO_D
    return ret

def pop_direct(seg, ind):

    seg_num = SEG_DESC[seg][0]
    ret = '''@{}
             D=A
             @{}
             D=D+A'''
    ret = ret.format(seg_num, ind)
    ret = ret + POP_TO_D
    return ret


def pop_static(vm_file, ind):
    ret = '''@{}.{}  //vm_file, ind
             D=A
             //@{}   //ind
             //D=D+A'''
    ret = ret.format(vm_file, ind, ind)
    ret = ret + POP_TO_D
    return ret


@segment_offset_limits
def Pop(*vm_line):

    _, seg, ind, _, _, Xxx = vm_line

    if seg in ['local', 'argument', 'this', 'that']:
        ret = pop_indirect(seg, ind)
    if seg in ['temp', 'pointer']:
        ret = pop_direct(seg, ind)
    if 'static' == seg:
        ret = pop_static(Xxx, ind)
    if 'constant' == seg:
        ret = Exception( "can't pop to constant")

    return ret

