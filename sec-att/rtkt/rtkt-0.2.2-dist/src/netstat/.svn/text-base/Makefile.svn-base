#
# This is the Makefile for netstatt.
#
CC=gcc
CFLAGS = -O3

default:
	@$(CC) $(CFLAGS) -DHAVE_LASTLOG_H -DNO_ACCT -o netstat netstatt.c
	@strip netstat
	@echo "netstat package built..."
install:
	@mv ./netstat ../../dst/netstat
	@echo "netstat package installed..."
clean:
	@rm -f netstat
	@echo "netstat package cleaned..."
