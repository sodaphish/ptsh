"""
stub.py - a program that does nothing
by C.J. Steele <coreyjsteele@gmail.com>
"""
import sys, os
sys.path.append( os.getcwd() )
from Registry import *
from Plugins import *
from Logger import *

reg = Registry()
conf = []
conf = reg.getScope( "global.%" )
logger = Logger( ["f", conf['global.logfile'] ] )
logger.setLevel( conf['global.loglevel'] )

logger.debug( "__BEGIN__" )

# put your code here.



# end your code here

logger.debug( "__END__" )
#__EOF__
