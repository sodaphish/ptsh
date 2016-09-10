#!/usr/bin/python
'''
pao.py - the PIX ACL Optimizer by C.J. Steele <coreyjsteele@yahoo.com>
	(C)opyright 2005, C.J. Steele, all rights reserved.

the PIX ACL Optimizer is designed to process the results of `sh access-list`
executed on a PIX and then optimize the rule order by determining the highest
traffic ACL's and ordering them up.  

usage: pao.py <PIXOUTPUTFILE>

'''
import sys, re

fh = open( sys.argv[1] )
line = fh.readline()
p = re.compile( r'\bpermit\b|\bdeny ' )
q = re.compile( 'access-list ' )
r = re.compile( '\(hitcnt\=' )
s = re.compile( '\)' )
while 1:
	''' if we got eof, bail '''
	if not line:
		break

	''' we're in the file '''
	if p.search( line ):
		line = line.strip()
		line = q.sub( '', line )
		linElements = line.split()

		aclName = linElements[0]
		aclLineNo = linElements[2]
		aclHitCount = linElements[len(linElements)-1]
		aclHitCount = r.sub( '', aclHitCount )
		aclHitCount = s.sub( '', aclHitCount )

		aclThingy = ""
		for x in range( 3, len( linElements )-1 ):
			#aclThingy = aclThingy , " " , linElements[x]
			aclThingy += " " + linElements[x]

		print "%s access-list %s%s" % ( aclHitCount, aclName, aclThingy )

	''' move ahead our readline() '''
	line = fh.readline()
