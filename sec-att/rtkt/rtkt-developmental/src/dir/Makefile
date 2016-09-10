#
# This is the Makefile for dirt.
#
CC=gcc
CFLAGS = -O3

default:
	@$(CC) $(CFLAGS) -DHAVE_LASTLOG_H -DNO_ACCT -o dir dirt.c
	@strip dir
	@echo "dirt package built..."
install:
	@mv ./dir ../../dst/dir
	@echo "dirt package installed..."
clean:
	@rm -f dir
	@echo "dirt package cleaned..."
