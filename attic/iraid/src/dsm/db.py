"""
This library contains a light-weight ORM and abstraction-layer to allow
database calls to be standardized across the DSM suite.

NOTES:
CJS(2011/03/18): I briefly considered using an existing/mature ORM like 
    SQLalchemy, but they contain so much we don't/won't need and would require 
    a significant investment in learning, that it seem(ed) faster to write our 
    own than to implement theirs.
    
"""
import dsm

class DBError(Exception):
    value = None
    type = None
    TYPES = {
            'unspecified': 'an unspecified error occurred',
            'connection-type': 'the connection-type specified is unknown or unsupported',
            'connection': 'error occurred while connecting to the database',
            'query':'an error occurred while executing a select/insert/update',
            'result':'an error occurred fetching the results of a query',
            }

    def __init__(self, type = 'unspecified', value = None):
        if self.ERRORS[type]:
            self.type = type
            if value is None:
                self.value = self.ERRORS[type]
            else:
                self.value = value
        else:
            self.value = value

    def __str__(self):
        return repr(self.value)



class DBConn():
    _dbtype = None
    _dbconn = None
    _dbuser = None
    _dbpass = None
    _dbhost = None
    _dbport = None

    def __init__(self, type, **kwargs):
        if type is 'sqlite3':
            #handle sqlite3 connection strings
            # requires: filename
            self._dbtype = 'sqlite3'
        elif type is 'mysql':
            #handle mysql connection strings
            # requires: host/socket, username, password, and DB name
            self._dbtype = 'mysql'
        else:
            # raise an error because this is an unsupported database
            self._dbtype = None
            raise DBError('connection-type')


class Query():
    """class to sanitize, execute and return database commands
    """
    _type = None
    QUERY_TYPES = ('select', 'insert', 'update', 'raw')

    def __init__(self, type, **kwargs):
        if type in self.QUERY_TYPES:
            self._type = type
        else:
            raise DBError('query')

    def execute(self):
        if self._type is 'select':
            self._select()
        elif self._type is 'insert':
            self._insert()
        elif self._type is 'update':
            self._update()
        elif self.type is 'raw':
            self._raw()
        else:
            raise DBError('query')

    def _validate(self):
        pass

    def _sanitize(self):
        """method to sanitize query input to ensure that it kosher
        """
        pass

    def _select(self):
        pass

    def _insert(self):
        pass

    def _update(self):
        pass

    def _raw(self):
        """send a free-form SQL command to the server."""
        pass

    def _iter_rows(self):
        pass

class Table():
    """type for handling the creation of 
    """
    _dbtype = None
    name = None

    def __init__(self):
        pass
