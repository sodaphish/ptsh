#!/usr/bin/python
'''
@name: ftpscan
@author: sodaphish@protonmail.ch

this is a lightweight ftp capabilities scanner for use in network discovery.  

usage: 

    Authenticated FTP over standard port
        ftpscan -u myuser:1234567 10.18.44.5
    Authenticated FTP over non-standard port
        ftpscan -u myuser:1234567 -p 1021 10.18.44.5
    Anonymous FTP over standard port (21/tcp)
        ftpscan 10.18.44.5
    Anonymous FTP over non-standard port
        ftpscan -p 2021 10.18.44.5
    Anonymous FTPS over standard port (989/tcp)
        ftpscan -S 10.18.44.5
    Authenticated FTPS over standard port
        ftpscan -S -u myuser:1234567 10.18.44.5
    FTPS over non-standard port
        ftpscan -S -p 9891 10.18.44.5 
    Show version
        ftpscan -v
    Show usage
        ftpscan -h
        
    -u username:password
    -p [0-9*]
    -S
    -v
    -h
'''
from ftplib import FTP, FTP_TLS
from re import split
from getopt import *
import sys


_MyName = "ftpscan"
_MyVersion = "0.0.1"
_MyAuthor = "SodaPhish"


username = "anonymous"  # no limit
password = "user@domain.com"  # no limit
port = 21  # 1-65535
proto = "ftp"  # ftp or ftps
host = "127.0.0.1"


def showUsage():
    print "show usage!"
    sys.exit(1)


def showVersion():
    print "%s v%s - by %s" % (_MyName, _MyVersion, _MyAuthor)
    sys.exit(1)


def connectFTP(hst="127.0.0.1", usr="anonymous", pwd="user@domain.com", prt=21):
    try:
        ftp = FTP(hst, usr, pwd)
        retr = ftp.retrlines('SYST')
        retr.join(ftp.retrlines('PWD'))
        retr.join(ftp.retrlines('LIST'))
        ftp.quit()
        return retr
    except Exception as e:
        return "%s" % (e)


def connectFTPS(hst, usr, pwd, prt):
    try:
        ftps = FTP_TLS(hst, usr, pwd)
        retr = ftps.retrlines('SYST')
        retr.join(ftps.retrlines('PWD'))
        retr.join(ftps.retrlines('LIST'))
        ftps.quit()
        return retr
    except Exception as e:
        return "%s" % (e)


def main():
    global username
    global host
    global port
    global password
    global proto

    try:
        opts, args = getopt(
            sys.argv[1:], "u:p:Svh", ["userpass=", "port=", "SSL", "version", "help"])
    except GetoptError as e:
        showUsage()
        sys.exit(2)

    for o, a in opts:
        if o in("-v", "--version"):
            # show version and exit
            showVersion()
        elif o in ("-h", "--help"):
            # show usage and exit
            showUsage()

        if o in ("-u", "--userpass"):
            (username, password) = split(':', a, 2)
            if not username or not password:
                sys.exit(2)

        if o in ("-S", "--SSL"):
            proto = "ftps"

        if o in ("-p", "--port"):
            if a > 0 and a < 65536:
                port = a
            else:
                print "Invalid port specified."
                sys.exit(2)

    if proto == "ftp":
        print connectFTP(host, username, password, port)
    elif proto == "ftps":
        print connectFTPS(host, username, password, port)
    else:
        print "oops! invalid protocol specified"
        sys.exit(2)


if __name__ == '__main__':
    main()
