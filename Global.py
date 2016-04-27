"""
@author: SodaPhish <sodaphish@protonmail.ch>

This is the global configuration, it needs to be included in all splib projects, and tailored accordingly

"""
import sys


# TODO: unfortunately this has to be manually set for now.
sys.path.append( "/Users/SodaPhish/Documents/workspace/src/src/" )
sys.path.append( "./" )



try:
    from sp.base.Version import Version
    from sp.base.Config import Config
    from sp.base.Logging import LoggerConfig
    from sp.base import Exceptions
except Exception as e:
    print "must install sp in sys.path() -- %s" % (e)
    print "email sodaphish@protonmail.ph for a copy of the sp lib"
    sys.exit(2)


cfg = None
try: 
    cfg = Config("settings.cfg")
    if cfg.get_value('init.validate'):
        """
        config file requires database schema validation
        """
        #TODO: implement this
        pass
    
    if cfg.get_value('init.autostart'):
        """
        config file specifies we should do stuff when we startup
        """
        #TODO: implement this
        pass
    
except Exception as e:
    raise e




_ver = Version(int(cfg.get_value('version.major')),int(cfg.get_value('version.minor')),int(cfg.get_value('version.patch')))


loglevel=cfg.get_value('logging.loglevel')
logcfg = LoggerConfig(loglevel, **cfg.config)
logging.config.dictConfig(logcfg.config)
log = logging.getLogger()




"""
Verify that the configuration file is defined and that our database type is defined.
"""
try: cfg
except NameError:
    print "configuration file not defined as 'cfg'"
    sys.exit(1)
#NOTE: this is optional for some projects.
try: cfg.get_value('db.type')
except Exception as e:
    print "database type not defined in configuration file"
    sys.exit(1)
    


#TODO: move this to a function in sp.db
db = None
if cfg.get_value(db.type):
    if cfg.get_value(db.type) == 'mysql':
        #TODO: attempt the database connection using the MySQL 
        pass
    elif cfg.get_value(db.type) == 'sqlite3':
        try:
            db = sqlite3.connect(cfg.get_value('db.path'))
        except Exception as e:
            log.critical("%s" % e )
            sys.exit(1)
else: 
    #no database
    pass



#EOF