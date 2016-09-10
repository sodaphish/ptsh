CC=gcc
CFLAGS =
BIN = $(DESTDIR)/usr/bin
MAN = $(DESTDIR)/usr/share/man

default: tcpshow

clean:
	rm -f tcpshow

tcpshow:
	$(CC) $(CFLAGS) -o tcpshow tcpshow.c
	strip tcpshow

install: tcpshow
	install -d $(BIN)
	install ./tcpshow $(BIN)
	install ./tcpshow.1.gz $(MAN)/man8

uninstall: 
	rm -f $(BIN)/tcpshow
	rm -f $(MAN)/man8/tcpshow.1.gz
