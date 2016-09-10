class KeywordSet():
	keywords=None
	query=None
	
	def __init__(self, words=()):
		""" an object with keywords 
		"""
		self.keywords=list()
		for w in words:
			self.keywords.append( w )
		self.query=self.get_query()

	def append(self,kw):
		""" add a keyword to the list
		"""
		if kw not in self.keywords:
			self.keywords.append(kw)
			return True
		else:
			return False

	def remove(self,kw):
		""" remove a keyword from the list
		"""
		pass

	def get_query(self):
		""" output an squl query that represents the keyword set
		"""
		if len(self.keywords) >= 1:
			query = """SELECT feedentryid, keyword FROM keywords WHERE (keyword is '%s'"""%(self.keywords[0])
			for word in self.keywords[1:]:
				query = "%s or keyword is '%s'"%(query, word)
			query = "%s) order by feedentryid DESC"%(query)
			return query
		else:
			return False

	def __repr__(self):
		""" alias for self.get_query()
		"""
		return str(self.get_query())


if __name__ == '__main__':
	set1 = KeywordSet()
	set2 = KeywordSet( ('3g', '4g', 'verizon', 'android', 'iphone', 'ios', 'at&t', 't-mobile') )

	print set1
	set1.append('Linux')
	print set1
	print set2
