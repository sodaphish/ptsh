# -*- coding: utf-8 -*-
"""
@author: sodaphish@protonmail.ch
"""

import sys

try:
    from sp.base import Exceptions
except:
    print "Install sp into sys.path()"
    sys.exit(2)
    


class DBSchema():
    """
    XML database schema abstraction
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