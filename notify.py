#!/usr/bin/python 
'''
pynotify - a cli interface to the Notify OSD facility in Ubuntu and other distros.
	by C.J. Steele <coreyjsteele@gmail.com>  (http://sodaphish.com)

This code is distributable and modifiable via the GNU GPL license.
'''
import pynotify
import sys
from optparse import OptionParser


def catargs( arg ):
	retval = ""
	for i in range( 0, len(arg) ):
		retval = retval + arg[i]
		retval = retval + " "
	return retval


usage = "usage: %prog {-t -m}"
parser = OptionParser( usage )
parser.add_option( "-a", "--appname", dest="appname", help="application the notification comes from" )
parser.add_option( "-t", "--title", dest="title", help="title of the notification" )
parser.add_option( "-m", "--message", dest="msg", help="the message to display" )
( options, args ) = parser.parse_args()

if not options.appname:
	options.appname = "pynotify"

if not options.title:
	options.title = "UNKNOWN"

if not options.msg:
	if args:
		options.msg = catargs( args )
	else:
		parser.error( "you have to specify a message, at least." )

if options.title and options.msg:
	pynotify.init( options.appname )
	notification = pynotify.Notification( options.title, options.msg, "" )
	notification.show()
else:
	parser.usage()

sys.exit( 0 )


