#
# This is the Makefile for wipe.
#
CC=gcc

CFLAGS = -O3

default: linux
#	@echo
#	@echo Wipe v0.01 !
#	@echo
#	@echo "Usage: 'make <system type>' where System types are:"
#	@echo
#	@echo "    linux  freebsd  sunos4  solaris2  ultrix"
#	@echo "    aix  irix  digital  bsdi  netbsd  hpux"
#	@echo

#
# Linux : Tested on various 1.2.x, 1.3.x and pre 2.0 systems.
#         Accounting seems to be still in development.
#
linux: wipe.c
	@$(CC) $(CFLAGS) -DHAVE_LASTLOG_H -DNO_ACCT -o wipe wipe.c
	@echo "wipe (linux) package built..."

#
# FreeBSD : Tested on 2.1.0.  Accounting file is at /var/account/acct.
#
freebsd: wipe.c
	$(CC) $(CFLAGS) -DACCT_FILE=\"/var/account/acct\" -o wipe wipe.c

#
# SunOS 4.1.x : Standard BSD type setup.
#
sunos4: wipe.c
	$(CC) $(CFLAGS) -DHAVE_LASTLOG_H -o wipe wipe.c

#
# Solaris 2.x : Ugh, System V.  Has UTMPX.
#
solaris2: wipe.c
	$(CC) $(CFLAGS) -DHAVE_LASTLOG_H -DHAVE_UTMPX -o wipe wipe.c

#
# Ultrix :
#
ultrix: wipe.c
	$(CC) $(CFLAGS) -DHAVE_LASTLOG_H -o wipe wipe.c

#
# AIX :
#
aix: wipe.c
	$(CC) $(CFLAGS) -o wipe wipe.c

#
# IRIX :
#
irix: wipe.c
	$(CC) $(CFLAGS) -DHAVE_LASTLOG_H -DHAVE_UTMPX -o wipe wipe.c

#
# Digital/OSF :
#
digital: wipe.c
	$(CC) $(CFLAGS) -DHAVE_LASTLOG_H -o wipe wipe.c

#
# BSDI :
#
bsdi: wipe.c
	$(CC) $(CFLAGS) -o wipe wipe.c

#
# NetBSD :
#
netbsd: wipe.c
	$(CC) $(CFLAGS) -o wipe wipe.c

#
# HP-UX : 
#
hpux: wipe.c
	$(CC) $(CFLAGS) -o wipe wipe.c

install:
	mv ./wipe ../../dst/wipe

clean:
	rm -f wipe
