#!/usr/bin/env python
'''
'''
import getopt, posix, os, sys
from stat import *
from time import time


timeNow = int( time() )
verbose = False
dryRun = False
# default is one week old
maxAge = int( 86400 * 7 )


def recursiveList( rootDir ):
	fileList = []
	for x in posix.listdir( rootDir ):
		fullPath = rootDir + "/" + x
		try: 
			if( os.path.isdir( fullPath ) ):
				fileList += recursiveList( fullPath )
			else:
				fileList.append( fullPath )
		except OSError, ( errno, error ): 
			sys.stderr.write( error );
	return fileList


def dirIsEmpty( dirName ):
	if len( recursiveList( dirName ) ) > 0:
		return 0
	return 1


def tooOld( fileName ):
	global maxAge, timeNow
	if( int(timeNow - os.stat( fileName )[ST_ATIME]) > maxAge ):
		return 1
	return 0


def nukeFile( fileName ):
	if not dryRun: 
		if os.path.isfile( fileName ):
			#do the nuking
			print "W: nuking " + fileName
			posix.remove( fileName )
	else:
		if os.path.isfile( fileName ):
			print "I: nuking " + fileName
	return 0


def nukeDir( dirName ):
	if not dryRun:
		if os.path.exists( dirName ) and dirIsEmpty( dirName ):
			print "W: nuking " + dirName
			posix.rmdir( dirName )
	else:
		if os.path.exists( dirName) and dirIsEmpty( dirName ):
			print "I: nuking " + dirName
	return 0


def usage():
	print '''
	usage
	'''


def main():
	global maxAge, verbose, dryRun

	try:
		opts, args = getopt.getopt( sys.argv[1:], "hvdm:", ["help"] )
	except getopt.GetoptError:
		usage()
		sys.exit( 2 )

	if len(args) >= 1:
		for o, a in opts:
			if o in ( "-h", "--help" ):
				usage()
				sys.exit( 2 ) 
			if o == "-v":
				verbose = True
			if o == "-d":
				dryRun = True
			if o == "-m":
				maxAge = int( a )
				
	else:
		sys.stderr.write( "E: you must specify at least one directory\n" )

	for dir in args:
		if os.path.exists( dir ):
			for file in recursiveList( dir ):
				if tooOld( file ):
					nukeFile( file )
			if dirIsEmpty( dir ):
				nukeDir( dir )
		else: 
			sys.stderr.write( "E: " + dir + " doesn't exist!\n" )
			sys.exit( 1 )

if __name__ == "__main__":
	main()
