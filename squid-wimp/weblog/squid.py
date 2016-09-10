#!/usr/bin/env python

'''
Squid Web proxy cache log parsing classes.

Contents:

- AccessParser: squid access logfile parser class
  log = AccessParser(log filehandle)
  - methods:
	log.getlogent()
  - attributes:
    log.utime
    log.elapsed
	log.client
	log.log_tag
	log.status
	log.bytes
	log.method
	log.url
	log.ident
	log.peer_tag
	log.peerhost
	log.mimetype
  - read-only variables:
	log.num_error
	log.num_processed

- StoreParser: squid store logfile parser class
  log = StoreParser(log filehandle)
  - methods:
	log.getlogent()
  - attributes:
    log.utime
    log.action
	log.status
	log.datehdr
	log.lastmod
	log.expires
	log.mimetype
	log.expect_len
	log.real_len
	log.method
	log.url
  - read-only variables:
	log.num_error
	log.num_processed

- test: test function
'''


# (c) 1998 Copyright Mark Nottingham
# <mnot@pobox.com>
#
# This software may be freely distributed, modified and used, 
# provided that this copyright notice remain intact.
#
# This software is provided 'as is' without warranty of any kind.


# Squid Access Logfile Format
# ---------------------------
#
# Version 1.1 Access log
# 
# timestamp elapsed_time client log_tag/status bytes method URL rfc931 \
# peer_tag/peerhost mimetype
#
# rfc931: identd info, - otherwise
#
#
# Squid Store Logfile Format
# --------------------------
#
# Version 1.1 Store log
#
# time action status datehdr lastmod expires type expect-len/real-len \
# method key
#
#
# for more information about both formats, see the Squid FAQ at
# http://squid.nlanr.net/




__version__ = '0.99'


from string import atoi, atof, split
import sys


class AccessParser:
	''' Splitting Squid Access Logfile Parser '''

	def __init__(self, file_descriptor):
		self.num_processed = 0
		self.num_error = 0
		self._fd = file_descriptor			
		self.utime = 0
		self.elapsed = 0
		self.client = ''
		self.log_tag = ''
		self.status = 0
		self.bytes = 0
		self.method = ''
		self.url = ''
		self.ident = ''
		self.peer_tag = ''
		self.peerhost = ''
		self.mimetype = ''

	
	def getlogent(self):
		''' Increament location in the log and populate object attributes '''

		while 1: 	# loop until we find a valid line, or end
			line = self._fd.readline()		
			if not line: return 0
			self.num_processed = self.num_processed + 1
			
			n = split(line, None)
			if len(n) != 10:
				self.num_error = self.num_error + 1
			else:
				try:
					self.utime = int(atof(n[0]))
					self.elapsed = int(atoi(n[1]))
					self.client = n[2]
					(self.log_tag, status) = split(n[3], '/', 2) 
					self.status = atoi(status)
					self.bytes = atoi(n[4]) 
					self.method = n[5] 
					self.url = n[6]
					self.ident = n[7]
					(self.peer_tag, self.peerhost) = split(n[8], '/', 2)
					self.mimetype = n[9]
				except:
					self.num_error = self.num_error + 1
					continue
				return 1



class StoreParser:
	''' Splitting Squid Store Logfile Parser '''

	def __init__(self, file_descriptor):
		self.num_processed = 0
		self.num_error = 0
		self._fd = file_descriptor
		self.utime = 0
		self.action = 0
		self.status = ''
		self.datehdr = ''
		self.lastmod = 0
		self.expires = 0
		self.mimetype = ''
		self.expect_len = ''
		self.real_len = ''
		self.method = ''
		self.url = ''

	
	def getlogent(self):

		''' Increament location in the log and populate object attributes '''

		while 1: 	# loop until we find a valid line, or end
			line = self._fd.readline()		
			if not line: return 0
			self.num_processed = self.num_processed + 1
			
			n = split(line, None)
			if len(n) != 10:
				self.num_error = self.num_error + 1
			else:
				try:
					self.utime = int(atof(n[0]))
					self.action = n[1]
					self.status = atoi(n[2])
					self.datehdr = atoi(n[3])
					self.lastmod = atoi(n[4]) 
					self.expires = atoi(n[5]) 
					self.mimetype = n[6]
					(expect_len, real_len) = split(n[7], '/', 2)
					self.expect_len = atoi(expect_len)
					self.real_len = atoi(real_len)
					self.method = n[8]
					self.url = n[9]
				except:
					self.num_error = self.num_error + 1
					continue
				return 1





			
def test_access():
	''' basic test suite- modify at will to test all functionality '''
	
	file = sys.stdin
	log = AccessParser(file)	
	while log.getlogent():
		print "%s %s %s %s" % (log.client, log.log_tag, log.bytes, log.peerhost)
	print "lines: %s" % (log.num_processed)
	print "error: %s" % (log.num_error)
		
		
if __name__ == '__main__':
	test_access()

