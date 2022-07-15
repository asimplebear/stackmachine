from arithmetic import abs_ops, cond_ops
import os

class Parser:

    def __init__(self, file_path):

        with open(file_path) as rob:
            self.lines = rob.readlines()

        self.clines = [x.split('//')[0].strip()\
                                 for x in self.lines]
        self.clines = enumerate(self.clines)
        self.comms = [x for x in self.clines if x[1]]
        self.max_comm = len(self.comms)
        self.comm_num = -1
        self.comm = None
        self.line_num = 0

        self.index = 0

        #self.file = 'fIlE'
        self.func = None
        self.ret_ind = 0
        self.type = None
        self.arg1 = None
        self.arg2 = None


        file_name = os.path.basename(file_path)
        self.file = os.path.splitext(file_name)[0]

    #called once by codewriter
    #for use in writing tags

    def get_file(self):
        return self.file

    def hasMoreCommands(self):
        return self.comm_num + 1 < self.max_comm

    def get_type(self):
        return self.typ

    def get_arg1(self):
        return self.arg1

    def get_arg2(self):
        return self.arg2






    def get_comm(self):
        return self.comm

    def get_e_line(self):
        return self.line_num, self.lines[self.line_num]

    def get_index(self):
        return self.index

    def get_func(self):
        return self.func

    def advance(self):
        self.comm_num += 1
        self.comm = self.comms[self.comm_num][1]
        self.line_num = self.comms[self.comm_num][0]


        if self.comm.startswith('function'):
            _, func, nLocs = self.comm.split(' ')

            self.func = func###############

            nLocs = int(nLocs)
            self.typ = 'C_FUNCTION'
            self.arg1 = func
            self.arg2 = nLocs


        elif self.comm.startswith('return'):
            self.typ = 'C_RETURN'
            self.arg1 = None
            self.arg2 = None

            self.func = None ##################


        elif self.comm.startswith('call'):
            _, func, nArgs = self.comm.split(' ')
            self.index += 1
            nArgs = int(nArgs)
            self.typ = 'C_CALL'
            self.arg1 = func
            self.arg2 = nArgs

        elif self.comm in abs_ops:
            self.typ = 'C_ARITHMETIC'
            self.arg1 = self.comm
            self.arg2 = None


        elif self.comm in cond_ops:
            self.typ = 'C_ARITHMETIC'
            self.arg1 = self.comm
            self.arg2 = None
            self.index += 1



        elif self.comm.startswith('goto'):
            _, label = self.comm.split(' ')
            self.typ = 'C_GOTO'
            self.arg1 = label
            self.arg2 = None

        elif self.comm.startswith('if-goto'):
            _, label = self.comm.split(' ')
            self.typ = 'C_IF'
            self.arg1 = label
            self.arg2 = label

        elif self.comm.startswith('label'):
            _, label = self.comm.split(' ')
            self.typ = 'C_LABEL'
            self.arg1 = label
            self.arg2 = None

        elif self.comm.startswith('push'):
            _, seg, ind = self.comm.split(' ')
            self.typ = 'C_PUSH'
            ind = int(ind)
            self.arg1 = seg
            self.arg2 = ind

        elif self.comm.startswith('pop'):
            _, seg, ind = self.comm.split(' ')
            self.typ = 'C_POP'
            ind = int(ind)
            self.arg1 = seg
            self.arg2 = ind

        else:
            e = '\nline {}:\n{}Not a vm command.'\
                    .format(*self.get_e_line())
            raise ValueError(e)


        return self.typ, self.arg1, self.arg2
