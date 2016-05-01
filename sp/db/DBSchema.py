# -*- coding: utf-8 -*-
"""
@author: SodaPhish <sodaphish@protonmail.ch>
"""

import sys, re, os
from __builtin__ import str


try:
    from bs4 import BeautifulSoup
except ImportError:
    print "couldn't import BeautifulSoup!"
    sys.exit(2)

try:
    from sp.base import Exceptions
    from sp.base import Version
except:
    print "you need to install splib into sys.path()"
    sys.exit(2)
    
    
    

class DBSchema():
    """
    XML database schema abstraction class to read-in, write-out, and validate database schemas.
    
    Schemas look like this: 
        <database>
            <table name="User">
                <column name="username" type="text"></column>
                <column name="password" type="text"></column>
            </table>
        </database>
    
    Supported types are: text, float, int, real, timestamp.
    
    A default value for a column can be specified between <column> and </column>, e.g. <column name="lastmodified">NOW()</column>
    
    Options for a column are specified in the options="" field within a column definition, e.g. <column name="rowid" options="AUTO_INCREMENT"></column>
    
    #TODO: add functionality to MySQL and SQLite3 classes to handle database initiation at startup
    
    #TODO: support versions of DBSchema so we can handle old schema definitions appropriately.
    """
    
    schema_version = Version(0,0,1) #default schema version
    schema = None  #the soup once its been made
    isvalid = False #varifies the validity of a schema

    
    def __init__(self, schema):
        """
        DBSchema constructor takes a schema definition as one of the following: a string, a filename, or an open file handle.
        """
        if type(schema) is str and not os.path.exists( schema ):
            self.schema = BeautifulSoup(schema, 'html.parser')
        elif type(schema) is file:
            self.schema = BeautifulSoup(schema, 'html.parser')
        elif type(schema) is str and os.path.exists():
            try: 
                self.schema = BeautifulSoup(open(schema), 'html.parser')
            except Exception as e:
                raise Exceptions.FileAccessError
        
        self.isvalid = self.validate()
        if not self.isvalid:
            raise Exceptions.DBSchemaError
        
        #set our schema version
        self.schema_version = self.schema.database['version']
        
        
   
    def validate(self):
        """
        boolean function to verify the validity of a schema
        """
        #TODO: make sure the schema is complete.  This is going to be much harder than it seems.
        return True



    def get_tables(self):
        """
        return a list of tables in the schema
        """
        retval = []
        if self.isvalid:
            for table in self.schema.findAll("table"):
                retval.append(table)
            return retval
        else:
            return None
 
 
    
    def get_table(self,tablename):
        """
        return the rows of a table in the schema
        """
        retval = []   
        if self.isvalid:
            for t in self.schema.findAll("table"):
                if t['name'] is tablename:
                    for col in t['name']:
                        retval.append(col)
            if len(retval) > 0:
                return retval
            else: 
                return False
        else:
            return False
  
    

    def __repr__(self):
        """
        pretty-print the schema
        """
        return self.schema.prettify()
    
    
#EOF