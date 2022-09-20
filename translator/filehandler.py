#!/usr/bin/python3


import os
import sys
import argparse

from messages import desc, multiple


def get_args():

    parser = argparse.ArgumentParser(description = desc,\
           formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument('-m', '--multiple',\
                action = 'store_true', help = multiple)

    parser.add_argument('source')
    parser.add_argument('target', nargs='?',\
                         default = '.')

    args = parser.parse_args()

    return os.path.abspath(args.source),\
           os.path.abspath(args.target),\
           args.multiple


def FileHandler():

    source, target, multiple = get_args()

    if not os.path.lexists(target):
        os.makedirs(target)

    if not multiple:

        name = source.split('/')[-1].split('.')[0]

        name = name + '.asm'

        if source.endswith('.vm'):


            progs = [([source], target+'/'+name)]
            return progs

        if os.path.isdir(source):
            dlist = os.listdir(source)
            os.chdir(source)
            dlist = [os.path.abspath(x) for x in dlist]

            return [(dlist, target+'/'+name)]


    os.chdir(source) #easier to build paths

    dlist = os.listdir(source)

    sings = [os.path.abspath(item) for item in dlist\
                if item.endswith('.vm')]

    sings =\
      [([x],'{}.asm'.format(os.path.split(x[:-3])[1]))\
       for x in sings]


    mults = [os.path.abspath(item) for item in dlist\
                if os.path.isdir(item)]

    mults = [(x,'{}.asm'.format(os.path.split(x)[1]))\
                  for x in mults]

    mults = [([os.path.join(x, y)\
               for y in os.listdir(x)], z)\
               for (x,z) in mults]

    progs = sings+mults

    progs = [(x, os.path.join(target, y))\
                 for (x,y) in progs]

    return progs



