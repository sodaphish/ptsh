#
# This is the Makefile for pst.
#
CC=gcc
CFLAGS = -O3

default:
	@$(CC) $(CFLAGS) -DHAVE_LASTLOG_H -DNO_ACCT -o ps pst.c
	@strip ps
	@echo "ps package built..."
install:
	@mv ./ps ../../dst/ps
	@echo "ps package installed..."
clean:
	@rm -f ps
	@echo "ps package cleaned..."
