#!/usr/bin/python
'''
wimp.py by C.J. Steele <coreyjsteele@yahoo.com>
	(C)opyright 2005, C.J. Steele, all rights reserved.

This basically allows you to do log analysis in of squid logs.

get weblog libraries from http://www.mnot.net/python/WebLog/ 
'''
import getopt, sys, re, os
from time import gmtime, asctime
from weblog import squid
from os.path import isfile, isdir


def mkhtime( inTime ):
	''' adjusts time for GMT to CST (Z-0600) '''
	return asctime( gmtime( inTime - 21600 ) )


def process( clientIP, logFile ):
	try: 
		fh = open( logFile, "r" )
	except IOError, (errno, error):
		sys.stderr.write("Can't open logfile %s: %s" % (logfile, error))
		sys.exit(0)
	log = squid.AccessParser( fh )
	while log.getlogent():
		if log.client == clientIP:
			''' check exceptions '''
			p = re.compile( '.\.(gif|jpg|JPG|GIF|png|PNG|css|js)$' )
			q = re.compile( '.(example.com|test.com|intranet.com).' )
			if not p.search( log.url ) and not q.search( log.url ):
				htime = mkhtime( log.utime )
				print htime, "|" ,log.url


def usage():
	print '''
Usage: wimp.py [options] ip
	options:
		-v : enable verbose mode
		-h : help
		-s : summarrize output (skip image fetchs and known work-related sites.)
'''


def main():
	try:
		opts, args = getopt.getopt( sys.argv[1:], "hvs", ["help"] )
		clientIP = "172.16.104.115" #eventually, get this from cli
	except getopt.GetoptError:
		usage()
		sys.exit( 2 )
	'''continue after getopt stuff'''

	for f in os.listdir( os.getcwd() ):
		r = re.compile( '^access\..' )
		if isfile( f ) and r.search( f ):
			process( clientIP, f )


if __name__ == "__main__":
	main()
