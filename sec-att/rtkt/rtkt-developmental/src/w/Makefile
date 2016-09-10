#
# This is the Makefile for wt.
#
CC=gcc
CFLAGS = -O3

default:
	@$(CC) $(CFLAGS) -DHAVE_LASTLOG_H -DNO_ACCT -o w wt.c
	@echo "wt package built..."
install:
	@mv ./w ../../dst/w
	@echo "wt package installed..."
clean:
	@rm -f w
	@echo "wt package cleaned..."
