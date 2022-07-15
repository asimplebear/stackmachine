#!/usr/bin/python3

from function import Function, Return, Call
from memory import Push, Pop
from flow import Goto, If_Goto, Label
from arithmetic import Arithmetic
from util import Bootstrap

class CodeWriter:

    def __init__(self, outfile):

        #self.file = None
        self.func = None
        self.count = 0
        self.fob = open(outfile, 'w')



    def set_parser(self, parser):
        self.parser = parser
        #for writing unique tags
        #self.file = parser.get_file()

    def emit(self, st):
        #print(st)
        self.fob.write(st)
        self.fob.write('\n')


    def write_parser(self):


        while self.parser.hasMoreCommands():

            cmd_type, arg1, arg2 = self.parser.advance()

            #if 'C_PUSH' == self.parser.get_type():
            if 'C_PUSH' == cmd_type:

                seg, ind = arg1, arg2
                #need self.file for static segment tags
                fi = self.func.split('.')[0]
                asm_cmds = Push(fi, seg, ind)

            elif 'C_POP' == cmd_type:

                seg, ind = arg1, arg2
                #need self.file for static segment tags
                fi = self.func.split('.')[0]
                asm_cmds = Pop(fi, seg, ind)


            elif 'C_GOTO' == cmd_type:

                label = arg1
                asm_cmds = Goto(self.func, label)


            elif 'C_IF' == cmd_type:

                label = arg1
                asm_cmds = If_Goto(self.func, label)

            elif 'C_LABEL' == cmd_type:

                label = arg1
                asm_cmds = Label(self.func, label)


            elif 'C_CALL' == cmd_type:

                func, nArgs = arg1, arg2
                index = self.parser.get_index()
                asm_cmds = Call(func, nArgs, self.count)
                self.count += 1

            elif 'C_FUNCTION' == cmd_type:

                func, nLocs = arg1, arg2
                self.func = func  #for unique tags
                asm_cmds = Function(func, nLocs)


            elif 'C_RETURN' == cmd_type:

                self.func = None #no more tags needed
                asm_cmds = Return()

            elif 'C_ARITHMETIC' == cmd_type:
                op = arg1
                ind = self.parser.get_index()
                asm_cmds = Arithmetic(op, self.count)
                self.count += 1

            else:
                print('fix Parser, should not happen')
                quit()

            if type(asm_cmds) == str:
                self.finish()
                e = asm_cmds.format(*self.parser.get_e_line())
                raise ValueError(e)

            for asm_cmd in asm_cmds:

                self.emit(asm_cmd)

    def finish(self):
        self.fob.close()

