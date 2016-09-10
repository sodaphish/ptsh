"""
CPEM Secure XML RPC Client (cpem/client.py)

@copyright: Copyright 2010, C.J. Steele, all rights reserved.

@author: C.J. Steele <coreyjsteele@gmail.com> 
"""

import xmlrpclib
import sys
import os
import cpem
from cpem import *
from cpem.misc import Version

#===============================================================================
# SecureXMLRPCClient() Class
#===============================================================================
class SecureXMLRPCClient():
    """SecureXMLRPCClient
    This is a class that facilitiates and manages the process of connecting to a
    secure XML/RPC server
    
    The Client will only connect to a server of the same major and minor version.
    build/bug version is irrelevant to the connection process.
    """
    host = None
    port = None
    version = None
    cert_key = None
    cert_file = None
    state = None
    cpemClient = None


    #TODO: make this use keys to verify connections!
    #TODO: all certificates need to be checked!
    #TODO: the client needs to support proxies
    def __init__(self,host='127.0.0.1',port=3170,certfile='certs/cert.pem',keyfile='certs/cert.pem'):
        try:
            self.set_host(host)
            self.set_port(port)
            self.set_version(Version(0,2,0))
            self.set_key_file(keyfile)
            self.set_cert_file(certfile)
            self.set_state(False)
        except:
            raise

        # TODO: implement key-based authentication
        try:
            self.cpemClient = xmlrpclib.ServerProxy(self.get_dsn())
            self.state = True
        except:
            sys.stderr.write('connection failed.')
            raise
    '''end __init__()'''


    def call(self,func):
        """execFunction()
        public method to execute and return RPC calls to the RPC server.
        """
        if self.state is True:
            try:
                # this actually calls the function, gets the results, and returns them to the caller
                return getattr(self.cpemClient,func)
            except:
	           raise CPEMException,'call to %s failed.' % (func)
        else:
            raise CPEMException,'Client not connected.'
    '''end call()'''


    def set_host(self,host):
        """set_host()
        internal method to validate the server passed to the constructor.
        """
        # TODO: verify server either resolves to a name, or that it is a valid IP 
        self.host = host
        # TODO: return a boolean value based on the results of our ability to
        # resolve the IP/hostname
    '''end set_host()'''


    def set_port(self,port):
        """set_port()
        internal method to validate the server port passed to the constructor.
        """
        if int(port) > 0 and int(port) <= 65535:
            self.port = port
            return True
        return False
    '''end set_port()'''


    def set_cert_file(self,certfile):
        """set_cert_file()
        method to verify the certificate file
        """
        #TODO: implement this
        self.cert_file = certfile
    '''end set_cert_file()'''


    def set_key_file(self,keyfile):
        """set_cert_key()
        method to verify the certificate key file
        """
        #TODO: implement this
        self.cert_key = keyfile
    '''end set_cert_key()'''

    def set_state(self,state):
        """set_state()
        sets the state of the current connection to a boolean value
        """
        #TODO: implement this -- this should be automagic; check the socket state
        self.state = state
    '''end set_state()'''

    def set_version(self,version=Version()):
        """set_version()
        """
        #TODO: implement this
        self.version = version
    '''end set_version()'''

    def get_dsn(self):
        """get_dsn()
        method to provide the data source name (DSN) of the CPEM server.  
        """
        return ("http://%s:%s" % (self.host,self.port))
    ''''end get_dsn()'''

'''end SecureXMLRPCClient()'''
#------------------------------------------------------------------------------ 


#===============================================================================
# CPEMClient() Class -- an alias
#===============================================================================
class CPEMClient(SecureXMLRPCClient):
    pass
'''end CPEMClient()'''
#------------------------------------------------------------------------------
