desc = '''
Translates .vm stackmachine files to .asm
assembly programs (and assembles down to
.hack programs)

<source> is path (abs or rel) to source
files/directories and <target> is path
to drop the .asm and .hack files. If no
target is given it defaults to current.

(see options --multiple
for usage example)
'''

multiple = '''
Without the --multiple (or -m)
flaga single program (.asm file)
is created from either a single
.vm fileor a directory containing
multiple .vm files (including Sys.vm)

With the -m flag multiple .asm files
are created from a directory containing
single .vm files and/or directories of
.vm files.

So in the following situation:
.
│ 
│ 
├── programs
│   ├── prog1
│   │   ├── Main.vm
│   │   └── Sys.vm
│   ├── prog2.vm
│   └── prog3
│       ├── Bar.vm
│       ├── Foo.vm
│       └── Sys.vm
├── prog4
│   ├── Bar.vm
│   ├── Foo.vm
│   └── Sys.vm
└── prog5.vm

running translator.py prog4
and     translator.py prog5.vm
creates prog4.asm, prog4.hack,
and prog5.asm, prog5.hack

and running translator.py -m programs
creates prog{i}.asm and prog{i}.hack
for i = 1,2,3
'''

err = '''
Exception occured at line {}:\n{}
'''



