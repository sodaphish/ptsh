#!/usr/bin/python
'''
chkps.py by C.J. Steele <coreyjsteele@yahoo.com>

checks /var/run/utmp for entries that have no corresponding entry in
/proc/<PID>; such entries indicate some level of corruption in UTMP, which
could be an indication that utmp has been hacked or that the process table has
been hacked...some kidz are sloppy

NOTE: Only *nix's supporting procps will have /proc, and therefore will be
capable of using this script.

TODO: 
 * handle sys.argv[1] passing of which file to process, 
 * cli switch to specify utmp or wtmp (or both)
'''
import utmp, time, os.path
from UTMPCONST import *

utmpRecord = utmp.UtmpRecord( UTMP_FILE )

headerNotSet = 1

while 1:
	utEntry = utmpRecord.getutent()
	if not utEntry:
		break
	if utEntry[0] == USER_PROCESS and not os.path.exists( ('/proc/%s' % utEntry[1]) ):
		if headerNotSet:
			print "%-10s %-10s %-30s %-27s %-8s %-5s" % ( "USER", "TTY", "HOST", "LOGIN", "PID", "STATUS" )
			headerNotSet = 0
		print "%-10s %-10s %-30s %-27s %-8d %-5d" % ( utEntry[4], utEntry[2], utEntry[5], time.ctime( utEntry[8][0] ), utEntry[1], -1 )

if headerNotSet:
	print "Process table appears to be in tact."

utmpRecord.endutent()
