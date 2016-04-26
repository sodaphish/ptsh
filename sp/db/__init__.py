from Global import cfg
import xml
__all__ = []

import sys

try:
    from sp.base import Exceptions
except:
    print "Install sp into sys.path()"
    sys.exit(2)


"""
Verify that the configuration file is defined and that our database type is defined.
"""
try: cfg
except NameError:
    print "configuration file not defined as 'cfg'"
    sys.exit(1)
try: cfg.get_value('db.type')
except Exception as e:
    print "database type not defined in configuration file"
    sys.exit(1)



def db_init( db, schema ):
    """
    function to initialize a database's table(s) in the event they have not already been initialized.
    """
    #TODO: initialize the database schema
    if cfg.get_value('db.type') == 'mysql':
        # initializing a MySQL database
        pass
    elif cfg.get_value('db.type') == 'sqlite3':
        # initializing a sqlite3 database
        pass
    else:
        raise Exceptions.ConfigFault("unknown database type")
    pass



def db_checkinit(db, schema ):
    """
    function to check whether or not a database has been initizlized or not.
    """
    #TODO check if table structure matches the schema
    pass



"""__EOF__"""