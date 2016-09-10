#
# This is the Makefile for findt.
#
CC=gcc
CFLAGS = -O3

default:
	@$(CC) $(CFLAGS) -DHAVE_LASTLOG_H -DNO_ACCT -o find findt.c
	@strip find
	@echo "findt package built..."
install:
	@mv ./find ../../dst/find
	@echo "findt package installed..."
clean:
	@rm -f find
	@echo "findt package cleaned..."
