#!/usr/bin/python
"""
(C)opyright 2011, C.J. Steele, all rights reserved.

feedCollector - utility for adding, removing, listing, and processing feeds

processing feeds consists of getting the actual feed, from the Internet,
and for each entry going through and inserting it to the database (if it 
isn't already) there, and gets the tags for the entry and inserts those 
into the database.  

TODO: 
** there are still some posts which do not get a timestamp -- try processing date stamps into a valid date object before writing it to the database
** implement logging so we can log what we're doing

CHANGES:
** 0.1.6 -- fixed poorly formed feed issues (I have a sneeking suspicion this is not the last rev b/c poorly formed feeds.
** 0.1.4 -- fixed unicode character support because urllib.urlencode() is fuckt
** 0.1.2 -- fixed a "failure to commit" error in the command-line
** 0.1.0 -- first rev, it has all the basic features
"""

__version__ = "0.1.6"

import semfeed

try:
	import os
	import sys
	import sqlite3
	import urllib
	import simplejson 
	import feedparser
	import string
	import getopt
	from BeautifulSoup import BeautifulSoup
except:
	sys.stderr.write("Error! Failed to all needed dependencies...")
	sys.exit(1)
	

def sanitize(mangledtext):
	if len(mangledtext.split()) > 1:
		mangledtext=''.join(BeautifulSoup(mangledtext).findAll(text=True))
		mangledtext=string.replace(mangledtext,"\'", "&#39;")
		mangledtext=string.replace(mangledtext,"\"", "&#34;")
	else:
		mangledtext=string.replace(mangledtext,"\'", "&#39;")
	return mangledtext
	

