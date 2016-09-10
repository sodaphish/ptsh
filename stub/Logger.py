'''
Logging.py - by C.J. Steele <coreyjsteele@yahoo.com>
    (C)opyright 2006, C.J. Steele, all rights reserved.

This is a degraded replacement to the 'logging' module -- degraded for simplicity.

Usage: 

logger = Logging( ["f", "/path/to/your/logfile.log"] )
logger.setLevel( "WARN" )
logger.debug( "a debug message" )
logger.info( "a info message" )
logger.warn( "a warn message" )
logger.error( "a error message" )
logger.critical( "a critical message" )
# the above will result in the warn, error and critical messages being written to file

logger2 = Logging( "s" )
logger2.setLevel( "error" )
logger2.warn( "a warn message" )
logger2.error( "a error message" )
logger2.critical( "a critical message" )
# the above will result in the error and critical messages being output to standard out

'''
from time import strftime, localtime

class Logger:
    
    ''' our logger ''' 
    level = 0
    type = "file"
    filename = ""
    filedescripter = ""
    entryCount = 0

    def __init__( self, args ):
        ''' python has no switch '''
        if args[0] == "f":
            self.type = "file" 
            self.filename = args[1]
            #TODO: catch this if it fails.
            self.filedescripter = open( self.filename, "a" )

        elif args[0] == "s":
            self.type = "stream"

        else:
            raise Exception( "LoggingError", "unknown type!" )

    def setLevel( self, level ):
        if level.lower() == "debug":
            self.level = 0
        elif level.lower() == "info":
            self.level = 1
        elif level.lower() == "warn":
            self.level = 2
        elif level.lower() == "error":
            self.level = 3
        elif level.lower() == "critical":
            self.level = 4
        else:
            self.level = 0

    def outputHandler( self, lvl, msg ):
        output = "%s - %s - %s" % ( strftime( "%G-%m-%d %H:%M:%S", localtime() ), lvl, msg )
        if self.type == "file":
            #TODO: catch these when they fail...
            self.filedescripter.write( output )
            self.filedescripter.write( "\n" )
        else:
            print( output )
        self.entryCount += 1

    def debug( self, message ):
        if self.level <= 0:
            self.outputHandler( "DBG", message )

    def info( self, message ):
        if self.level <= 1:
            self.outputHandler( "INF", message )

    def warn( self, message ):
        if self.level <= 2:
            self.outputHandler( "WRN", message )

    def error( self, message ):
        if self.level <= 3:
            self.outputHandler( "ERR", message )

    def critical( self, message ):
        if self.level <= 4:
            self.outputHandler( "CRI", message )


''' EOF '''
