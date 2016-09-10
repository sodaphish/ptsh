"""
CPEM Main Library

@author: C.J. Steele <corey@hostedbycorey.com>
@summary: This is the main CPEM library
@version: 0.1.9

"""
from string import replace
import os
import sys
import logging
import inspect

from cpem.misc import Version

__version__ = Version(0,1,9)


#===============================================================================
# Setup CPEM global logging facility.
#===============================================================================
_cpem_logger = logging.getLogger('')
_cpem_logger.setLevel(logging.DEBUG)
_log_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)-8s - %(message)s")
_console_log_handler = logging.StreamHandler()
_console_log_handler.setFormatter(_log_formatter)
#TODO: CJS 2011/04/09 - figure out a more absolute pathing for the log file.
_file_log_handler = logging.FileHandler("cpem.log")
_file_log_handler.setFormatter(_log_formatter)
#_cpem_logger.addHandler(_console_log_handler)
_cpem_logger.addHandler(_file_log_handler)


def log_event(loglevel,logmessage,strip_nl=True):
  #TOOD: CJS 2011/04/09 - make sure this is getting everything the way we want it.
  caller = inspect.getframeinfo(inspect.currentframe().f_back)
  caller_frmt = "%s:%s:%s" % (os.path.basename(caller[0]),caller[1],caller[2])
  if strip_nl:
      # replace the new-line characters with spaces in logmessage
      logmessage = replace(logmessage,'\n','')

  if loglevel is "info":
    _cpem_logger.info(caller_frmt + '() ' + logmessage)
  elif loglevel is "warn":
    _cpem_logger.warn(caller_frmt + '() ' + logmessage)
  elif loglevel is "error":
    _cpem_logger.error(caller_frmt + '() ' + logmessage)
  elif loglevel is "critical":
    _cpem_logger.critical(caller_frmt + '() ' + logmessage)
  else:
    _cpem_logger.debug(caller_frmt + '() ' + logmessage)


class CPEMException(Exception):
    value = None

    #TODO: get callback data too so we can figure out from whence the exception came.
    def __init__(self,value):
        self.value = value

    def __str__(self):
        return repr(self.value)

    def __repr__(self):
        return repr(self.value)


#EOF
