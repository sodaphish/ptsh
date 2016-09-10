#!/bin/sh
#
# ftpbackup.sh v.0.1.0
# (C)opyright 2003, C.J. Steele <coreyjsteele@yahoo.com>, all rights reserved.
# 
# This is a shell script that backsup specified directories and files,
# compresses the archive and uploads it to a specified server via the ftp 
# protocol.  
#
# TODO/ROADMAP:
#	- time/date stamp archives (v.0.2.0)
# 

# directories and/or files you want backed up.
TARGETS="/var/www /home/csteele /home/asteele"

# information on where you want your backups put.
RMT_HOST="hostname"
RMT_USER="username"
RMT_PASSWD="password"


TMPFILE=`mktemp /shared/backup/filesystems.XXXXXX`
tar -cvf $TMPFILE.tar $DIRS
gzip $TMPFILE.tar

# put the backup on the server
ncftpput -u $RMT_USER -p $RMT_PASSWD $RMT_HOST $TMPFILE.tar.gz ./

# delete the backup file
rm -rf $TMPFILE.tar.gz
