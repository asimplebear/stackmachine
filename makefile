all:
	translator/translator.py -m programs TARG

clean:
	rm -rf TARG
	rm -f *.asm
	rm -f *.hack
