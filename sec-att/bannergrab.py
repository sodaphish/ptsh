#!/usr/bin/python 
#
# bannergrab.py - an IPv4 application banner grabber
# written by sodaphish@protonmail.ch on 2015/11/30
#

import socket, sys, string, unicodedata, re, select
from os.path import basename

all_chars = ( unichr(i) for i in xrange(0x110000) )
control_chars = ''.join(map (unichr, range(0,32) + range(127,160)) )
control_char_re = re.compile('[%s]' % re.escape(control_chars))

def isip( host ):
	try:
		socket.inet_aton(host)
		return True
	except socket.error:
		return False


def remove_control_chars(s):
    return control_char_re.sub('', s)


def bannergrabber(ip_address,port):
	if not isip( ip_address ):
		try:
			ip_address = socket.gethostbyname(ip_address)
		except Exception, e:
			return "%s" % ( e )

	try:
		s = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
		s.settimeout(5.0) #timeout in seconds
		s.connect( (ip_address,port) )
		#send garbage to illicit a response from quiet services
		s.send( "\001\012\012\012" )
		banner = s.recv(4096)
		return ( remove_control_chars( banner ) )
	except Exception, e:
		return "%s" % (e)


if __name__ is "__main__":
	if len(sys.argv) < 3:
		print "usage: %s <ip> <port>" % ( basename( sys.argv[0] ) )
	else:
		ip = sys.argv[1]
		port = int(sys.argv[2])
		banner = bannergrabber(ip,port)
		if banner:
			print "%s:%d:%s" % ( ip, port, banner )
