"""
@author: SodaPhish <sodaphish@protonmail.ch>
"""


import sys 
from cmd2 import Cmd

try:
    from Global import *
except Exception as e:
    print "splib at shit and died, fix it!"
    sys.exit(1)



class PTSH(Cmd):
    prompt = 'ptsh> '
    default_to_shell = True #this won't work for logging stuff.
    echo = False

    shortcuts = {'?':'help', '!':'shell', '@':'load'}

    def do_quit(self,arg):
        '''
        quit ptsh
        '''
        # TODO: save session log, close DB, etc.
        return True
 
 
 
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
        pass
  
    
    def do_show(self,line):
        '''
        show variables - display set variables
        show version - version of ptsh
        show workspace - the current workspace
        '''
        pass



    def default( self, line):
        # default handler, but this shouldn't be necessary because of default_to_shell
        pass


shell = PTSH()
shell.cmdloop()