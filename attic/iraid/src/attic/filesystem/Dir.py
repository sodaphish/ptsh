"""
Dir.py - by C.J. Steele <corey@hostedbycorey.com>
(C)opyright 2011, Corey J. Steele, all rights reserved.

Dir
This object is creates a list of File objects, and allows for the 
addition, removal, etc., of such file objects.
"""
import os
from dsm.filesystem.File import File

class Dir():
	__rootdir = None
	__files = []

	def __init__(self,rootdir=None):
		"""parses rootdir and populates self.__files with File objects for 
		every file in the dir
		"""
		if os.path.exists(rootdir):
			self.__rootdir=rootdir
			self.add_dir(rootdir)
		else:
			pass


	def __repr__(self):
		"""over-loads string representation of the file parts.
		"""
		for f in self.__files:
			print "%s" % (f)


	def __get_files(self,directory=None):
		"""uses os.walk to pull the files out of dir, creating a File object for each file.
		"""
		for root,dirs,filelist in os.walk(directory):
			for files in filelist:
				filename="%s%s%s" % (root,os.sep,files)
				try:
					self.add_file(filename)
				except:
					#TODO:fix this so it handles the exception gracefully
					pass
		return True


	def add_file(self,filename):
		"""routine to add a file to the Dir
		"""
		if os.path.exists(filename):
			self.__files.append(File(filename))
		else:
			raise(os.Error)


	def add_dir(self,dirname):
		""" alias routine to handle reading files from a directory
		"""
		if os.path.exists(dirname):
			self.__get_files(dirname)
		else:
			raise(os.Error)


	def rm_dir(self,dirname):
		""" function to remove all the files in a directory from the fileset
		"""
		for root,dirs,filelist in os.walk(dirname):
			for files in filelist:
				fn="%s%s%s" % (root,os.sep,files)
				#TODO: check success or failure, handle accordingly
				self.rm_file(fn)
		return True


	def rm_file(self,filename):
		"""function to remove a file from the fileset
		"""
		return self.__files.remove('filename')
		return False


	def verify(self):
		"""function to go through all the __files in the directory and make sure they all exist in the __rootdir, and vice versa
		"""


	def fullVerify(self):
		"""same as verify, but also validates the checksums of each file as it goes.
		"""


	def __eq__(self,target):
		"""comparison operator to determine equality between two Dir objects -- only checks that the entries in __files are the same.
		"""
		pass


	def __ne__(self,target):
		"""niceity function that relies on __eq__
		"""
		pass