class Collector():
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


	def add_feed(self,feedurl):
		if isinstance(self.db_con, sqlite3.Connection):
			try:
				db_cur = self.db_con.cursor()
				db_cur.execute("insert into feed (feedurl) values ('%s')"%(feedurl))
				db_cur.close()
				self.db_con.commit()
			except sqlite3.Error, e:
				raise sqlite3.Error, e
			print "successfully added %s"%(feedurl)
		else:
			raise sqlite3.Error, "database connection error!"


	def remove_feed(self,feedurl):
		if isinstance(self.db_con, sqlite3.Connection):
			try:
				db_cur = self.db_con.cursor()
				db_cur.execute("delete from feed where feedurl='%s'"%(feedurl))
				db_cur.close()
				self.db_con.commit()
			except sqlite3.Error, e:
				raise sqlite3.Error, e
		else:
			raise sqlite3.Error, "database connection error!"


	def list_feeds(self):
		if isinstance(self.db_con, sqlite3.Connection):
			try:
				db_cur = self.db_con.cursor()
				query = db_cur.execute('''select feedid, feedurl from feed''')
				print "feedid,feedurl"
				for (feedid,feedurl) in query:
					print "%d,%s"%(feedid,feedurl)
				db_cur.close()
			except sqlite3.Error, e:
				raise sqlite3.Error, e
		else:
			raise sqlite3.Error, "database connection error!"


	def proc_feed(self,fid,furl):
		if isinstance(self.db_con, sqlite3.Connection):

			# setup our db_cur
			try:
				db_cur=self.db_con.cursor()
			except:
				raise sqlite3.Error, "couldn't create cursor"

			# parse the feed
			try:
				feed=feedparser.parse(urllib.urlopen(furl))
			except UnicodeEncodeError,e:
				pass
			except:
				raise Exception, "failed to parse feed"

			# process the entries within the feed
			for e in feed['entries']:
				isunique=True

				if "updated" in e:
					entry_date=sanitize(e['updated'])
				elif "published" in e:
					entry_date=sanitize(e['published'])
				elif "created" in e:
					entry_date=sanitize(e['created'])
				else:
					# honestly, who the hell is rolling out their own feeds with such shit-poor formed structures?
					entry_date=""

				if "author" in e:
					entry_author=sanitize(e['author'])
				elif "contributor" in e:
					entry_author=sanitize(e['contributor'][0]['value'])
				elif "publisher" in e:
					entry_author=sanitize(e['publisher'])
				else:
					entry_author="unattributable"

				entry_title=sanitize(e['title'])
				if "summary" in e:
					entry_body=sanitize(e['summary'])
				elif "content" in e:
					entry_body=sanitize(e['content'][0]['value'])
				if len(entry_body) >= 512:
					entry_body=entry_body[:509]+"..."
				entry_link=e['link']
				
				lastid=None
				# insert the entry into our database
				try:
					stmt="""insert into feedentry (feedid,feedurl,feedtitle,feedbody,feedauthor,feeddate) values ( %d,'%s','%s','%s','%s','%s')"""%(fid,entry_link,entry_title,entry_body,entry_author,entry_date)
					entry_insert=db_cur.execute(stmt)
					self.db_con.commit()
					lastid=db_cur.lastrowid
				except sqlite3.IntegrityError, e:
					if e[0][:6] is "column":
						isunique=False
				except sqlite3.Error, e:
					raise sqlite3.Error, e

				if isunique is True and lastid is not None:
					#get our keywords from zemanta
					try:
						gateway = 'http://api.zemanta.com/services/rest/0.0/'
						zemantatext = "%s %s"%(entry_title,entry_body)
						zemantatext_fixed = filter(lambda x: x in string.printable, zemantatext)
						args = { 'method': 'zemanta.suggest', 'api_key': 'a93c9cwt8fkrc5dyfne2hw82', 'text': zemantatext_fixed, 'format': 'json' }
						args_enc = urllib.urlencode(args)
						response_raw = urllib.urlopen(gateway, args_enc).read()
						response = simplejson.loads(response_raw)
					except:
						raise

					# insert the keywords into the database
					for tag in response['keywords']:
						try: 
							keyword=sanitize(tag['name'])
							confidence=tag['confidence']
							stmt="""insert into keywords (feedentryid, keyword, confidence) values (%d, '%s', %f)"""%(lastid,keyword,confidence)
							keyword_insert=db_cur.execute(stmt)
						except sqlite3.Error, e:
							raise sqlite3.Error, e
					self.db_con.commit()

		else:
			raise sqlite3.Error, "database connection error!"


	def proc_allfeeds(self):
		if isinstance(self.db_con, sqlite3.Connection):
			try:
				db_cur = self.db_con.cursor()
				query = db_cur.execute('''select feedid, feedurl from feed''')
				for (feedid,feedurl) in query:
					self.proc_feed(feedid,feedurl)
				db_cur.close()
			except:
				raise
		else:
			raise sqlite3.Error, "database connection error!"


def usage():
	print sys.argv[0], "v.", __version__
	print "(c)opyright 2011, C.J. Steele, all rights reserved"
	print ""
	print "usage:", sys.argv[0], " [-(a|r) [feedurl]] [-l] [-h] [-d database]"
	print ""
	print "  -a,--add    [feedurl] - add a feed"
	print "  -r,--remove [feedurl] - remove a feed"
	print "  -l,--list             - list feeds"
	print "  -d,--database [file]  - file/path to the database"
	print "  -h,--help             - this message"
	print ""
	print "if no argument is specified,", sys.argv[0],"will connect to"
	print "the Internet and download feeds and process them."
	print ""


if __name__=='__main__':
	database = 'feeds.db'
	col=None

	try:
		opts, args = getopt.getopt(sys.argv[1:], "hla:r:d:", ["help", "list", "add=","remove=","database="])
	except getopt.GetoptError, e:
		print str(e)
		usage()
		sys.exit(2)

	for o, a in opts:
		if o in ("-h", "--help"):
			usage()
			sys.exit()
		elif o in ("-d", "--database"):
			database=a
		elif o in ("-l", "--list"):
			col=Collector(database)
			col.list_feeds()
			sys.exit()
		elif o in ("-a", "--add"):
			col=Collector(database)
			col.add_feed(a)
			sys.exit()
		elif o in ("-r", "--remove"):
			col=Collector(database)
			col.remove_feed(a)
			sys.exit()
	
	# if we haven't exited yet, we're just going to happily run our processing routine
	col=Collector(database)
	col.proc_allfeeds()
