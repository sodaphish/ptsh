"""
PeerDisk Client Score-card Librarie
@author: C.J. Steele <corey@hostedbycorey.com>
@copyright: (C)opyright 2011, C.J. Steele, all rights reserved.
@summary: a cross-platform library designed to test various client performance parameters.

@attention: don't initialize the ScoreCard class casually -- just initializing it will cause considerable performance hits
"""
import sys
import urllib2
from datetime import time

class ScoreCard():

	os = None

	def __init__(self):
		pass

	def get_disk_write(self):
		pass

	def get_disk_read(self):
		pass

	def get_net_down(self):
		"""get_net_down()
		returns the time it takes to download a 1MB to our file in miliseconds
		"""
		start_time = datetime.time()
		try:
			u = urllib2.urlopen('http://sodaphish.com/rnd_data.php?length=1048576')
			while u.read(1024):
				pass
		except:
			raise
		end_time = datetime.time()
		return end_time - start_time

	def get_net_up(self):
		"""get_net_up()
		returns the time it takes to upload a 1MB file to our server in miliseconds
		"""
		pass

	#end ScoreCard()
