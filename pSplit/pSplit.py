#!/usr/bin/python
'''
pSplit.py by C.J. Steele <coreyjsteele@yahoo.com>

This is a simple script used to chop large pcap files into more manageable
sizes for analysis.  `pJoin.py` can be used to re-merge these smaller files.
It may not be fast, but at least it works!

usage: pSplit.py [source_file] [template] [bytes]
	source_file = the large pcap file
	template = the base-name of the little files (-#.cap is appended.)
	bytes = the approximate maximum size of the little files
'''
import sys
from pcapy import *
from impacket.ImpactDecoder import EthDecoder, LinuxSLLDecoder
from impacket import ImpactPacket


def showUsage():
	print "pSplit.py by C.J. Steele <coreyjsteele@yahoo.com>"
	print "usage: pSplit.py [source_file] [template] [bytes]"
	print "    source_file = the large pcap file"
	print "    template = the base-name of the little files (-#.cap is appended.)"
	print "    bytes = the approximate maximum size of the little files"
	print ""


if len( sys.argv ) < 3:
	showUsage()
	sys.exit( 1 )

fileCount = 1
p = open_offline( sys.argv[1] )

datalink = p.datalink()
if DLT_EN10MB == datalink:
	decoder = EthDecoder()
elif DLT_LINUX_SLL == datalink:
	decoder = LinuxSLLDecoder()
else: 
	raise Exception( "Datalink type not supported: " % datalink )

while 1:
	try: 
		(hdr, data ) = p.next()
		filename = "%s_%d.cap" % ( sys.argv[2], fileCount )
		pktCount = 0
		capSize = 0
		d = p.dump_open( filename )
		while capSize < int( sys.argv[3] ):
			pkt = decoder.decode( data )
			try: 
				bytes = len( pkt.get_packet() )
			except:
				pass
			capSize += bytes
			pktCount += 1
			d.dump( hdr, data )
		fileCount += 1
		print "%s is %d bytes with %d packets" % ( filename, capSize, pktCount )
	except:
		break
