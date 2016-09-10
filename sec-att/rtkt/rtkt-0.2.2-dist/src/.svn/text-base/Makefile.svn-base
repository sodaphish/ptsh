#
# General Makefile for rtkt files...
#

SUB = ls netstat ps tcps top w who wipe dir find lcap

default: 
	@for i in $(SUB); do make -C $$i; done
install:
	@for i in $(SUB); do make install -C $$i; done
clean:
	@for i in $(SUB); do make clean -C $$i; done
