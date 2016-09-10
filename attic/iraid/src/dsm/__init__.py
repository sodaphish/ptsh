import logging
import inspect
import os
import sys
import string

from dsm.utility import *

__version__ = "0.0.1"
__all__ = [ 'manifest', 'version', 'filesystem', 'utilities', ]

#TODO: make this so its dynamically determined, possibly use: 
# http://code.activestate.com/recipes/474083-get-the-path-of-the-currently-executing-python-scr/
__root_dir = '/home/cjs/mine/src/iraid'
__logfile = __root_dir + "/dsm.log"

#TODO: make it so we can set the log level from a client... 
logging.basicConfig( filename = __logfile, level = logging.DEBUG, format = '%(asctime)s - %(levelname)-8s - %(module)s - %(funcName)s:%(lineno)d - %(message)s', datefmt = '%a, %d %b %Y %H:%M:%S' )

def log_event( loglevel, logmessage ):
	#TOOD: ...this appears to be working, but... it could be better...
	caller = inspect.getframeinfo( inspect.currentframe().f_back )[2]
	if loglevel is "info":
		logging.info( caller + '() ' + logmessage )
	elif loglevel is "warn":
		logging.warn( caller + '() ' + logmessage )
	elif loglevel is "error":
		logging.error( caller + '() ' + logmessage )
	elif loglevel is "critical":
		logging.critical( caller + '() ' + logmessage )
	else:
		logging.debug( caller + '() ' + logmessage )


