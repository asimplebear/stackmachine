
def translation_failure(trans):
    '''
    decorator to catch translation failures.
    Modifies line by line translators.  Prevents
    error of this program and instead shows user
    where it happened in the VM source code.
    '''
    def ret(*args):
        try:
            return trans(*args)
        except:
            print('line num {}'.format(error_line_num))
            print(error_line)
            quit()
    return ret


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


SET_SP = '''//set stack pointer MEM[0] = 256
@256
D=A
@SP
M=D
'''
ENTRY_POINT = '''
//program entry point
@Sys.init
0;JMP
'''

#BOOTSTRAP = clean(BOOTSTRAP)

def Bootstrap(multiple_files):
    if multiple_files:
        return SET_SP + ENTRY_POINT
    else:
        return SET_SP








