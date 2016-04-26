# -*- coding: utf-8 -*-
"""
@author: SodaPhish <sodaphish@protonmail.ch>
"""

import sys

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
    from sp.base import Exceptions
except:
    print "Install sp into sys.path()"
    sys.exit(2)
    


class DBSchema():
    """
    XML database schema abstraction class to read-in, write-out, and validate database schemas.
    #TODO: add functionality to MySQL and SQLite3 classes to handle database initiation and verification at startup
    """
    def __init__(self):
        #TODO: populate a schema from string or file
        pass
    
    def validate(self):
        """
        boolean function to verify the validity of a schema
        """
        #TODO: validates the schema as being properly formed
        pass

    
#EOF