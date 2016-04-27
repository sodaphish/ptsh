# -*- coding: utf-8 -*-
"""
@author: SodaPhish <sodaphish@protonmail.ch>
"""

import sys, re, os

#import etree
try: 
    from lxml import etree
except ImportError:
    try:
         import xml.etree.cElementTree as etree
    except ImportError:
        try: 
            import xml.etree.ElementTree as etree
        except ImportError:
            try:
                import cElementTree as etree
            except ImportError:
                try:
                    import elementtree.ElementTreee as etree
                except ImportError:
                    print "Failed to import ElementTree"
                    sys.exit(1)
             
try:
    from xml.dom import minidom
except ImportError:
    print "couldn't import minidom!"
    sys.exit(2)

try:
    from sp.base import Exceptions
except:
    print "Install sp into sys.path()"
    sys.exit(2)
    
    
    

class DBSchema():
    """
    XML database schema abstraction class to read-in, write-out, and validate database schemas.
    #TODO: add functionality to MySQL and SQLite3 classes to handle database initiation and verification at startup
    """
    
    schema = None  #the xml schema once loaded
    type = ""
    isvalid = False
    
    def __init__(self, schema):
        #TODO: populate a schema from string or file
        r = re.compile('\<.a-zA-Z0-9*.\>')
        if r.match(schema):
            # this is a text schema, process it accordingly
            pass
        else:
            # this SHOULD be a file being passed in as schema, process it accordingly.
            if os.path.exists(schema):
                try:
                    #try opening the file and reading it in.
                    pass
                except Exception as e:
                    #something went wrong, go ape-shit!
                    pass
            else:
                raise Exceptions.Generic("DBSchema() instantiation method did not receive a text or file-path schema.")
    
    
    def validate(self):
        """
        boolean function to verify the validity of a schema
        """
        #TODO: make sure the schema is complete.  how?
        return True


    def __repr__(self):
        """
        pretty-print the schema
        """
        pass
    
#EOF