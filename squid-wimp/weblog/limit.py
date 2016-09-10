#!/usr/bin/env python

'''
Web Log Limiting classes.

Contents:

- Path: directory/page limiting class
  pl_log = weblog.limit.Path(log object)
  methods:
    - pl_log.getlogent()
  variables:
    - pl_log.page_limit [ list of page names/file types to limit to ]
    - pl_log.page_exclude [ list of page names/file types to exclude ]
    - pl_log.path_limit [ list of specific pages/directories to limit to ]
    - pl_log.path_exclude [ list of specific pages/directories to exclude ]
    - pl_log.cache_size (size of page cache)
  read-only variables:
    - pl_log.num_skipped (number of lines that have been passed over)
  attributes:
    - all attributes from the log object are available.

  Page/Directory limiting requires previous use of weblog.url.Parse. Page
  and directory limitations are case sensitive.
  
  The page_limit and page_exclude specifications are for excluding a page
  name or file type; e.g., 'foo.html' or '.gif', not '/foo/bar/'.
  The dir_limit and dir_exclude specifications are from the document root; 
  e.g., '/foo/bar/baz.html', not 'baz.html' and '/bat.html' not 'bat.html'.
  When setting any of these four attributes, make sure to pass the arguments
  as a [list], all at once.


- Host: client host/domain/ip/network limiting class
  hl_log = weblog.limit.Host(log object)
  methods:
    - hl_log.getlogent()
  variables:
    - hl_log.limit_host [ list of hostnames/domains to limit to ]  
    - hl_log.exclude_host [ list of hostnames/domains to exclude ]
    - hl_log.cache_size (size of page cache)
  read-only variables:
    - hl_log.num_skipped (number of lines that have been passed over)
  attributes:
    - all attributes from the log object are available.    

  Hosts can be a FQDN or domain name; e.g., 'foo.bar.com', 'bar.com', '.com'.
  Hosts are not case-sensitive.
  
  If weblog.resolve has been used, the .host attribute will be used when 
  available; otherwise, the .client attribute will be used, and will 
  not match if it is not of the correct type. 


- Time: start/end time limiting class
  tl_log = weblog.limit.Time(log object)
  methods:
	- tl_log.getlogent()
  booleans:
    - tl_log.end_stop ( if set, will getlogent() will return 0 on first
                       line matching l_log.end )
  variables:
	- tl_log.start [ exclude log lines before this unix epoch time ]
	- tl_log.end [ exclude log lines after this unix epoch time ]
  read-only variables:
    - hl_log.num_skipped (number of lines that have been passed over)
  attributes:
	- all attributes of the log object are available.

  Because Time only needs the utime attribute from the parser, it
  pays to put it at the top of the 'stack' of instances, right below
  the Parser itself.


- test: test function
'''


# (c) 1998 Copyright Mark Nottingham
# <mnot@pobox.com>
#
# This software may be freely distributed, modified and used,
# provided that this copyright notice remain intact.
#
# This software is provided 'as is' without warranty of any kind.



__version__ = '0.99'

import re
from string import join
from types import ListType


class Path:
	''' Path Limiting Class '''

	def __init__(self, log):
		self.log = log
		self.dir_limit = []
		self.dir_exclude = ['::::::::']
		self.page_limit = []
		self.page_exclude = ['::::::::']
		self.cache_size = 10000
		self.num_skipped = 0
		self._cache = {}


	def __getattr__(self, attr):
		try:
			return getattr(self.log, attr)
		except AttributeError:
			raise AttributeError, attr


	def __setattr__(self, attr, value):
		if type(value) == ListType:
			value = map(lambda a: re.escape(a), value)
		if attr == 'dir_limit':
			self._dir_limit_pat = "^(" + join(value, "|") + ")"
			self._dir_limit_comp = re.compile(self._dir_limit_pat)
		if attr == 'dir_exclude':
			self._dir_exclude_pat = "^(" + join(value, "|") + ")"
			self._dir_exclude_comp = re.compile(self._dir_exclude_pat)
		if attr == 'page_limit':
			self._page_limit_pat = "(" + join(value, "|") + ")$"
			self._page_limit_comp = re.compile(self._page_limit_pat)
		if attr == 'page_exclude':
			self._page_exclude_pat = "(" + join(value, "|") + ")$"
			self._page_exclude_comp = re.compile(self._page_exclude_pat)
		self.__dict__[attr] = value


	def getlogent(self):
		''' Increment position in the log and populate requested attributes '''

		while self.log.getlogent():
			try:
				if self._cache[self.log.url_path]:
					return 1
			except KeyError:
				if self._path_match(self.log.url_path):
					return 1
			self.num_skipped = self.num_skipped + 1
		return 0


	def _path_match(self, path):
		''' matching engine; returns 1 if page is to be ignored '''

		if len(self._cache) > self.cache_size:
			self._cache = {}
		i = 1
		if self._dir_limit_comp.search(path) == None: i = 0
		elif self._page_limit_comp.search(path) == None: i = 0
		elif self._dir_exclude_comp.search(path) != None: i = 0
		elif self._page_exclude_comp.search(path) != None: i = 0					
		self._cache[path] = i
		return self._cache[path]



