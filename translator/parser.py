
def Parser(infile):
    '''
    argument is path/to/<file.vm> absolute OR relative
    return is list of these:
    [
     source_code_line_number,
     source_code_line,
     arg0,     like 'pop' or 'return' or 'eq' etc
     arg1,     like <function name> or <segment> etc
     arg2      like nArgs or <index> etc
    ]
     if arg2 and/or arg3 nonextant then list is padded
     with None.
    '''

    with open(infile) as rob:
        sls = rob.readlines() #source lines

    #[ [com, arg1, arg2], ... ]
    scs = [line.split('//')[0].strip() for line in sls]
    # i+1 is line number in source code
    scs = [(i+1, l) for (i,l) in enumerate(scs)]
    # filter out any blank lines
    scs = [(i,l) for (i,l) in scs if l]
    # put source line number and line (text)
    # [..[src_line_number, src_line, com, arg1, arg2]..]
    scs = [[i] + [sls[i-1]] +  l.split()\
                 for (i,l) in scs]

    #pad each with Nones beacause some commands
    #lack arg2 and or arg1
    for c in scs:
        while len(c) < 5:
            c.append(None)

    return scs
