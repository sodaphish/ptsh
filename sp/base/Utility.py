"""
@author: sodaphish@protonmail.ch
@date: 2016/07/11

utility functions that don't fall into a class for various reasons.
"""

import sys
try:
    import ipaddress 
except: 
    print "missing ipaddress; please `pip install ipaddress` before proceeding"
    sys.exit(2)
    


def is_ip(target):
    """
    returns false if target is not a valid IP address
    """
    try:
        ipaddress.ip_address(unicode(target))
    except ipaddress.AddressValueError:
        return False
    except ValueError:
        return False
    return True

def is_port(port):
    """
    returns true if the port is within the valid IPv4 range
    """
    if port >= 0 and port <= 65535:
        return True
    return False