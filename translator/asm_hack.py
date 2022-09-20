#!/usr/bin/python3

import sys
import os




LABELS = {
          "R0":     "0000000000000000",
          "R1":     "0000000000000001",
          "R2":     "0000000000000010",
          "R3":     "0000000000000011",
          "R4":     "0000000000000100",
          "R5":     "0000000000000101",
          "R6":     "0000000000000110",
          "R7":     "0000000000000111",
          "R8":     "0000000000001000",
          "R9":     "0000000000001001",
          "R10":    "0000000000001010",
          "R11":    "0000000000001011",
          "R12":    "0000000000001100",
          "R13":    "0000000000001101",
          "R14":    "0000000000001110",
          "R15":    "0000000000001111",
          "SP":     "0000000000000000",
          "ARG":    "0000000000000010",
          "LCL":    "0000000000000001",
          "THIS":   "0000000000000011",
          "THAT":   "0000000000000100",
          "KBD":    "0110000000000000",
          "SCREEN": "0100000000000000"
         }




COMPS = {
         "0":   "0101010",
         "1":   "0111111",
         "-1":  "0111010",
         "D":   "0001100",
         "A":   "0110000",
         "!D":  "0001101",
         "!A":  "0110001",
         "-D":  "0001111",
         "-A":  "0110011",
         "D+1": "0011111",
         "A+1": "0110111",
         "D-1": "0001110",
         "A-1": "0110010",
         "D+A": "0000010",
         'A+D': '0000010',
         "D-A": "0010011",
         "A-D": "0000111",
         "D&A": "0000000",
         "D|A": "0010101",
         "M":   "1110000",
         "!M":  "1110001",
         "-M":  "1110011",
         "M+1": "1110111",
         "M-1": "1110010",
         "D+M": "1000010",
         "D-M": "1010011",
         "M-D": "1000111",
         "D&M": "1000000",
         "D|M": "1010101"
        }



DESTS = {
         "":    "000",
         "M":   "001",
         "D":   "010",
         "MD":  "011",
         "A":   "100",
         "AM":  "101",
         "AD":  "110",
         "AMD": "111"
        }


JMPS = {
        "":    "000",
        "JGT": "001",
        "JEQ": "010",
        "JGE": "011",
        "JLT": "100",
        "JNE": "101",
        "JLE": "110",
        "JMP": "111"
       }





def two_bytes(n):
    '''
    turn dec to binary and pad to 16 bits
    '''
    t = bin(n)[2:]
    return '0'*(16-len(t)) + t

def clean_lines(lines):
    '''
    get rid of comments and spaces and empty lines
    '''
    ret = [line.split('//')[0].strip() for line in lines]
    ret = [x for x in ret if x]

    return ret


def translateAcommand(line):
    '''
    @<val>    where val is numbeer or label
    '''
    val = line[1:]
    assert line[0] == '@'
    if val.isdecimal():
        ret = two_bytes(int(val))
    else:
        ret = LABELS[val]

    assert '0' == ret[0]

    return ret


def translateCcommand(line):
    '''
    <dest>=<comp>;<jmp>
    '''
    dest,comp,jmp = '','',''
    if not ';' in line:
        dest, comp = line.split('=')
    elif not '=' in line:
        comp, jmp = line.split(';')
    else:
        dest, this = line.split('=')
        comp, jmp = this.split(';')
    ret = '111{}{}{}'.format(COMPS[comp],\
                             DESTS[dest],\
                             JMPS[jmp])

    return ret


def translate_line(x):

    #A-instruction
    if x.startswith('@'):
        return translateAcommand(x)
    #C-instruction  dest=comp;jump
    if '=' in x or ';' in x:
        return translateCcommand(x)


def tag_line(line):
    '''
    if is a tagline return label, else False
    '''
    a, b, c = line[0], line[1:-1], line[-1]
    if a == '(' and c == ')':
        return b
    else:
        return False


def resolve_tags(lines):
    '''
    strip out all tag lines and resolve
    the labels to machine code line numbers
    '''
    ret = []
    #resolve all tags to line number that
    #follows.  get rid of line tag was on.
    for line in lines:
        t = tag_line(line)
        if t:
            #len(ret) is next line number
            #do not append current line
            LABELS[t] = two_bytes(len(ret))
        else:
            #not a tagline
            ret.append(line)

    return ret


def new_vars(l):
    '''
    collect all labels introduced
    by A-commands in source
    '''
    #mem0 - mem15 are default labeled
    cnt = 16
    for i in l:
        #if A-command and has NEW non-numerical
        #name then declare it starting AFTER R15
        if i.startswith('@') and\
                        not i[1:] in LABELS.keys() and\
                        not i[1:].isdecimal():
            LABELS[i[1:]] = two_bytes(cnt)
            cnt = cnt + 1


def assemble_commands(lines):
    '''
    assemble list of asm commands to
    list of binary strings
    '''
    #strip comments and blank lines
    ret = clean_lines(lines)
    #strip taglines and resolve to line numbers
    ret = resolve_tags(ret)
    #collect vars defined by A-commands
    new_vars(ret)
    #transcribe asm to machine
    ret = [translate_line(line) for line in ret]

    return ret



def assemble_file(asm_file):
    '''
    given path/to/file.asm create path/to/file.hack
    '''

    name, ext = os.path.splitext(asm_file)
    assert '.asm' == ext

    hack_file = '{}.hack'.format(name)

    with open(asm_file) as fob:
        asm_lines = fob.readlines()

    mach_lines = assemble_commands(asm_lines)

    mach_text = '\n'.join(mach_lines) + '\n'

    with open(hack_file, 'w') as fob:
        fob.write(mach_text)

    #print('{} ==> {}'.format(asm_file, hack_file))


def assemble_directory(asm_dir):
    '''
    assemble every .asm file in asm_dir
    '''
    os.chdir(asm_dir)
    asm_files = [x for x in os.listdir()\
                   if '.asm' == os.path.splitext(x)[-1]]

    for asm_file in asm_files:
        assemble_file(asm_file)


def main():


    if len(sys.argv) != 2:
        raise Exception('usage: ./Assember <file> | <directory> ')

    arg = sys.argv[1]

    if os.path.isdir(arg):

        assemble_directory(arg)

    elif '.asm' == os.path.splitext(arg)[1]:

        assemble_file(arg)

    else:
        print('{} is not good file name'.format(arg))


if __name__ == '__main__':

    main()




