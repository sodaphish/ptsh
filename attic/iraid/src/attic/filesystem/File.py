"""
DSMMetaFile Class

Class to extend the DSMFile foundation class to support meta data across multiple OS-es.  
"""
import os,stat,pickle
from dsm.filesystem.FileBase import FileBase
from dsm.filesystem.PosixStat import PosixStat

class File(FileBase):
	__stat = PosixStat()

	def __init__(self,filename):
		if os.path.exists(filename):
			pt,fn = os.path.split(filename)
			self.set_path(pt)
			self.set_name(fn)
			self._checksum()
			self.__stat.update(os.stat(self.get_fullname()))
		else:
			#TODO: fix this -- should raise an error
			return False

	def get_stat(self):
		return self.__stat.dump()
