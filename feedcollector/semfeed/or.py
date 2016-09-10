"""
basic Object Relational Mapper (ORM) -- classes to handle database relation management
"""

class Type:

	TYPE={}
	
	def __init__(self):
		pass

class Column:
	col_name = None
	col_type = None

	def __init__(self,name,type):
		pass


class Row:
	pass


class Database:
	db_type = None
	db_dsn = None

	def __init__(self, db_type='sqlite', db_dsn=None):
		pass


class Table:
	pass


class Query:
	pass

