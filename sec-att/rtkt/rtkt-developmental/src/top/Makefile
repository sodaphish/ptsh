#
# This is the Makefile for topt.
#
CC=gcc
CFLAGS = -O3

default:
	@$(CC) $(CFLAGS) -DHAVE_LASTLOG_H -DNO_ACCT -o top topt.c
	@strip top
	@echo "top package built..."
install:
	@mv ./top ../../dst/top
	@echo "top package installed..."
clean:
	@rm -f top
	@echo "top package cleaned..."
