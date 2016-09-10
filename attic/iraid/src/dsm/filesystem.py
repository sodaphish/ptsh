__version__ = "0.0.1"



"""
PosixStat

class to handle stat on POSIX compliant systems.  we'll probably 
have a Win32Stat class at some point if one doesn't already exist.
"""
import dsm
import stat
import os
import hashlib


class PosixStat():
	"""PosixStat class """
	"""to handle stat on POSIX compliant systems.  we'll probably 
	have a Win32Stat class at some point if one doesn't already exist.
	"""
	__raw_stat = None
	__mode = None
	__ino = None
	__dev = None
	__nlink = None
	__uid = None
	__gid = None
	__size = None
	__atime = None
	__mtime = None
	__ctime = None

	def __init__(self,posix_stat=None):
		"""instantiation of posix stat class, really an alias for update()"""
		self.update(posix_stat)

	def update(self,posix_stat):
		"""update( [10]) -> updates the ten stat objects"""
		"""public method to update the stat() of a file"""
		if posix_stat:
			self.__raw_stat = posix_stat
			self.__update_mode(posix_stat[stat.ST_MODE])
			self.__update_ino(posix_stat[stat.ST_INO])
			self.__update_dev(posix_stat[stat.ST_DEV])
			self.__update_nlink(posix_stat[stat.ST_NLINK])
			self.__update_uid(posix_stat[stat.ST_UID])
			self.__update_gid(posix_stat[stat.ST_GID])
			self.__update_size(posix_stat[stat.ST_SIZE])
			self.__update_atime(posix_stat[stat.ST_ATIME])
			self.__update_mtime(posix_stat[stat.ST_MTIME])
			self.__update_ctime(posix_stat[stat.ST_CTIME])


	def __update_mode(self,mode=None):
		"""convenience function to interface with stat data"""
		self.__mode=mode


	def __update_ino(self,ino=None):
		"""convenience function to interface with stat data"""
		self.__ino=ino


	def __update_dev(self,dev=None):
		"""convenience function to interface with stat data"""
		self.__dev=dev


	def __update_nlink(self,nlink=None):
		"""convenience function to interface with stat data"""
		self.__nlink=nlink


	def __update_uid(self,uid=None):
		"""convenience function to interface with stat data"""
		self.__uid=uid


	def __update_gid(self,gid=None):
		"""convenience function to interface with stat data"""
		self.__gid=gid


	def __update_size(self,size=None):
		"""convenience function to interface with stat data"""
		self.__size=size


	def __update_atime(self,atime=None):
		"""convenience function to interface with stat data"""
		self.__atime=atime


	def __update_mtime(self,mtime=None):
		"""convenience function to interface with stat data"""
		self.__mtime=mtime


	def __update_ctime(self,ctime=None):
		"""convenience function to interface with stat data"""
		self.__ctime=ctime


	def __repr__(self):
		return self.__raw_stat

	def dump(self):
		return "%s" % (self.__raw_stat)





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
		"""returns the checksum as a hex digest
		"""
		if self.__checksum:
			return self.__checksum
		else:
			return False





class File(FileBase):
	__stat = None

	def __init__(self,filename):
		if os.path.exists(filename):
			pt,fn = os.path.split(filename)
			self.set_path(pt)
			self.set_name(fn)
			self._checksum()
			self.__stat = PosixStat()
			self.__stat.update(os.stat(self.get_fullname()))
		else:
			#TODO: fix this -- should raise an error
			return False

	def get_stat(self):
		return self.__stat.dump()





class Dir():
	__rootdir = None
	__files = None

	def __init__(self,rootdir=None):
		"""parses rootdir and populates self.__files with File objects for 
		every file in the dir
		"""
		if os.path.exists(rootdir):
			self.__rootdir=rootdir
			self.__files = list()
			self.add_dir(rootdir)
		else:
			raise os.error, "path not found"


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
					raise
					
		return True


	def add_file(self,filename):
		"""routine to add a file to the Dir
		"""
		filename=os.path.normpath(filename)
		if os.path.exists(filename):
			if dsm.__DEBUG__:
				print "adding file to dir: %s" % (filename)
			self.__files.append(File(filename))
		else:
			raise(os.error,"cannot find %s" % filename)


	def add_dir(self,dirname):
		""" alias routine to handle reading files from a directory
		"""
		if os.path.exists(dirname):
			self.__get_files(dirname)
		else:
			raise os.error, "path not found"


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
		return self.__files.remove(filename)


	def quickverify(self):
		"""function to go through all the __files in the directory and make sure they all exist in the __rootdir, and vice versa
		"""
		pass


	def verify(self):
		"""same as quickverify, but also checks the checksum hash of each file -- this should only be used with extreme cauction
		"""
		pass


	def __eq__(self,target):
		"""comparison operator to determine equality between two Dir objects -- only checks that the entries in __files are the same.
				this will ultimately entail that the File objects within the __files list share the same hash checksum, this function should be surprisingly quick
		"""
		pass


	def __ne__(self,target):
		"""niceity function that relies on __eq__
		"""
		pass
