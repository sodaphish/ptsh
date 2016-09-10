#
# This is the Makefile for lcap.
#
CC=gcc
CFLAGS = -O3 -Wall

default:
	@$(CC) $(CFLAGS) -DHAVE_LASTLOG_H -DNO_ACCT -o lcap lcap.c
	@strip lcap
	@echo "lcap package built..."
install:
	@mv ./lcap ../../dst/lcap
	@echo "lcap package installed..."
clean:
	@rm -f lcap
	@echo "lcap package cleaned..."
