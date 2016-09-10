"""
File Class

This class provides a basic framework for working with files in DSM.
"""
import os
import hashlib

class FileBase():
	__path = None
	__name = None
	__checksum = None

	def __init__(self, filename=None):
		"""constructor for the File class
		"""
		if os.path.exists(filename):
			try:
				pt,fn = os.path.split(filename)
				self.set_path(pt)
				self.set_name(fn)
				self._checksum()
			except:
				#TODO: fixme
				pass
		else:
			#TODO: raise an exception
			self.__path = None
			self.__name = None


	def get_path(self):
		"""function to return just the name of path of the file
		"""
		if os.path.exists(self.__path):
			return self.__path
		else:
			return None


	def get_name(self):
		"""function to return just the name of the file 
		"""
		if os.path.exists( "%s%s" % (self.__path,self.__name)):
			return self.__name
		else:
			return None


	def get_fullname(self):
		"""function to return just the name of the file 
		"""
		filename = "%s%s" % (self.__path,self.__name)
		if os.path.exists(filename):
			return str(filename)
		else:
			return None


	def __repr__(self):
		"""function to represent the File object
		"""
		return( str(self.get_fullname()) )


	def __eq__(self,target):
		"""function to test equality between two File objects
		"""
		if isinstance(target,File):
			if self.__checksum == target.get_checksum:
				return True
		return False


	def __ne__(self,target):
		"""function to test inequality between two File objects
		"""
		if self.__eq__(target):
			return False
		return True


	def set_path(self,path):
		"""function used to set the path of the object
		"""
		path = "%s%s" % (path,os.sep)
		if os.path.exists(path):
			self.__path = path
		else:
			raise OSError("path not found")


	def set_name(self,filename):
		"""function used to set the path of the object
		"""
		fullpath = "%s%s" % (self.__path,filename)
		if os.path.exists(fullpath):
			self.__name = filename 
		else:
			raise OSError("path not found")


	def _checksum(self):
		"""creates a hash of a file
		"""
		sha1 = hashlib.sha1()
		with open(self.get_fullname(),'rb') as f:
			for chunk in iter(lambda: f.read(sha1.block_size), ''):
				sha1.update(chunk)
		self.__checksum = sha1.hexdigest()


	def get_checksum(self):
		if self.__checksum:
			return self.__checksum
		else:
			return False
