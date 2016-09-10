import semfeed
import os
import sys
import sqlite3
import string
import getopt

__version__ = "0.1.0"

class Keywords():
	db_con = None

	def __init__(self,dbfile):
		if not os.path.exists(dbfile):
			try:
				fh=open(dbfile,'w')
				fh.close()
			except:
				raise
		if os.path.exists(dbfile):
			try:
				self.db_con = sqlite3.connect(dbfile)
				self._db_init()
			except sqlite3.Error, e:
				raise sqlite3.Error, e
		else:
			raise os.error, "can't open database file"


	def _db_init(self):
		if isinstance(self.db_con, sqlite3.Connection):
			try:
				db_cur = self.db_con.cursor()
				db_cur.executescript("""
					BEGIN TRANSACTION;
					CREATE TABLE IF NOT EXISTS "feed" ( "feedid" INTEGER PRIMARY KEY AUTOINCREMENT, "feedurl" TEXT UNIQUE NOT NULL );
					CREATE TABLE IF NOT EXISTS "feedentry" ( "feedentryid" INTEGER PRIMARY KEY AUTOINCREMENT, "feedid" INTEGER NOT NULL, "feedurl" TEXT NOT NULL UNIQUE, "feedtitle" TEXT NOT NULL, "feedbody" TEXT NOT NULL, "feedauthor" TEXT NOT NULL, "feeddate" TEXT NOT NULL );
					CREATE TABLE IF NOT EXISTS "keywords" ( "feedentryid" INTEGER NOT NULL, "keyword" TEXT NOT NULL, "confidence" REAL NOT NULL );
					COMMIT;
				""")
				db_cur.close()
				self.db_con.commit()
			except:
				raise
		else:
			raise sqlite3.Error, "database connection error!"


	def get_keyword(self,keyword=None,conf=0):
		query=""
		if keyword is not None:
			# we watnt to query a specific keyword
			query="""SELECT keyword, confidence FROM keywords WHERE keyword LIKE '%s'"""%(keyword)
		else: 
		# get all keywords
			query="""SELECT keyword, confidence FROM keywords"""

		try:
			db_cur = self.db_con.cursor()
			result=db_cur.execute(query)
			for kw,con in result:
				print str(con), str(kw)
			db_cur.close()
		except sqlite3.Error, e:
			print e[0]
		except UnicodeEncodeError:
			pass
