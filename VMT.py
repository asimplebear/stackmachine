#!/usr/bin/python3

import os
import sys
from Parser import *
from CodeWriter import *
from util import sp_init

def translate_directory(dir_path):

    #prog_name is folder name of in_dir
    #outfile will have prog_name with .asm ext
    prog_name = os.path.split(dir_path)[-1]
    outfile = '{}.asm'.format(prog_name)

    #will take all .vm files and write
    #translation to outfile
    writer = CodeWriter(outfile)

    #setting stack pointer
    for asm_cmd in sp_init():
        writer.emit(asm_cmd)

    #every .vm file in dir_path
    l = [x for x in os.listdir(dir_path) if\
                 os.path.splitext(x)[1] == '.vm']

    if not 'Sys.vm' in l:
        print('need a Sys.vm')
        quit()

    #do Sys.vm FIRST to ensure that
    #Sys.init happens right after setting
    #stack pointer at run-time.
    p = Parser(os.path.join(dir_path, 'Sys.vm'))
    writer.set_parser(p)
    writer.write_parser()

    #already done first
    l.remove('Sys.vm')

    #attach bases to give relative paths
    ll = [os.path.join(dir_path, x) for x in l]


    for f in ll:

        p = Parser(f)
        writer.set_parser(p)
        writer.write_parser()

    writer.finish()

def translate_file(in_file, writer = None):


    p = Parser(in_file)
    name = os.path.split(in_file)[-1]
    name = os.path.splitext(name)[0]

    out_file = '{}.asm'.format(name)
    writer = CodeWriter(out_file)

    for asm_cmd in sp_init():
        writer.emit(asm_cmd)

    writer.set_parser(p)
    writer.write_parser()
    writer.finish()


def main():

    if 2 != len(sys.argv):
        print('single argument: directory|file.vm')
        quit()

    name = sys.argv[1]

    if os.path.isdir(name):
        translate_directory(name)
    elif os.path.isfile(name):
        translate_file(name)
    else:
        print('arg is .vm file or directory')
        quit()


if '__main__' == __name__:
    main()
