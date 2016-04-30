# -*- coding: utf-8 -*-
"""
@author: SodaPhish <sodaphish@protonmail.ch>
"""

import sys, re, os
from sp.base.Exceptions import DBSchemaError
from pyparsing import tableName

try:
    from xml.dom import minidom
except ImportError:
    print "couldn't import minidom!"
    sys.exit(2)

try:
    from sp.base import Exceptions
    from sp.base import Version
except:
    print "Install sp into sys.path()"
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
    
    #TODO: add functionality to MySQL and SQLite3 classes to handle database initiation and verification at startup
    
    #TODO: support versions of DBSchema so we can handle old schema definitions appropriately.
    """
    
    schema_version = Version(0,0,1)
    schema = None  #the xml schema once loaded
    type = ""
    isvalid = False

    
    def __init__(self, schema):
        """
        DBSchema constructor takes a schema definition as one of the following: a string, a filename, or an open file handle.
        """
        #TODO: populate a schema from string or file
        r = re.compile('\<.a-zA-Z0-9*.\>')
        if r.match(schema):
            # this is a text schema, process it accordingly
            try:
                self.schema = minidom.parseString(schema)
            except Exception as e:
                raise DBSchemaError
        else:
            # this SHOULD be a file-name or an open file handler being passed in as schema, process it accordingly.
            if os.path.exists(schema):
                try:
                    #try opening the file and reading it in.
                    self.schema = minidom.parse( schema)
                except Exception as e:
                    #something went wrong, go ape-shit!
                    #TODO: figure out if this was an access error or malformed XML, until then... 
                    raise DBSchemaError

            else:
                raise Exceptions.Generic("DBSchema() instantiation method did not receive valid input.")
        
        self.isvalid = self.validate()
        
        if not self.isvalid:
            raise DBSchemaError

    
    def validate(self):
        """
        boolean function to verify the validity of a schema
        """
        #TODO: make sure the schema is complete.  how?
        return True

    def get_tables(self):
        """
        return a list of tables in the schema
        """
    
    def get_table(self,tablename):
        """
        return the rows of a table in the schema
        """
        #TODO: implement this
        pass


    def __repr__(self):
        """
        pretty-print the schema
        """
        #TODO: clean this up, it will just return a giant string right now, but whatevs.
        rc = []
        nodelist = self.schema.getElementsByTagName("database")[0]
        for node in nodelist:
            if node.nodeType == node.TEXT_NODE:
                rc.append(node.data)
        return ''.join(rc)
    
    
#EOF