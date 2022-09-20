#!/usr/bin/python3

from filehandler import FileHandler
from codewriter import CodeWriter
from asm_hack import assemble_file



for srcs,targ in FileHandler():

    #CodeWriter(srcs,targ)
    c = CodeWriter(srcs, targ)
    c.run()

    assemble_file(targ)




