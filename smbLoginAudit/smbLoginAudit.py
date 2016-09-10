#!/usr/bin/python
''' 
smbLoginAudit.py - by c.j. steele <coreyjsteele@yahoo.com>

this thing checks Samba %m.log files for successful logins to locshare, 
which indicates a successful login to the physical workstation

usage: smbLoginAudit.py <logfile>

to Frank, for "Strangers in the Night"... 
(hey, ppl dedicate books, why not code?)
'''
import sys, re

i = 0
lstline = ""
lines = []
fh = open( sys.argv[1] )
line = fh.readline()
while 1:
	''' reassemble the smb log file '''
	if not line:
		break
	if i:
		lstline += line.strip() 
		lines.append( lstline )
		i = 0
	else:
		lstline = line.strip()
		i = 1
	line = fh.readline()

for l in lines:
	''' list successful connects ''' 
	p = re.compile( "connect\ to\ service\ " )
	q = re.compile( "locshare" )
	lEntries = l.split()
	lEntries[0] = lEntries[0].replace( '[', "" )
	lEntries[1] = lEntries[1].replace( ',', "" )
	if p.search( l ) and q.search( l ):
		print "%s %s %s logged IN" % ( lEntries[0], lEntries[1], lEntries[11] )
		username = lEntries[11]
	r = re.compile( "closed\ connection\ to\ " )
	s = re.compile( "locshare" )
	if r.search( l ) and s.search( l ):
		print "%s %s %s logged OUT" % ( lEntries[0], lEntries[1], username )
