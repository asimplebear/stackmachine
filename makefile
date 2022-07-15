all:
	./VMT.py singletons/rec_fac.vm
	./VMT.py programs/primes
	./VMT.py programs/static_test
	./VMT.py programs/fib

clean:
	rm -f *.asm
	rm -f *.hack
