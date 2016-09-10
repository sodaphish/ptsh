import sqlite3, os, sys

class Registry:




	dbHandle = None
	dbCursor = None




	def __init__( self, dbfile='registry.db' ):
		"""__init__
		Constructor for the Registry class.
		"""
		if os.path.exists( dbfile ):
			self.dbHandle = sqlite3.connect( dbfile )
		else:
			self.dbHandle = sqlite3.connect( dbfile )
			self.dbCursor = self.dbHandle.cursor()
			self.dbCursor.execute( '''create table if not exists registry ( regkey text(128) not null, regval text not null, primary key(regkey), unique(regkey) )''' )
			self.dbCursor.execute( '''insert into registry ( regkey, regval ) values ( 'root.sanityCheck', '1' )''' )
		self.dbCursor = self.dbHandle.cursor()




	def __del__( self ):
		self.dbHandle.commit()




	def get( self, regkey ):
		"""get()
		retrieves a variable from the database and returns it
		"""
		r = self.dbCursor.execute( '''select regval from registry where regkey='%s' limit 1''' % ( regkey ) ) 
		for row in r:
			return row[0]




	def set( self, regkey, regval ):
		if self.get( regkey ):
			self.dbCursor.execute( '''update registry set regval='%s' where regkey='%s' ''' % ( regval, regkey ) )
		else:
			self.dbCursor.execute( '''insert into registry ( regkey, regval ) values ( '%s', '%s' )''' % ( regkey, regval ) )
		self.dbHandle.commit()
		return True




	def delkey( self, regkey ):
		if self.get( regkey ):
			self.dbCursor.execute( '''delete from registry where regkey='%s' '''  % ( regkey ) )
			return True
		else:
			return False




	def getScope( self, scope ):
		res = self.dbCursor.execute( '''select regkey, regval from registry where regkey like '%s%%' ''' % ( scope ) )
		results = []
		for row in res:
			results[row[0]]=row[1]
		return results




'''end Registry'''
