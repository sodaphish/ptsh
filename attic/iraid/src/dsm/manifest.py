"""
Data Storage Model - Manifest Library

(c)opyright 2011, C.J. Steele, all rights reserved.

This module contains classes and routines for working with manifests of various sorts
"""
import dsm
from dsm.utility import *
import logging
import sqlite3


# major == Manifest version, Minor == Subscriber/Provider major version, patch == my internal version info
__version__ = Version(1, 0, 0)

class ManifestError(Exception):
	value = None

	def __init__(self, value):
		self.value = value

	def __str__(self):
		return repr(self.value)


class Manifest():
	dbfile = None
	rootdir = None
	_dbhandle = None
	_dbcursor = None
	version = None

	def __init__(self, dbfile):
		self._files = list()
		if not os.path.exists(dbfile):
			try:
				logging.debug('creating database file: ' + dbfile)
				dbf = open(dbfile, 'w')
				dbf.close()
			except:
				raise
		if os.path.exists(dbfile):
			try:
				self._dbhandle = sqlite3.connect(dbfile)
				logging.debug('connected to the database!')
				self._dbcursor = self._dbhandle.cursor()
				self._init_db()
				self.version = __version__
			except sqlite3.Error, e:
				logging.critical('DATABASE HERP DERP', e[0])
				raise
		else:
			logging.critical('could not locate database file ' + self.dbfile)
			raise os.error, 'database file canot be written to'


	def __destroy__(self):
		""" force pending writes to disk and close-down
		"""
		try:
			self._dbhandle.commit()
			self._dbhandle.close()
		except sqlite3.Error, e:
			raise sqlite3.Error, 'database shutdown error!'


	def get_schema_ver(self):
		#TODO: do we need to try/except this block?
		schema_maj = self.get_key('schema:major')
		logging.debug('VARIABLE: schema_maj=' + str(schema_maj))
		schema_min = self.get_key('schema:minor')
		logging.debug('VARIABLE: schema_min=' + str(schema_min))
		schema_pat = self.get_key('schema:patch')
		logging.debug('VARIABLE: schema_pat=' + str(schema_pat))
		if schema_maj is not None and schema_min is not None and schema_pat is not None:
			try:
				current_db_version = Version(schema_maj, schema_min, schema_pat)
				logging.debug('schema variables all populated, version on disk:' + current_db_version)
				return current_db_version
			except TypeError, e:
				logging.critical(e[0])
		return None


	def _init_db(self):
		# create our database tables
		cur_db_ver = self.get_schema_ver()
		logging.debug(cur_db_ver)
		if cur_db_ver != __version__:
			logging.warn('db version on disk is different than current code schema.  version on disk:' + cur_db_ver, +' current version:' + __version__)
		elif cur_db_ver is None:
			# cur_db_ver is undefined, so its a new database
			try:
				dbcursor = self._dbhandle.cursor()
				query = "CREATE TABLE IF NOT EXISTS config ( keyname text(256) NOT NULL, keyval TEXT(256) NOT NULL, UNIQUE(keyname), PRIMARY KEY(keyname) )"
				logging.debug('SQL_STMT: ' + query)
				dbcursor.execute(query)
				self._dbhandle.commit()
				logging.info('manifest initialized!')
			except sqlite3.OperationalError, e:
				logging.critical('database initialization failed with an operational error: ' + e[0])
				raise
			except sqlite3.Error, e:
				logging.critical('database initialization failed: ' + e[0])
				raise sqlite3.Error, e
		elif cur_db_ver == __version__:
			#our schema's match, no need to touch the database.
			pass


	def get_key(self, keyname):
		try:
			dbcursor = self._dbhandle.cursor()
			query = """SELECT keyname, keyval FROM config WHERE keyname = '%s'""" % (keyname)
			logging.debug('Fetching ' + keyname + '. SQL_STMT: ' + query)
			result = dbcursor.execute(query)
			(kn, kv) = result.fetchone()
			logging.debug('KEY QUERY RESULT:' + kn + ' ' + kv)
			return str(kv)
		except:
			# primary concern with this except is to sustain
			logging.warn(keyname + ' not found in CONFIG')
			return None


	def set_key(self, keyname, value):
		try:
			dbcursor = self._dbhandle.cursor()
			if self.get_key(keyname) is not None:
				#key already exists, update it
				query = '''UPDATE config SET keyval='%s' WHERE keyname='%s' ''' % (value, keyname)
				logging.debug('SQL_STMT: ' + query)
				dbcursor.execute(query)
				logging.debug(keyname + ' has been set to ' + str(value))
			else:
				#key doesn't exist, do insert
				query = '''INSERT INTO config (keyname,keyval) VALUES ('%s','%s')''' % (keyname, value)
				logging.debug('SQL_STMT: ' + query)
				dbcursor.execute(query)
				logging.debug(keyname + ' has been set to ' + self.get_key(keyname))
			self._dbhandle.commit()
		except sqlite3.OperationalError, e:
			logging.critical('malformed sql query: ' + e[0])
			raise
		except Exception, e:
			logging.critical('couldn\'t set key/value pair: ' + e[0])
			raise ManifestError, "couldn't set key/value pair"


class SubscriberManifest(Manifest):
	def _init_db(self):
		"""override the _init_db method to make sure the subscriber manifest creates the appropriate database scheme
		"""
		try:
			dbcursor = self._dbhandle.cursor()
			config_table_query = "CREATE TABLE IF NOT EXISTS config ( keyname text(256) NOT NULL, keyval TEXT(256) NOT NULL, UNIQUE(keyname), PRIMARY KEY(keyname) )"
			logging.debug('SQL_STMT: ' + config_table_query)
			dbcursor.execute(config_table_query)
			self._dbhandle.commit()
			file_table_query = "CREATE TABLE IF NOT EXISTS files( filename(512) not null, fid text(32) NOT NULL, checksum text(32) NOT NULL, UNIQUE(filename), UNIQUE(fid), PRIMARY KEY(fid) )"
			logging.debug('SQL_STMT: ' + file_table_query)
			dbcursor.execute(file_table_query)
			self._dbhandle.commit()
			self.set_key('schema.major', __version__.major)
			self.set_key('schema.minor', __version__.minor)
			self.set_key('schema:patch', __version__.patch)
			logging.info('manifest initialized!')
		except sqlite3.OperationalError, e:
			logging.critical('database initialization failed with an operational error: ' + e[0])
			raise
		except sqlite3.Error, e:
			logging.critical('database initialization failed: ' + e[0])
			raise sqlite3.Error, e


	def add_file(self, filename, fid, checksum):
		pass

	def remove_file(self, filename):
		pass

	def find_file(self, filename):
		pass

	def verify(self):
		pass

	def export(self, filename = None):
		pass



class ProviderManifest(Manifest):

	def _init_db(self):
		"""override the _init_db method to make sure the provider manifest creates the appropriate database scheme
		"""
		# fid, checksum, data
		dbcursor = self._dbhandle.cursor()
		dbcursor.execute('create table files( fid text(32) not null, checksum text(32) not null, data() not null, unique (fid), primary key(filename) )')
		self._dbhandle.commit()
		pass

	def add_file(self, fid, checksum, data):
		pass

	def remove_file(self, fid):
		pass

	def find_file(self, fid):
		pass

	def verify(self):
		pass

	def export(self, filename = None):
		pass
