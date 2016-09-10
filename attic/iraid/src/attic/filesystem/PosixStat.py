"""
PosixStat

class to handle stat on POSIX compliant systems.  we'll probably 
have a Win32Stat class at some point if one doesn't already exist.
"""
import stat

class PosixStat():
	"""class to handle stat on POSIX compliant systems.  we'll probably 
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
		self.update(posix_stat)

	def update(self,posix_stat):
		"""convenience function to update my internal stat data
		"""
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
		"""convenience function to interface with stat data
		"""
		self.__mode=mode


	def __update_ino(self,ino=None):
		"""convenience function to interface with stat data
		"""
		self.__ino=ino


	def __update_dev(self,dev=None):
		"""convenience function to interface with stat data
		"""
		self.__dev=dev


	def __update_nlink(self,nlink=None):
		"""convenience function to interface with stat data
		"""
		self.__nlink=nlink


	def __update_uid(self,uid=None):
		"""convenience function to interface with stat data
		"""
		self.__uid=uid


	def __update_gid(self,gid=None):
		"""convenience function to interface with stat data
		"""
		self.__gid=gid


	def __update_size(self,size=None):
		"""convenience function to interface with stat data
		"""
		self.__size=size


	def __update_atime(self,atime=None):
		"""convenience function to interface with stat data
		"""
		self.__atime=atime


	def __update_mtime(self,mtime=None):
		"""convenience function to interface with stat data
		"""
		self.__mtime=mtime


	def __update_ctime(self,ctime=None):
		"""convenience function to interface with stat data
		"""
		self.__ctime=ctime


	def __repr__(self):
		return self.__raw_stat

	def dump(self):
		return "%s" % (self.__raw_stat)
