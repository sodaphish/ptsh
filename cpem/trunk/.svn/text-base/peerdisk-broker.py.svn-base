"""
CPEM Daemon (cpemd.py)
@copyright: Copyright 2010, C.J. Steele, all rights reserved.
@author: C.J. Steele <coreyjsteele@gmail.com>
@summary: main C&C for the PeerDisk broker

XML RPC over HTTPS adapted from http://code.activestate.com/recipes/496786
@attention: there's a bug in Python 2.7 that causes issues, only use python 2.6 with this.
@attention: https://bugs.launchpad.net/ubuntu/+source/pyopenssl/+bug/821984
"""
from sys import exit,argv,platform
from time import sleep,time
import getopt

#TODO: pin these down so we aren't importing the entire standard library!
import sys
import inspect
import os
sys.path.append('.')
import cpem
from cpem.server import *
from cpem.plugins import refresh_plugins


server = None


def signal_handle_sighup():
	#TODO: re-read the configuration and re-call main()
	#TODO: re-initialize plugins too!
	refresh_plugins(server)
	pass


def signal_handle_sigterm():
	#TODO: safely close out our database connections
	cpem.log_event('debug',"PeerDisk daemon caught sigterm or sigint")
	sys.exit(1)


def usage():
	print "PeerDisk Broker Daemon v.",cpem.__version__
	print "(C)opyright 2011, C.J. Steele, all rights reserved."
	print " -h, --help     show this help"
	print " -v, --verbose  log agent events to console"
	print " -V, --version  display version information"
	print " -D, --daemon   run as a daemon"
	print


if __name__ == "__main__":
	# handle supported platform-specific pieces
	if platform.startswith("linux"):
		agent_os = 'linux'
		from os import fork,chdir,setsid,umask,walk,stat
		import signal
		signal.signal(signal.SIGHUP,signal_handle_sighup)
		signal.signal(signal.SIGTERM,signal_handle_sigterm)
		signal.signal(signal.SIGINT,signal_handle_sigterm)
	elif platform.startswith("win32"):
		agent_os = 'win32'
		import win32api
		import win32con
		#TODO: catch equiv of sighup for Windows so we can re-read our config file, etc.
	elif platform.startswith('darwin'):
		agent_os = 'darwin'
		from os import fork,chdir,setsid,umask,walk,stat
		import signal
		signal.signal(signal.SIGHUP,signal_handle_sighup)

	try:
		opts,args = getopt.getopt(argv[1:],"hvVD",["help","verbose","version","daemon"])
	except getopt.GetoptError:
		usage()
		exit(2)

	# handle command-line arguments
	for opt,arg in opts:
		if opt in ("-h","--help"):
			usage()
			exit(0)
		elif opt in ("-v","--verbose"):
			cpem._cpem_logger.setLevel(logging.DEBUG)
			#TODO: make we need some sort of global variable indicating our  in CPEM
			pass
		elif opt in ("-V","--version"):
			print "PeerDisk Broker v.",cpem.__version__
			print "(C)opyright 2011, C.J. Steele, all rights reserved."
		elif opt in ("-D","--daemon"):
			# daemonization bits for Linux and MacOSX
			if agent_os == 'linux' or agent_os == 'darwin':
				try:
					pid = fork()
					if pid > 0:
						exit(0)
				except OSError,e:
					exit(1)
				#TODO: make this cross-platform sensitive?  
				chdir("/")
				setsid()
				umask(0)
				try:
					pid = fork()
					if pid > 0:
						exit(0)
				except OSError,e:
					exit(1)
			# NT doesn't use daemonization, 
			#TODO: http://islascruz.org/html/index.php?gadget=StaticPage&action=Page&id=6
			elif agent_os == 'win32':
				#TODO: check to see if we were called by the service controll process?
				print "E: NT doesn't support daemonizing, you must start the service with the 'net start cpemagent' command"
				exit(1)


	# initialization has been finished, lets do this!
	try:
		server = CPEMServer()
	except CPEMException,e:
		print e
		sys.exit(1)


#EOF