class Host:
	''' Client Host/Domain Limiting Class '''
	
	def __init__(self, log):
		self.log = log
		self.host_limit = []
		self.host_exclude = ['::::::::']
		self.cache_size = 10000
		self.num_skipped = 0
		self._cache = {}
		if hasattr(self.log, 'host'):
			self._loc = 'host'
		else:
			self._loc = 'client'

		
	def __getattr__(self, attr):
		try:
			return getattr(self.log, attr)
		except AttributeError:
			raise AttributeError, attr


	def __setattr__(self, attr, value):
		if attr == 'host_limit':
			self._host_limit_pat = "(" + join(value, "|") + ")\.?$"
			self._host_limit_comp = re.compile(self._host_limit_pat, re.IGNORECASE)
		if attr == 'host_exclude':
			self._host_exclude_pat = "(" + join(value, "|") + ")\.?$"
			self._host_exclude_comp = re.compile(self._host_exclude_pat, re.IGNORECASE)
		self.__dict__[attr] = value


	def getlogent(self):
		''' Increment position in the log and populate requested attributes '''

		while self.log.getlogent():
			try:
				if self._cache[getattr(self.log, self._loc)]:
					return 1
			except KeyError:
				if self._host_match(getattr(self.log, self._loc)):
					return 1
			self.num_skipped = self.num_skipped + 1
		return 0
		

	def _host_match(self, host):
		''' matching engine; returns 1 if page is to be ignored '''

		if len(self._cache) > self.cache_size:
			self._cache = {}
		i = 1
		if self._host_limit_comp.search(host) == None: i = 0
		elif self._host_exclude_comp.search(host) != None: i = 0
		self._cache[host] = i
		return self._cache[host]
			


class Time:
	''' Start/Stop Time Limiting Class '''
	
	def __init__(self, log):
		self.log = log
		self.start = 0
		self.end = 2000000000
		self.end_stop = 0
		self.num_skipped = 0

	
	def __getattr__(self, attr):
		try:
			return getattr(self.log, attr)
		except AttributeError:
			raise AttributeError, attr


	def getlogent(self):
		''' Increment position in the log and populate requested attributes '''

		while self.log.getlogent():
			if self.log.utime < self.start:
				self.num_skipped = self.num_skipped + 1
				continue
			if self.log.utime > self.end:
				if self.end_stop:
					return 0
				else:
					self.num_skipped = self.num_skipped + 1
					continue
			return 1
		return 0	
	




def test():
	''' basic test suite- modify at will to test full functionality '''

	import sys
	from weblog import combined, url

	file = sys.stdin
	log = combined.Parser(file)

	up_log = url.Parser(log)

	lim_log = Host(up_log)
	lim_log.host_limit = ['.com']
	lim_log.host_exclude = ['aol.com']

	jpg_log = Path(lim_log)
	jpg_log.page_limit = ['.jpg']

	s_log = Time(jpg_log)
	s_log.start = 899306347

	while s_log.getlogent():
		print "%s %s" % (s_log.client, s_log.url)
	print "lines processed-", log.num_processed
	print "error lines-", log.num_error
	print "lines skipped- %s host, %s path, %s time, %s total" % (
			lim_log.num_skipped, jpg_log.num_skipped, s_log.num_skipped,
			lim_log.num_skipped + jpg_log.num_skipped + s_log.num_skipped)


if __name__ == '__main__':
	test()
