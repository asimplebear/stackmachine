import sys
from util import Bootstrap
from parser import Parser
from function import Function, Call, Return
from memory import Push, Pop
from flow import Goto, If_Goto, Label
from arithmetic import Arithmetic

CTYP = {'function': Function,
        'call':     Call,
        'return':   Return,
        'push':     Push,
        'pop':      Pop,
        'goto':     Goto,
        'label':    Label,
        'if-goto':  If_Goto
       }
for op in ['eq', 'gt', 'lt']:
    CTYP[op] = Arithmetic
for op in ['add', 'sub', 'neg', 'and', 'or', 'not']:
    CTYP[op] = Arithmetic


class CodeWriter:
    '''
    srcs = ['/path/to/file.vm, ...]
    targ = '/path/to/dir_to_put_asm_files'
    '''

    def __init__(self, srcs, targ):

        with open(targ, 'w') as wob:
            wob.write(Bootstrap(len(srcs) > 1))
            wob.write('\n')
        self.targ = targ
        self.srcs = srcs
        self.func_name = None
        self.vmfile = None

    def run(self):
        with open(self.targ, 'a') as wob:

            for src in self.srcs:
                if not src.endswith('.vm'): continue

                self.Xxx =\
                     src.split('/')[-1].split('.')[0]

                self.count = 0 #cond op count

                for srcl in Parser(src):

                    line_num, line, args = srcl

                    wob.write('//'+self.Xxx+'.vm line number '+str(line_num)+': \n//'+line)
                    wob.write('\n')

                    if not any(args):
                        continue
                    comm, arg1, arg2 = args

                    if comm == 'function':
                        self.func_name = arg1

                    if comm == 'return':
                        self.func_name = None

                    if comm in ['call','eq','gt','lt']:
                        self.count += 1

                    code = CTYP[comm](comm,
                                      arg1,
                                      arg2,
                                      self.func_name,
                                      self.count,
                                      self.Xxx)

                    if type(code) == Exception:
                        msg = 'Exception occurred atline {}\n{}'.format(line_num, line)
                        sys.tracebacklimit = 0
                        raise Exception(msg) from code
                    wob.write(code)


