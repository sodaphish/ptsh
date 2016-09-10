#!/usr/bin/python

import sys, os
sys.path.append( '/home/hostedby/python/usr/lib64/python2.3/site-packages/' )
sys.path.append( '/home/hostedby/python/usr/lib/python2.3/site-packages/' )
import adodb
from GameServers import *

def main():
	servers = []
	conn = adodb.NewADOConnection('mysql')
	conn.Connect('localhost', 'hostedby_soda', 'alpha01', 'hostedby_alpha')
	cursor = conn.Execute( 'select * from servers;' )
	while not cursor.EOF:
		arr = cursor.GetRowAssoc(0)
		server = ( "%s:%s" ) % ( arr['serverip'], arr['serverport'] )
		rcon = arr['serverrcon']
		players = int( os.popen( ( "/home/hostedby/www/mine/wc/qstat -R -P -cn -tsw -q3s %s -raw \' \' | grep -v ^game | grep -v ^Q3S | wc -l" ) % ( server ) ).read().rstrip( '\n' ) )
		if players < 5:
			print ( "./rcon.py %s %s rcon set g_respawn 2" ) % ( server, rcon )
		elif players < 11:
			print ( "./rcon.py %s %s rcon set g_respawn 4" ) % ( server, rcon )
		elif players < 15:
			print ( "./rcon.py %s %s rcon set g_respawn 8" ) % ( server, rcon )
		else:
			print ( "./rcon.py %s %s rcon set g_respawn 12" ) % ( server, rcon )
		cursor.MoveNext()
	cursor.Close()
	conn.Close()

if __name__ == '__main__':
	main()

