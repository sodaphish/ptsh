#!/usr/bin/env python
import anydbm, re, sys, getopt
from time import asctime, localtime



def findFile( fileName ):
	q = re.compile( fileName )
	d = anydbm.open( "/var/bkup/bpbkup", 'r' )
	for key in d.keys():
		if q.search( key ):
			a = d[key]
			print ( "%s: %s\n" ) % ( asctime( localtime( int( a ) ) ), key )
	d.close()


def findDate( date ):
	q = re.compile( date )
	d = anydbm.open( "/var/bkup/bpbkup", 'r' )
	for key in d.keys():
		if q.search( d[key] ):
			a = d[key]
			print ( "%s: %s\n" ) % ( asctime( localtime( int( a ) ) ), key )
	d.close()


if len( sys.argv ) > 1:
	findFile( sys.argv[1] )
else:
	findFile( "" )
