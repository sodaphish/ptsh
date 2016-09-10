"""
CPEM Secure XML RPC Server (cpem/server.py) 

@copyright: Copyright 2011, C.J. Steele, all rights reserved.
@author: C.J. Steele <corey@hostedbycorey.com>
@version: 0.1.9
@summary: provides the broker which uses the Broker-Agent Protocol to communicate with clients

@change: 

@attention: Some of this was built based on a recipe at http://code.activestate.com/recipes/496786, but it has since undergone significant modification.
"""

import SocketServer
import BaseHTTPServer
import SimpleHTTPServer
import SimpleXMLRPCServer
import inspect
import socket
import os
import sys
from OpenSSL import SSL
import cpem
from cpem import *
from cpem.plugins import *


#===============================================================================
# 
#===============================================================================
class ThreadedBaseServer(SocketServer.ThreadingMixIn,SocketServer.BaseServer):
    """ThreadedBaseServer Class
    Implements a BaseServer with the ThreadingMixIn to support asynchronous connectivity. 
    """
    pass
'''end ThreadedBaseServer()'''

#===============================================================================
# SecureXMLRPCServer() Class
#===============================================================================
class SecureXMLRPCServer(BaseHTTPServer.HTTPServer,SimpleXMLRPCServer.SimpleXMLRPCDispatcher):

    def __init__(self,server_address,HandlerClass,certFile='certs/cert.pem',keyFile='certs/key.pem',logRequests=False):
        """Secure XML-RPC server.
        It it very similar to SimpleXMLRPCServer but it uses HTTPS for transporting XML data.
        """
        cpem.log_event('debug',"starting SecureXMLRPCServer")
        self.logRequests = logRequests #turn off the BaseHTTPServer logging... because we dun need it.
        SimpleXMLRPCServer.SimpleXMLRPCDispatcher.__init__(self,True,None)
        ThreadedBaseServer(self,SocketServer.BaseServer.__init__(self,server_address,HandlerClass))

        ctx = SSL.Context(SSL.SSLv23_METHOD)
        ctx.use_privatekey_file (keyFile)
        ctx.use_certificate_file(certFile)
        self.socket = SSL.Connection(ctx,socket.socket(self.address_family,self.socket_type))
        self.server_bind()
        self.server_activate()
        cpem.log_event('debug','server setup complete')

        def shutdown_request(self,request):
            request.shutdown()

    '''end __init__()'''

'''end SecureXMLRPCServer()'''
#------------------------------------------------------------------------------ 


#===============================================================================
# SecureXMLRpcRequestHandler() Class
#===============================================================================
class SecureXMLRpcRequestHandler(SimpleXMLRPCServer.SimpleXMLRPCRequestHandler):

    def setup(self):
        """setup()
        #TODO: document this.
        """
        self.connection = self.request
        self.rfile = socket._fileobject(self.request,"rb",self.rbufsize)
        self.wfile = socket._fileobject(self.request,"wb",self.wbufsize)
    '''end setup()'''

    def do_POST(self):
        """do_POST()
        #TODO: document this.
        """
        client_ip,client_port = self.client_address
        cpem.log_event('info','client connection from %s:%d' % (client_ip,client_port))
        try:
            data = self.rfile.read(int(self.headers["content-length"]))
            cpem.log_event('debug','client request: %s' % data)
            response = self.server._marshaled_dispatch(data,getattr(self,'_dispatch',None))
            cpem.log_event('debug','response to client: %s' % response)
        except:
            # something goed boom
            cpem.log_event('error','oops! something went wrong ')
            self.send_response(500)
            self.end_headers()
        else:
            # we received a valid XML response
            cpem.log_event('debug',"valid XML response received.")
            try:
                self.send_response(200)
                self.send_header("Content-type","text/xml")
                self.send_header("Content-length",str(len(response)))
                self.end_headers()
                cpem.log_event('debug',"response headers sent")
                self.wfile.write(response)
                cpem.log_event('debug',"response sent")
                self.wfile.flush()
                cpem.log_event('debug',"buffer flushed")
                self.connection.shutdown() #do we need to do a full shutdown?
            except:
                cpem.log_event('error',"Something went wrong sending the response")
    '''end do_POST()'''

'''end SecureXMLRpcRequestHandler()'''
#------------------------------------------------------------------------------ 


#===============================================================================
# CPEMServer() Class
#===============================================================================
class CPEMServer():
    """CPEMServer()
    #TODO: Document
    """

    cert_file = None
    cert_key = None
    server = None
    server_host = None
    server_port = None

    def __init__(self,HandlerClass=SecureXMLRpcRequestHandler,host='0.0.0.0',port=3170,cert='certs/sslcert.crt',key='certs/sslcert.crt'):
        cpem.log_event('debug',"entering CPEMServer constructor")
        try:
            self.set_server_host(host)
            self.set_server_port(port)
            self.set_cert_file(cert)
            self.set_key_file(key)
        except:
            cpem.log_event('critical','error occurred during setup')
            raise
        cpem.log_event('debug',"cleared initial cpem .set_* routines")
        try:
            cpem.log_event('debug',"starting SecureXMLRPCServer")
            self.server = SecureXMLRPCServer((self.server_host,self.server_port),HandlerClass,self.cert_file,self.cert_key)
            cpem.log_event('debug',"SecureXMLRPCServer started")
            self.server.register_introspection_functions()
            cpem.log_event('debug',"register_introspection_fuctions() completed")
            init_plugins(self.server)
            cpem.log_event('debug',"plugins loaded")
            self.server.serve_forever()
        except Exception,e:
            cpem.log_event('error',"failed to setup server: %s" % (e[0]))
    '''end __init__()'''


    def set_server_host(self,host):
        """Takes an IP or hostname and, if its valid, set self.host to the passed value.
        """
        #TODO: validate this-- it can be a host or an IP
        cpem.log_event('debug',"setting self.server_host=%s" % (host))
        self.server_host = host
    '''end set_server_host()'''


    def set_server_port(self,port):
        """validate the port passed to the constructor; must be an int between 1 and 65534
        """
        if port >= 1 and port <= 65535:
            cpem.log_event('debug',"setting self.server_port=%s" % (port))
            self.server_port = port
        else:
            cpem.log_event('error','port out of range')
            raise TypeError,'port out of range'
    '''end set_server_port()'''


    def set_cert_file(self,certfile):
        """verifies that the file exists
        """
        #TODO: implement this
        cpem.log_event('debug',"setting self.cert_file=%s" % (certfile))
        self.cert_file = certfile
    '''end set_cert_file()'''


    def set_key_file(self,keyfile):
        """verifies that the key file exists
        """
        #TODO: implement this
        cpem.log_event('debug',"setting self.cert_key=%s" % (keyfile))
        self.cert_key = keyfile
    '''end set_key_file()'''

'''end CPEMServer()'''
#------------------------------------------------------------------------------
