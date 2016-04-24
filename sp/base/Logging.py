# -*- coding: utf-8 -*-
"""
@author: adosch <adam@wisehippy.com>
"""
import sys,os,logging
from logging import handlers
import logging.config


class DirectoryAccessError(Exception):
    """
    Exception for directory access permission errors
    """
    pass


class InvalidLogLevelType(Exception):
    """
    """
    pass


class InvalidSyslogFacilityType(Exception):
    """
    """
    pass


class LoggerConfig(object):
    """
    LoggerConfig class object to setup and define root-level logging 
    inside a script or application setting in dictionary form to be
    used as input back into the 'logging' module
    """
    def __init__(self, loglevel, logfile=None, logfile_rotate=0, logfile_maxsize=0, logfile_level=logging.INFO,
                 syslog=None, syslog_host="/dev/log", syslog_port=514, syslog_facility=logging.handlers.SysLogHandler.LOG_USER,
                 syslog_level=logging.INFO, console=False, console_level=logging.DEBUG, *args, **kwargs):

        self.log = None        

        self.handler_list = []
        
        self.config = {}

        self.loglevel = self._validate_loglevel(kwargs.get('logging.loglevel', loglevel))

        self.logfile = self._check_dirpath(kwargs.get('logging.logfile', logfile))
        self.logfile_rotate = int(kwargs.get('logging.logfile_rotate', logfile_rotate))
        self.logfile_maxsize = int(kwargs.get('logging.logfile_maxsize', logfile_maxsize))
        self.logfile_level = self._validate_loglevel(kwargs.get('logging.logfile_level', logfile_level))

        self.syslog = kwargs.get('logging.syslog', syslog)
        self.syslog_host = kwargs.get('logging.syslog_host', syslog_host)
        self.syslog_port = kwargs.get('logging.syslog_port', syslog_port)
        self.syslog_facility = self._validate_syslogfacility(kwargs.get('logging.syslog_facility', syslog_facility))
        self.syslog_level = self._validate_sysloglevel(kwargs.get('logging.syslog_level', syslog_level))

        self.console = kwargs.get('logging.console', console)
        self.console_level = self._validate_loglevel(kwargs.get('logging.console_level', console_level))

        self.version = 1
        self.disable_existing_loggers = False

        self.config['version'] = self.version
        self.config['disable_existing_loggers'] = self.disable_existing_loggers

        # For more formatting types, visit:  https://docs.python.org/2/library/logging.html
        # This should really be done in a lookup fashion of some sort?
        self.config['formatters'] = {}
        self.config['formatters']['standard'] = {}
        self.config['formatters']['standard']['format'] = "[%(asctime)s] %(levelname)s %(module)s:%(funcName)s:%(lineno)d %(message)s"
        #self.config['formatters']['standard']['format'] = "[%(asctime)s] %(module)s %(levelname)s %(funcName)s:%(lineno)d %(message)s"
        self.config['formatters']['standard']['datefmt'] = "%Y-%m-%d %H:%M:%S"

        self.config['formatters']['syslog'] = {}
        self.config['formatters']['syslog']['format'] = "%(module)s[%(process)d]: %(levelname)s %(message)s"

        self.config['handlers'] = self._process_handlers()

        self.config['loggers'] = self._process_root_logger()

    def _return_formatstring(self, handlername):
        pass

    def _check_dirpath(self, filename):
        try:
            _dirname = os.path.dirname(filename)
    
            if not _dirname:
                _dirname = os.path.curdir
    
    
            if all([os.access(_dirname, os.R_OK), os.access(_dirname, os.W_OK)]):
                return filename
            else:
                raise Exceptions.DirectoryAccessError("Unable to read or write to directory location '%s'" % _dirname)

        except AttributeError: # If original 'None' type is passed in
            return None

    def _validate_loglevel(self, level):
        _level = level

        if isinstance(_level, str):

            result = logging.getLevelName(_level)
    
            if isinstance(result, int):
                return result
            else:
                raise Exceptions.InvalidLogLevelType("'%s' in not a valid log level" % _level)
        else:
            return _level

    def _validate_sysloglevel(self, level):
        _level = level

        if isinstance(_level, str):
    
            result = logging.handlers.SysLogHandler.priority_names.get(_level.lower())
    
            if result:
                return result
            else:
                raise Exceptions.InvalidLogLevelType("'%s' is not a valid Syslog level" % _level)
        else:
            return _level

    def _validate_syslogfacility(self, level):
        _level = level

        if isinstance(_level, str):
    
            result = logging.handlers.SysLogHandler.facility_names.get(_level.lower())
    
            if result:
                return result
            else:
                raise Exceptions.InvalidSyslogFacilityType("'%s' is not a valid Syslog facility level" % _level)
        else:
            return _level

    def _create_console_handler(self, console, level):
        pass

    def _create_logfile_handler(self, loglevel, logfile, logfile_rotate, logfile_maxsize, logfile_level):
        pass

    def _create_syslog_handler(self, syslog, syslog_host, syslog_port, syslog_facility, syslog_level):
        pass

    def _process_handlers(self):
        _handlers = {}

        if self.logfile:

            self.handler_list.append('logfile')

            _handlers['logfile'] = {}
            _handlers['logfile']['level'] = self.logfile_level
            _handlers['logfile']['formatter'] = 'standard'
            _handlers['logfile']['class'] = 'logging.handlers.RotatingFileHandler'
            _handlers['logfile']['filename'] = self.logfile
            _handlers['logfile']['maxBytes'] = self.logfile_maxsize
            _handlers['logfile']['backupCount'] = self.logfile_rotate

        if self.console:
            
            self.handler_list.append('console')

            _handlers['console'] = {}
            _handlers['console']['level'] = self.console_level
            _handlers['console']['formatter'] = 'standard'
            _handlers['console']['class'] = 'logging.StreamHandler'
            _handlers['console']['stream'] = sys.stdout # '/dev/stdout'

        if self.syslog:

            self.handler_list.append('syslog')

            _handlers['syslog'] = {}
            _handlers['syslog']['level'] = self.syslog_level
            _handlers['syslog']['formatter'] = 'syslog'
            _handlers['syslog']['class'] = 'logging.handlers.SysLogHandler'           
            
            if self.syslog_host <> "/dev/log":
                _address = (self.syslog_host, self.syslog_port)
            else:
                _address = self.syslog_host          
            
            _handlers['syslog']['address'] = _address
            _handlers['syslog']['facility'] = self.syslog_facility
        
        return _handlers

    def _process_root_logger(self):
        _loggername = ''

        _loggers = {}
        _loggers[_loggername] = {}
        
        _loggers[_loggername]['handlers'] = self.handler_list
        _loggers[_loggername]['level'] = self.loglevel

        return _loggers
