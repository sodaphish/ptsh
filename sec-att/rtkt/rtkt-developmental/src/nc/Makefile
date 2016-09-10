CFLAGS = -O2 -Wall -c
CC = gcc

default: 
	@$(CC) netcat.c -o nc
	@strip nc
	@echo "nc package built..."
install:
	@mv ./nc ../../dst/nc
	@echo "nc package installed..."
clean:
	@rm -f *.o nc
	@echo "nc package cleaned..."
