#!/usr/bin/python
'''
stripBanners.py 

strips top and bottom 22 lines from ORA books downloaded via:

  `wget -U "Internet Explorer 6.0" -m http://www.unix.org.ua/orelly`

...it works on OS X with python 2.3 and Linux with python 2.3, but I 
make no guarantees about other platforms.

oh, and btw: i'm new to python, if that isn't blatantly obvious.

''' 


import sys, re
from string import strip
from os.path import isdir, isfile, abspath, isabs
from os import listdir, getcwd


def processDir( input ):
	if isdir( input ):
		topDir = listdir( input )
		for node in topDir:
			node = input + "/" + node
			node = abspath( node )
			if isdir( node ):
				processDir( node )
			elif isfile( node ):
				processFile( node )
	elif isfile( input ):
		processFile( input )


def processFile( fileName ):
	p = re.compile( ".\.(htm|html)$" )
	if p.search( fileName ):
		''' its an htm file and needs to be processed '''
		try:
			fh = open( fileName, "r" )
		except IOError, ( errno, error ):
			sys.stderr.write( "Can't open logfile %s: %s" % ( fileName, error ) )

		lineCount = 0
		lines = list()

		line = fh.readline()
		while( line ):
			if lineCount > 21:
				lines.append( line )
			lineCount += 1
			line = fh.readline()

		totalLines = lineCount - 22
		lineCount = 0

		try:
			fh2 = open( fileName, "w" )
		except IOError, ( errno, error ):
			sys.stderr.write( "Can't open file %s: %s" % ( fileName, error ) ) 
			sys.exit( 0 )

		for l in lines:
			if lineCount <= totalLines - 24:
				fh2.write( l )
			lineCount += 1
	return


basePath = sys.argv[1] 
processDir( basePath )
