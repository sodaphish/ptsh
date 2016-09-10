import os
from os.path import join
from shutil import *
import win32file
import win32con

#TODO: handle differential or full backups via command-line switch

toBackup = []
#TODO: whack trailing '\' chars, or it blows-up python
toBackup.append( os.path.abspath("z:\docs" ) )

fileList = []

for directory in toBackup:
    try:
        for root, dirs, files in os.walk( directory ):
            for file in files:
                #TODO: check the archive bit and if its on, add it to the archive
                if bool( win32file.GetFileAttributes(file) & win32con.FILE_ATTRIBUTE_ARCHIVE):
                    fileList.append( join( root, file ) )
    except:
        print( "oops:", directory )

for file in fileList:
    print( file )
    
#should now have a full list of all the crap to backup... DO IT!
