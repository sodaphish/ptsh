#!/bin/sh
# getlog.sh v.0.1.0 by C.J. Steele <csteele@good-sam.com>
# 	10 Jan 2003
# 
# this script retireves yesterday's firewall logs via http and puts them in to DUMPDIR
#


# import our globals
. /var/www/html/fwap/bin/globals

cd $DUMPDIR
wget --http-user=csteele --http-passwd=q1w2e3r4 http://frank.corp.good-sam.com/toaster.corp.good-sam.com/$YESTERDAY
