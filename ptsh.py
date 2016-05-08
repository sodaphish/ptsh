"""
@author: sodaphish@protonmail.ch
"""


import sys 
from cmd2 import Cmd

import sys



req_version = (2,5)
max_version = (3,0)
cur_version = sys.version_info

#TODO: make sure all code is py3 compatible, until then this has to be here...
if cur_version >= req_version and cur_version < max_version:
    pass
else:
    print "this script requires a version of python 2.5 or higher, but nothing in the 3.x series"
    sys.exit(2)



try:
    from Global import *
    from sp.base import Version
except Exception as e:
    print "splib ate shit and died, fix it!"
    sys.exit(1)



class PTSH(Cmd):
    prompt = 'ptsh> '
    default_to_shell = True #this won't work for logging stuff.
    echo = False
    version = Version.Version(0,0,1)
 
    shortcuts = {'?':'help', '!':'shell', '@':'load'}


    #TODO: implement getopt bits to support tab-completion

    def do_quit(self,arg):
        '''
        quit ptsh
        '''
        # TODO: save session log, close DB, etc.
        pass
 
 
 
    def do_alias(self,line):
        '''
        alias [newcommand] ["command(s)"] - sets a command or set of commands to a new alias
        '''
        pass
 
    
    def do_workspace(self,line):
        '''
        create or change workspaces.
        
        workspace create [workspace] -- creates new workspace
        workspace delete [workspace] -- deletes a workspace
        workspace [workspace] -- change workspaces
        workspace change [workspace] -- change workspaces.
        workspace  -- shows current workspace
        show workspace -- shows workspaces
        '''
        if line.split('\ ') is 'create':
            print "create workspace"
        elif line.split('\ ') is 'delete':
            print "delete workspace"
        elif line.split('\ ') is 'change':
            print "change workspaces"
        else:
            print "current workspace: %s" % (self.workspace)
  
    @options( [make_option( '-v', '--variables', help="display set variables")],
              [make_option( '-V', '--version', help="show current version information")], 
              )
    def do_show(self,line):
        '''
        show variables - display set variables
        show version - version of ptsh
        show workspace - the current workspace
        '''
        print len(line.split('\ '))
        if len(line) < 1:
            print "show usage"
        elif line.split('\ ')[1] is 'variables':
            print "show variables"
        elif line.split('\ ')[1] is 'version':
            print "ptsh v%s" % ( self.version )
        elif line.split('\ ')[1] is 'workspace':
            print "current workspace: %s" % (self.version)
        else:
            print "unrecognized command."
        pass



    def default( self, line):
        # default handler, but this shouldn't be necessary because of default_to_shell
        pass


shell = PTSH()
shell.cmdloop()