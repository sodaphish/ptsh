#!/bin/sh
# 
# written by C.J. Steele <csteele@good-sam.com> 10 Jan 2003
# 
# this script retireves yesterday's firewall logs and dumps it in DUMPDIR
#
. /var/www/html/fwap/bin/globals

cd $DUMPDIR
wget --http-user=csteele --http-passwd=q1w2e3r4 http://frank.corp.good-sam.com/toaster.corp.good-sam.com/$YESTERDAY
