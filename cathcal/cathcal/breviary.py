import datetime
from datetime import datetime
from datetime import timedelta
from datetime import date
from datetime import time
import dateutil
from dateutil import easter

import cathcal
from cathcal.psalter import PiusXPsalter
from cathcal.calendar import RomanCalendar1962


class Breviary():
	calendar = None


	def __init__(self,year=datetime.now().year):
		self.calendar= RomanCalendar1962(year)


	def office(self, thistime=datetime.time(datetime.now())):
		if thistime >= time(18,0,0) and thistime < time(21,0,0):
			return "Vespers"
		if thistime >= time(21,0,0) and thistime < time(0,0,0):
			return "Compline"
		if thistime >= time(0,0,0) and thistime < time(3,0,0):
			return "Matins"
		if thistime >= time(3,0,0) and thistime < time(6,0,0):
			return "Lauds"
		if thistime >= time(6,0,0) and thistime < time(9,0,0):
			return "Prime"
		if thistime >= time(9,0,0) and thistime < time(12,0,0):
			return "Terce"
		if thistime >= time(12,0,0) and thistime < time(15,0,0):
			return "Sext"
		if thistime >= time(15,0,0) and thistime < time(18,0,0):
			return "None"


	def season(self, thistime=date(datetime.now().year, datetime.now().month, datetime.now().day), verbose=False):
		"""season()
		returns the liturgical season based off the current time or a supplied date/time
		"""
		if verbose:
			if self.calendar.get_feast() is not 'Feria':
				return "%s (feast of %s)"%(self.calendar.get_season(thistime),self.calendar.get_feast(thistime))
			else:
				return "%s (%s)"%(self.calendar.get_season(thistime),self.calendar.get_feast(thistime))
		else:
			if self.calendar.get_feast() is not 'Feria':
				return "%s"%(self.calendar.get_season(thistime))
			else:
				return "%s"%(self.calendar.get_season(thistime))


	def feast(self, thistime=date(datetime.now().year, datetime.now().month, datetime.now().day)):
		"""feast()
		"""
		if self.calendar.get_feast() is not 'Feria':
			return "feast of %s"%(self.calendar.get_feast(thistime))
		else:
			return "%s"%(self.calendar.get_feast(thistime))
		


	def full_office(self, thistime=date(datetime.now().year, datetime.now().month, datetime.now().day)):
		"""full_office
		takes an optional datetime.time parameter, or uses the current time to 
		return a string with the office, season and appropriate feast
		"""
		return "Office of %s for %s in %s (%s)"%(self.office(), thistime.strftime("%A"), self.calendar.get_season(thistime),self.calendar.get_feast(thistime))
		"""
		if self.calendar.feast_day is not 'Feria':
			return "office of %s for %s in %s (feast of %s)"%(self.office(), datetime.now().strftime("%A"), self.calendar.get_season(thistime),self.calendar.get_feast(thistime))
		else:
			return "office of %s for %s in %s (%s)"%(self.office(), datetime.now().strftime("%A"), self.calendar.get_season(thistime),self.calendar.get_feast(thistime))
		"""

	def get_readings(self,thisdate=datetime.now()):
		return PiusXPsalter().get_readings(thisdate)
		

		 
#EOF
