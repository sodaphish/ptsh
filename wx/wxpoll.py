import sys, urllib, time
sys.path.append( '/home/hostedby/python/usr/lib/python2.4/site-packages' )
import pywapi
sys.path.append( '/home/hostedby/python/usr/lib64/python2.4/site-packages' )
from pysqlite2 import dbapi2 as sqlite3

__debug = False

try:
	obs = pywapi.get_weather_from_noaa( "KFSD" )
except Exception, e:
	print "Weather retrieval error! (%s)" % e[0]

if __debug:
	for key in obs:
		print "%s: %s" % ( key, obs[key] )


try:
	# setup our database connection
	conn = sqlite3.connect( '/home3/hostedby/public_html/mine/files/wx.db' )
	sql = conn.cursor()
	sql.execute( "CREATE TABLE IF NOT EXISTS observation \
		(date VARCHAR(32), \
		station VARCHAR(8), \
		temp NUMERIC(3,2), \
		dewpoint NUMERIC(3,2), \
		humidity NUMERIC(3,2), \
		pressure NUMERIC(3,2), \
		windir VARCHAR(16), \
		windspd NUMERIC(3,2) )" )

	insert_stmt = "INSERT INTO observation ( date, station, temp, dewpoint, humidity, pressure, windir, windspd ) VALUES ( '%s', '%s', %0.2f, %0.2f, %0.2f, %0.2f, '%s', %0.2f )" % \
		(time.strftime( '%Y-%m-%d %H:%M:%S', time.gmtime() ), obs['station_id'], float(obs['temp_f']), float(obs['dewpoint_f']), float(obs['relative_humidity']), float(obs['pressure_in']), obs['wind_dir'], float(obs['wind_mph']))

	sql.execute( insert_stmt )

	if __debug:
		print insert_stmt
		print "observation inserted as: " % sql.lastrowid

	conn.commit()
	conn.close()
except TypeError, t:
	pass
except Exception, e:
	print "Error! (%s)" % e[0]
	
print "done."
