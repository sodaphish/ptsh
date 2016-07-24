# -*- coding: utf-8 -*-
"""
@author: adosch <adam@wisehippy.com>
@author: SodaPhish <sodaphish@protonmail.ch>

Configuration library for splib.

Basic configuration file structure is that of a Windows INI file, e.g.:

[section]
variable1 = value1
variable2 = value2

All splib projects must have the following sections in their config file: 
    [init]
    validate = [0|1]
    autostart = [0|1]
    
    [version]
    major = [0-9999]
    minor = [0-9999]
    patch = [0-9999]
    
If a database is to be used, it will be defined in the section [db], which only has two globally required variables: 

    [db]
    type = [sqlite3|mysql]
    validate = [0|1]
    
    If type is sqlite3, then you must additionally specify: 
        schema = /path/to/schema
        path = /path/to/database/file
        
    If type is mysql, then you must additionally specify:
        host = [a-zA-Z0-9]
        port = [0-65535]
        user = [a-zA-Z0-9]
        pass = [a-zA-Z0-9]
        dbname = [a-zA-Z0-9]
        schema = /path/to/schema
        
    

"""

from ConfigParser import SafeConfigParser
import os
import Exceptions
import re
import sys

try:
    from sp.base.Exceptions import ConfigFault
except Exception as e:
    print "couldn't load splib!"
    sys.exit(2)


class Config(SafeConfigParser):
    """
    Config class is a wrapper arouond the SafeConfigParser.  It optionally
    takes 'filename' as an argument otherwise looks for configuration in
    settings.cfg.
    """

    def __init__(self, filename=None):
        """
        Initializes the SafeConfigParser() class, checks the filename and
        creates the configuration dictionary.
        """

        SafeConfigParser.__init__(self)
        if not filename:
            filename = "settings.cfg"

        self.config_file = self._check_file(filename)
        self.config = None
        self._populate_config()

    def _check_file(self, filename):
        """
        Check to see if file exists and is readable. If either condition is
        false, an error is raised, otherwise, the filename is returned.
        """
        if os.path.isfile(filename):
            if os.access(filename, os.R_OK):
                return filename
            else:
                raise Exceptions.FileAccessError(
                    'Cannot read file %s' % filename)
        else:
            raise Exceptions.FileAccessError(
                'File %s does not exist.' % filename)

    def _adjust_value(self, value):
        """
        Analyze the value string and perform adjustments to the value
        based on certain use cases.
        """
        # Change None values to a boolean True flag
        if value is None:
            return None

        # Change string true as True boolean
        if value.lower() == 'true':
            return True

        # Change string false to False boolean
        if value.lower() == 'false':
            return False

        # Change comma seperated values into an array
        if ',' in value and "mongodb" not in value:
            return [newval.strip() for newval in value.split(',')]

        # No adjustments needed, just return the value
        return value.strip()

    @property
    def config_file(self):
        """
        Configuration file being used.
        """
        return self.config_file

    @config_file.setter
    def config_file(self, value):
        """
        Setting Configuration file to use. Changing this value will reset
        the configuration dictionary.
        """
        self.config_file = self._check_file(value)
        self.config = None
        self._populate_config()

    @property
    def config(self):
        """
        Dictionary of configuration file.

        The dictionary can be reloaded via the get_config() method or by
        changing the config_file property.

        :key: in the format of 'section.item'
        """
        return self.config

    def _populate_config(self):
        """
        Retrieve configuration information from the config_file and
        create a dictionary of values using the section.item as the key.
        """
        # Get the config file
        try:
            self.readfp(open(self.config_file, 'r'))
        except Exception, e:
            raise Exception(e)

        # Get all non default sections, items and values
        _cfg = {}
        for _section in self.sections():
            for _key, _val in self.items(_section):
                _dictkey = str(_section).strip() + '.' + str(_key).strip()
                _cfg[_dictkey] = self._adjust_value(_val)

        # Handle default values here
        # if self.defaults() is not None:
        #    for _key, _val in self.defaults():
        #        _dictkey = 'DEFAULT.' + str(_key).strip()
        #        _cfg[_dictkey] = self._adjust_value(_val)
        # Set the class property

        self.config = _cfg

    def get_value(self, sectionitem):
        """
        Retrieve configuration information in 'section.item' reference
        If found, will return value.  If not found, will return None.
        """
        if sectionitem in self.config:
            return self.config[sectionitem]
        else:
            return None

    def reload(self):
        """
        routine to re-read the configuration file.  self.get_config() DOES NOT WORK
        """
        # TODO: overload self.get_config() when this is written.
        pass

    def save(self):
        """
        save the configuration off to disk; not elegant, but functional
        note: 1) it will not save comments that had been in a configuration, and 2) it writes files out in UNIX format, fuck yo DOS
        """
        configout = self.__repr__()
        if os.access(self.config_file, os.W_OK):
            try:
                fp = open(self.config_file, "w")
                fp.write(configout)
                fp.close()
            except Exception as e:
                raise Exceptions.ConfigFault("Couldn't write config!")
        else:
            raise Exceptions.FileAccessError("file not writable")

    def __repr__(self):
        """
        return a string value of the configuration
        """
        retval = ""
        sections = []
        for key in self.config:
            (section, variable) = key.split('.')
            if section not in sections:
                sections.append(section)
        sections.sort()
        for s in sections:
            retval = "%s[%s]\n" % (retval, s)
            for key in self.config:
                (sec, val) = key.split('.')
                if sec == s:
                    retval = "%s%s = %s\n" % (
                        retval, val, self.config["%s.%s" % (sec, val)])
            retval = "%s\n" % (retval)

        return retval

    def __getitem__(self, *meh):
        try:
            sectionitem = meh[0]
            return self.config[sectionitem]
        except Exception as e:
            raise ConfigFault("couldn't get item")

    def __setitem__(self, *meh):
        """
        assign a value to a section.variable
        """
        try:
            (section, value) = meh[0], meh[1]
            self.config[section] = value
        except Exception as e:
            raise ConfigFault("invalid assignment")

    def __delitem__(self, *bits):
        """
        delete a section.variable key pair, a la `del cfg['section.variable']`  
        """
        try:
            section = bits[0]
            if self.config[section]:
                del self.config[section]
        except Exception as e:
            raise ConfigFault("unknown variable")


""" ___EOF___ """
