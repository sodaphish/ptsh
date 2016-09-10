""" DSM DataStore - Data Storage Model (DSM) DataStore class & function library

Classes and fucntions related to supporting our internal datastore


NOTE: __schema_version__ is an integer representation of the version 
	number.  e.g. a version of 1.3.5 = a schema version of 135, 
	v0.0.1 = 1

"""
__version__ = "0.0.1"
__schema_version__ = 1


import os
import sqlite3
import uuid
from dsm.filesystem import * 


class StoreError(Exception):
	def __init__(self,value):
		self.value=value
	def __str__(self):
		return repr(self.value)


class File(File):
	_fid = None

	def _mkid(self):
		""" generates a UUID for the file and sets the hex value to self._fid
		"""
		pass:


class Store():

	_dbhandle = None
	_dbcursor = None
	_dbfile = None
	_schema_version = None
	_rootdir = None


	def __init__(self,dbfile,rootdir):
		"""constructor for the Store class"""
		"""has two modes: initialize the sqlite db, and refresh an existing datastore."""
		if os.path.exists(dbfile) and os.access(self._dbfile,os.W_OK):
			self._dbfile = dbfile
			try:
				self._dbhandle = sqlite3.connect('dbfile')
				self._dbcursor = self._dbhandle.cursor()
			except sqlite3.Error, e:
				raise StoreError(e.args[0])
		else:
			if os.path.exists(dbfile):
				raise StoreError('Not Writeable')
			else:
				raise StoreError('Database Initialization Error')


	def _init_db(self):
		"""_init_db() -> creates the table structure in the database if it isn't already, TODO: handle automatic updating """
		if self._schemaver():
			# db is already set, skip initialization
		else:
			if type(self._dbcursor) is 'sqlite3.Cursor' and self._schemavar() is not None:
				try:
	 				#create the config table
					self._dbcursor.execute('''create table config ( key text(128) not null,value text not null, primary key(key),unique(key) )''')
					#create the files table
					self._dbcursor.execute('''create table files ( fid text(32) not null, filename,checksum text(32) not null, stat  )''')
					#set our schema value
					self._dbcursor.execute('''insert into config ( key,value ) values ( ?,? )''', ('schema_ver',dsm.datastore.__schema_version__))
					#set our rootdir
					self._dbcursor.execute('''insert into config ( key,value ) values ( ?,? )''', ('rootdir',self._rootdir))
				except sqlite3.Error, e:
					raise StoreError(e.args[0])
			else:
				raise StoreError('invalid database connection')


	def _schemaver(self,schemaver=None):
		"""_schemaver() -> get or set version of database schema"""
		"""if an argument is passed, we'll set the schemavar in the database to the value of that argument"""
		"""IMPORTANT: when setting schemavar, it cannot be different than dsm.datastore.__schema_version__"""
		if type(self._dbcursor) is 'sqlite3.Cursor':
			if schemavar:
				if schemavar is dsm.datastore.__schema_version__:
					try:
						self._dbcursor.execute('''update config set value=? where key=? ''', (schemavar,'schema_ver'))
					except sqlite3.Error,e:
						raise StoreError(e.args[0])
				else:
					pass
					#TODO: hook to upgrade the schema
			else:
				# select the ver from our schema... 
				try:
					self._dbcursor.execute('''select value from config where key=?''', ('schema_var'))
					(self._schema_version)=self._dbcursor.fetchone()
					if self._schema_version is not None:
						return True
					else:
						raise StoreError('malformed schema in database')
				except sqlite3.Error, e:
					raise StoreError(e.args[0])
		else:
			raise StoreError('invalid database connection')



	def config_get(self,keyname):
		""" fetches keyname from the db, if the value isn't present it raises 
			an Exception.
		"""
		pass


	def config_set(self,keyname,value):
		""" checks first to see if keyname already is in db, and if it is it 
			updates, otherwise it sets.  if any errors are encountered, raises 
			an exception
		"""
		pass


	def fetch_uuid(self,fullfilename):
		""" queries the database for a file matching the fullfilename and 
			returns the fid of that file if one is found, if none is found,
			it raises an Exception
		"""
		pass


	def _add_file(self,f):
		""" adds a file to the datastore, first verifying that it isn't 
			already in the datastore -- takes argument of type File
		"""
		if fetch_uuid( ) is None:
			return True
		return False


	def _rm_file(self,fid):
		""" removes a files from the database, checks first to ensure its not on 
			the disk, if it is, it raises an exception
		""" 
		pass


	def _update_file(self,fid):
		""" deletes a file from teh datastore, then adds it back with the updated 
			values
		"""
		pass


	def _verify_file(self,fid):
		""" performs quick verification process on an individual file, returns a 
			boolean value, takes a UUID which is looked-up in the file database, 
			and checks c/m times on the file vs what's in the database
		"""
		pass


	def _fullverify_file(self,fid):
		""" performs a full verification process on an individual file, returns a 
			boolean value, takes a UUID which is looked-up in the file database,
			and generates a new checksum of the file as it lives on disk and 
			compares that to the checksum on the database; raises an exception on 
			failure of checksum
		"""
		pass


	def verify(self):
		""" performs a quick verification of the entire store, i.e. walks the 
			files in the file table and checks them with self._verify_file, 
			raises an exception if _verify_file fails
		"""
		pass


	def fullverify(self):
		""" goes through and does a full check of the database contents AND the filesystem...
		"""
		pass


	def mkmanifest(self):
		""" creates an XML manifest to be provided to the Broker, takes no 
			arguments and raises an error on failure, returns an object of type 
			Manifest, or None in the event of a failure
		"""
		pass


	#TODO: write a schema upgrade routine to allow for database schemas to be updated on the fly
	#  NOTE: This is going to suck complete anus
