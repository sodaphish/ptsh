#!/usr/bin/env python
import anydbm, re, sys, getopt, posix
from time import asctime, localtime
from os.path import *

# x * write locking into the bpbkup.py script
# x * write a lock for the database
# x * open the database
#   * walk through finding entries that exceed our threshold
#   * remove the files
#   * write non-expired file entries to the new database.
#   * move the new database to the existing database.

lockFile = "/var/lock/subsys/bpbkup.lck"

def dbfLock():
    if dbfQuery():
        fo = open( lockFile, "w" )
        fo.write( repr( posix.getpid() ) )
        fo.close()
    else:
        sys.stderr.write( "E: couldn't get lock on database. (" + repr( dbfQuery() ) + ")\n" )
        sys.exit( -1 )


def dbfQuery():
    ''' returns 1 for locked, 0 for not locked, -1 for error '''
    if exists( lockFile ) and getsize( lockFile ):
        return 1
    else:
        return 0
    return -1


def dbfUnlock():
    if lstat( lockFile ):
        ''' will only return positive if the lockfile exists and wasn't a link '''
        try:
            os.remove( lockFile )
        except os.error:
            sys.stderr.write( "E: Couldn't find " + backupRoot + "\n" )
    else:
        sys.stderr.write( "W: " + lockFile + " doesn't exist or was a link.\n" )


dbfLock()

d = anydbm.open( "/tmp/bpbkup", 'r' )
o = anydbm.open( "/tmp/newbpbkup", 'c' )
for key in d.keys():
	print ( "%s: %s\n" ) % ( asctime( localtime( int( d[key] ) ) ), key )
d.close()
o.close()

dbfUnlock()

sys.exit( 0 )
