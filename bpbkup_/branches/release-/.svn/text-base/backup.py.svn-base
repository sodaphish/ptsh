#!/usr/local/bin/python
'''
backup.py by C.J. Steele <coreyjsteele@yahoo.com>
	(C)opyright 2005, C.J. Steele, all rights reserved.

this is a backup script that will allow you to perform full or daily 
incremental backups of data and store the results of your backups in 
a db3 database file that can be searched with the bpbq.py tool.

TODO:
 * make routines more bullet-proof -- catch errors, check input, etc.
 * (maybe) compress backedup files
 * (maybe) implement differential backups
'''
import getopt, posix, os, sys, tempfile, anydbm, shutil
from stat import *
from time import time, strftime, localtime


timeNow = int( time() )
currentDate = strftime( '%m%d%Y', localtime() );
backupRoot = tempfile.mkdtemp( "-" + currentDate, 'bpbackup-', '/var/bkup/' )
backupDone = False
backupType = "full"
backupDB = "/var/bkup/bpbkup"
verbose = False


def initializeBackup():
	if not os.path.isdir( backupRoot ):
		sys.stderr.write( "E: Couldn't find " + backupRoot + "\n" )
		return 0
	#db = anydbm.open( backupDB, 'r' ) 
	#if not db:
	#	sys.stderr.write( "E: Couldn't find " + backupDB + "\n" )
	#	return 0
	#db.close()
	return 1


def recursiveList( rootDir ):
	fileList = []
	for x in posix.listdir( rootDir ):
		fullPath = rootDir + "/" + x
		if( os.path.isdir( fullPath ) ):
			fileList += recursiveList( fullPath )
		else:
			# its a file, add it to our list to bakup
			fileList.append( fullPath )
	return fileList


def bornToday( fileName ):
	if( timeNow - os.stat( fileName )[ST_MTIME] < 86400 ):
		return 1
	return 0


def backupFile( fileName ):
	'''backup a file to the backupRoot
	NOTE: though doing the full open and close on the DB every time we backup a file is inefficient, its safe.
	TODO: 
		* need to create directories with safe permissions
		* add checks to make sure files exist in the backup dir after they've been backedup
		* consider implementing checksuming on backups to verify that they were the same at the time of backup
	'''
	db = anydbm.open( backupDB, 'c' )
	backedupFileName = backupRoot + "/" + fileName 
	pathInfo = os.path.dirname( backedupFileName )
	if not os.path.exists( pathInfo ):
		os.makedirs( pathInfo )
	shutil.copyfile( fileName, backedupFileName )
	shutil.copystat( fileName, backedupFileName )
	db[backedupFileName] = repr( timeNow )
	db.close()


def usage():
	print '''
	Usage: backup.py <-f|-i> <-d /path/to/stored/backups> </paths/to/backup>
	options:
		-h, --help : this help message
		-f         : perform a full backup
		-i         : perform an incremental backup
		-d         : directory where backups should be stored
	'''


def main():
	global backupType

	try:
		opts, args = getopt.getopt( sys.argv[1:], "hvfid:", ["help"] )
	except getopt.GetoptError:
		usage()
		sys.exit( 2 )

	if len(args) >= 1:
		for o, a in opts:
			if o == "-v":
				verbose = True
			if o in ( "-h", "--help" ):
				usage()
				sys.exit( 2 ) 
			if o == "-d":
				if os.path.exists( a ):
					os.file.rmdir( backupRoot )
					backupRoot = a
			if o == "-f":
				backupType = "full"
			if o == "-i":
				backupType = "incremental"
	else:
		sys.stderr.write( "E: you must specify at least one directory to backup\n" )

	if initializeBackup():
		if backupType == "full":
			for dir in args:
				for file in recursiveList( dir ):
					backupFile( file )
		elif backupType == "incremental":
			for dir in args:
				for file in recursiveList( dir ):
					if bornToday( file ):
						backupFile( file )
	else:
		sys.stderr.write( "E: initializeBackup() failed.\n" )
		sys.exit( 2 )


if __name__ == "__main__":
	main()
