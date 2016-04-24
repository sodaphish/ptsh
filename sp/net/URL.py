"""
a helper class for *HTTP* URL's

@NOTE: surely someone else has written this before, but, I couldn't find one, so I wrote this one.

@author: SodaPhish <sodaphish@protonmail.ch>

TODO: 
 * support other protocols other than HTTP
 * add a timeout to gethostbyname lookups 
"""

import sys,socket
from urlparse import urlparse
from socket import gethostbyname

try:
	import ipaddress 
except: 
	print "you need to `pip install ipaddress` before proceeding"
	sys.exit(2)



class InvalidURL(Exception):
	"""
	InvalidURL exception what we raise if something isn't a valid URL
	"""
	pass



class URL():

	def __init__(self, urlstring):
		obj = urlparse(urlstring)
		#ParseResult(scheme='http', netloc='google.com', path='', params='', query='', fragment='')
		#ParseResult(scheme='http', netloc='google.com', path='/rss', params='', query='g=fugly', fragment='')
		#ParseResult(scheme='http', netloc='google.com:8080', path='/rss', params='', query='g=fugly', fragment='')
		#NOTE: FTP IS NOT SUPPORTED YET
		#ParseResult(scheme='ftp', netloc='username:password@google.com', path='/pub/mirror/x', params='', query='', fragment='')

		if obj.scheme and obj.netloc:
			if ':' in obj.netloc:
				(host,port)=obj.netloc.split(':')
				self.netloc = host
				#TODO: validate this!!!!
				self.port = int(port)
			else:
				self.netloc = obj.netloc
				self.port = 80

			if not self.is_ip(self.netloc) and not self.is_hostname(self.netloc):
				raise InvalidURL

		self.scheme = obj.scheme
		self.path = obj.path
		self.params = obj.params
		self.query = obj.query
		self.fragment = obj.fragment


	def is_ip(self,target):
		"""
		returns false if target is not a valid IP address
		"""
		try:
			ipaddress.ip_address(unicode(target))
		except ipaddress.AddressValueError:
			return False
		except ValueError:
			return False
		return True


	def is_hostname(self,target):
		"""
		returns false if target is not resolvable 
		"""
		try:
			addr = gethostbyname( target )
		except socket.gaierror:
			return False
		return True
			

	def __repr__(self):
		if self.port:
			if not self.query:
				return "%s://%s:%d%s" % (self.scheme,self.netloc,self.port,self.path)
			return "%s://%s:%d%s?%s" % (self.scheme,self.netloc,self.port,self.path,self.query)
		else:
			if not self.query:
				return "%s://%s%s" % (self.scheme,self.netloc,self.path)
			return "%s://%s%s?%s" % (self.scheme,self.netloc,self.path,self.query)
	


if __name__ == '__main__':
	"""
	testing of URL class
	"""
	url = URL("http://google.com")
	url2 = URL("http://google.com/rss?g=fugly")
	url3 = URL("http://google.com:8080/rss?g=fugly&dingos=fluffy")
	#url4 = URL("ftp://username:password@google.com/pub/mirror/x")

	print url
	print url2
	print url3

				
'''___EOF___'''
