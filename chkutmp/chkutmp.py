#!/usr/bin/python
'''
chkutmp.py 

checks /var/run/utmp for entries that have no corresponding entry in 
/proc/<PID>; such entries indicate some level of corruption in UTMP, 
which causes various problems for some applications

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
	print UTMP_FILE, "appears to be in tact."

utmpRecord.endutent()
