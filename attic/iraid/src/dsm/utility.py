"""
utilities.py

A hodge-podge collection of utility functions and classes used for convenience.
"""

import os
import hashlib


def chks_file(filename=None):
	if os.path.exists(filename):
		sha1 = hashlib.sha1()
		with open(filename,'rb') as f:
			for chunk in iter(lambda: f.read(sha1.block_size), ''):
				sha1.update(chunk)
		return sha1.hexdigest()
	else:
		raise os.error, 'file not found(%s)'%(filename)


def chks_fid(fid=None,db=None):
	pass



class Version():
	major=None
	minor=None
	patch=None

	def __init__(self,major=0,minor=0,patch=0):
		if isinstance(major,int) and isinstance(minor,int) and isinstance(patch,int):
			self.major=major
			self.minor=minor
			self.patch=patch
		else:
			raise TypeError

	def __repr__(self):
		return "%d.%d.%d" % (self.major,self.minor,self.patch)

	def __eq__(self,target):
		if self.major == target.major and self.minor==target.minor and self.patch==target.patch:
			return True
		return False

	def __gt__(self,target):
		if type(target) is "Version":
			if self.major > target.major:
				return True
			if self.minor > target.minor:
				return True
			if self.patch > target.patch:
				return True
		return False


	def __lt__(self,target):
		if type(target) is "Version":
			if self.major < target.major:
				return True
			if self.minor < target.minor:
				return True
			if self.patch < target.patch:
				return True
		return False







#EOF
