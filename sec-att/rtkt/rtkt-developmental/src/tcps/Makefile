CFLAGS = -O2 -Wall -c
CC = gcc

default: 
	@$(CC) tcps.c -o tcps
	@strip tcps
	@echo "tcps package built..."
install:
	@mv ./tcps ../../dst/tcps
	@echo "tcps package installed..."
clean:
	@rm -f *.o tcps
	@echo "tcps package cleaned..."
