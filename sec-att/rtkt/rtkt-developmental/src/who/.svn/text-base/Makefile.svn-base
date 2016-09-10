#
# This is the Makefile for whot.
#
CC=gcc
CFLAGS = -O3

default:
	@$(CC) $(CFLAGS) -DHAVE_LASTLOG_H -DNO_ACCT -o who whot.c
	@strip who
	@echo "whot package built..."
install:
	@mv ./who ../../dst/who
	@echo "whot package installed..."
clean:
	@rm -f who
	@echo "whot package cleaned..."
