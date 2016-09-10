#!/usr/bin/env python

'''
Web Log Url Parsing class.

Contents:
- Parser: logfile url parsing class
  p_log = weblog.url.Parser(log object)
  methods:
	- p_log.getlogent()
  variables:
	- p_log.cache_size  [ maximum size of url cache ]
  attributes:
    - url_scheme      /  ref_scheme - (http|ftp|gopher...)
    - url_host        /  ref_host 
    - url_path        /  ref_path
    - url_parameters  /  ref_parameters - (section after ';')
    - url_query       /  ref_query - (section after '?')
    - url_fragment    /  ref_fragment - section after '#')
    - all attributes of the log object are available as well.

  This class will parse the url and referer (if available) into their
  respective components. It will also replace each with the unparsed
  result of those components; this assures that the input is fully 
  conformant and in sync with the components.

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


from urlparse import urlparse, urlunparse
from string import lower

class Parser:
	def __init__(self, log):
		self.log = log
		self.cache_size = 10000
		self._cache = {'url': {}, 'ref': {}}
		self._referer_present = 0
		if hasattr(self.log, 'referer'):
			self._referer_present = 1


	def __getattr__(self, attr):
		try:
			return getattr(self.log, attr)
		except AttributeError:
			raise AttributeError, attr


	def getlogent(self):
		''' Increment position in the log and populate requested attributes '''

		if self.log.getlogent():
			### parse url
			if not self._cache['url'].has_key(self.log.url):
				self._cache['url'][self.log.url] = self._parse(self.log.url, 'url')
			(	self.url_scheme, 
				self.url_host, 
				self.url_path, 
				self.url_parameters,
				self.url_query, 
				self.url_fragment, 
				self.url) = self._cache['url'][self.log.url]

			### parse referer
			if self._referer_present:
				if not self._cache['ref'].has_key(self.log.referer):
					self._cache['ref'][self.log.referer] = self._parse(self.log.referer, 'ref')
				(	self.ref_scheme, 
					self.ref_host, 
					self.ref_path, 
					self.ref_parameters,
					self.ref_query, 
					self.ref_fragment, 
					self.referer) = self._cache['ref'][self.log.referer]
			return 1
		else:
			return 0


	def _parse(self, url, url_type):
		if len(self._cache[url_type]) > self.cache_size:
			self._cache[url_type] = {}
		p = urlparse(url)		
		parsed = (p[0], lower(p[1])) + p[2:]
		return parsed + (urlunparse(parsed),)


def test():
	''' basic test suite- modify at will to test full functionality '''

	import sys
	from weblog import combined

	file = sys.stdin
	log = combined.Parser(file)

	p_log = Parser(log)			# url parser

	while p_log.getlogent():
		print "%s\n%s %s %s" % (log.url, p_log.url, p_log.url_path, p_log.url_query)
		print "%s\n%s %s %s" % (log.referer, p_log.referer, p_log.ref_host, p_log.ref_path)
		print



if __name__ == '__main__':
	test()
