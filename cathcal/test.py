#!/usr/bin/python3

import sys
sys.path.append( "~/.python/usr/local/lib/python3.2" )

import datetime
from datetime import *
from dateutil import parser
import cathcal
from cathcal.calendar import RomanCalendar1962
from cathcal.breviary import Breviary

if __name__ == '__main__':
	b = Breviary()
	#timeobj = datetime.time(datetime.now())
	print(datetime.now())
	print("office:      %s" % b.office())
	print("season:      %s" % b.season())
	print("feast:       %s" % b.feast())
	print("readings:    %s" % b.get_readings())
	#print ("{\"office\":\"%s\",\"season\":\"%s\",\"feast\":\"%s\",\"readings\":\"%s\"}")%(b.office(),b.season(),b.feast(),b.get_readings())
	
