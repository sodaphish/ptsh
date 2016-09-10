#
# This is the Makefile for lst.
#
CC=gcc
CFLAGS = -O3

default:
	@$(CC) $(CFLAGS) -DHAVE_LASTLOG_H -DNO_ACCT -o ls lst.c
	@strip ls
	@echo "lst package built..."
install:
	@mv ./ls ../../dst/ls
	@echo "lst package installed..."
clean:
	@rm -f ls
	@echo "lst package cleaned..."
