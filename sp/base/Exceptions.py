


class Generic(Exception):
	pass


class ConfigFault(Exception):
	"""
	Fault in configuration file syntax/formatting.	
	"""
	pass



class DatabaseConnectError(Exception):
	"""
	database connection error
	"""
	pass



class DatabaseError(Exception):
	"""
	generic database error
	"""
	pass


class FileAccessError(Exception):
    """
    Error accessing a file
    """
    pass

