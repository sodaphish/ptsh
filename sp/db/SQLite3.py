# -*- coding: utf-8 -*-
"""
@author: SodaPhish <sodaphish@protonmail.ch>
"""

import sys

try:
    from sp.base import Exceptions
except:
    print "Install sp into sys.path()"
    sys.exit(2)
    

class Connect():

    def __init__(self,**dsn):
        pass
    
    def select_sql(self):
        pass
    
    def insert_sql(self):
        pass
    
    def update_sql(self):
        pass
    
    def get_cursor(self):
        pass

    def db_init( self, schema ):
        """
        function to initialize a database's table(s) in the event they have not already been initialized.
        
        schema here is the XML schema, filename, or open file handle, which gets turned into a DBSchema object
        """
        #TODO: initialize the database schema
        try: 
            pass
        except:
            raise Exceptions.ConfigFault("Couldn't initialize database")
    
    
    def db_checkinit(self, schema ):
        """
        function to check whether or not a database has been initizlized or not.
        """
        #TODO check if table structure matches the schema defined for the table.
        pass



#EOF