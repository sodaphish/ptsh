import logging
import inspect

__version__="0.1.6"
__log_level = logging.DEBUG
__all__ = ['collector', 'keywords']

#TODO: make this so its dynamically determined, possibly use: 
# http://code.activestate.com/recipes/474083-get-the-path-of-the-currently-executing-python-scr/
__root_dir = '/home/cjs/mine/src/feedcollector'
__logfile = __root_dir + "/semfeed.log"


"""
setup our logging facility.  anyone who wants to be able to use this has to at least include
import.semfeed, and then they can call the log event via semfeed.log_event(LEVEL,MESSAGE)
"""
logging.basicConfig(filename=__logfile,
	level=__log_level,format='%(asctime)s %(levelname)-8s %(message)s', datefmt='%a, %d %b %Y %H:%M:%S')



def log_event(loglevel,logmessage):
	#TOOD: fix me so this shows the right calling function
	caller =  inspect.getframeinfo(inspect.currentframe().f_back)[2]
	if loglevel is "info":
		logging.info(caller + '() ' + logmessage)
	elif loglevel is "warn":
		logging.warn(caller + '() ' + logmessage)
	elif loglevel is "error":
		logging.error(caller + '() ' + logmessage)
	elif loglevel is "critical":
		logging.critical(caller + '() ' + logmessage)
	else:
		logging.debug(caller + '() ' + logmessage)
