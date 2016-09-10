import cathcal
from datetime import *
import string


class Verse():
	
	def __init__(self,verse):
		self.chapter = 1
		self.verse_start = 1
		self.verse_end = 1


	def get_chapter(self,verse):
		parts = list()
		parts = string.split(verse,":",2)
		return parts[1]
		

	def get_verse(self,verse):
		parts = list()
		parts = string.split(verse,":",2)
		verse = parts[1]
		parts2 = list()
		parts2 = string.split(verse,"-",2)
		return parts2




class PiusXPsalter():
	"""PiusXPsalter
	class to provide interface to the prayers according to the Pius X rubrics for the breviary.

	A couple of rules:
	1) Lauds 1 is celebrated on all sundays and ferias except from Septuagesima until the second Sunday in Passiontide
	2) Lauds 2 is used on Sundays and Ferias of Advent until the vigil of Christmas, and from Septuagesima until Monday of Holy Week inclusive
	3) 
	"""
	_nocturn1 = { 'Sunday':'1,2,3', 'Monday':'13,14,16', 'Tuesday':'34:1-10,34:11-17,34:18-28', 'Wednesday':'44:1-10,44:11-18,45', 'Thursday':'61,65:1-12,65:13-20', 'Friday':'77:1-8,77:9-16,77:17-31', 'Saturday':'104:1-15,104:16-27,104:28-45' }
	_nocturn2 = { 'Sunday':'8,9:1-11,9:12-21', 'Monday':'17:1-16,17:17-31,17:32-51', 'Tuesday':'36:1-15,36:16-29,36:30-40', 'Wednesday':'47,48:1-13,48:14-20', 'Thursday':'67:1-11,67:12-24,67:25-36', 'Friday':'77:32-39,77:40-55,77:56-72', 'Saturday':'105:1-18,105:19-33,105:34-48' }
	_nocturn3 = { 'Sunday':'9:1-12,9:13-18,10', 'Monday':'19,20,29', 'Tuesday':'37:1-13,37:14-23,38', 'Wednesday':'49:1-15,49:16-23,50', 'Thursday':'68:1-13,68:14-29,68:30-27', 'Friday':'78,80,82', 'Saturday':'106:1-16,106:17-32,106:33-43' }
	_lauds1 =   { 'Sunday':'92,99,62,Benedicite_omnia,148', 'Monday':'46,5,28,Benedictus_es,116', 'Tuesday':'95,42,66,Magnus_es,134', 'Wednesday':'96,64,100,Incipite_Domino,145', 'Thursday':'97,89,35,Audite_verbum_Domini,146', 'Friday':'98,142,84,Vere_tu_es,147', 'Saturday':'149,91,63,Miserere_nostri,150' }
	_lauds2 =   { 'Sunday':'50,117,62,Benedictus_es,148', 'Monday':'50,5,28,Gratias_ago_tibi,116', 'Tuesday':'50,42,66,Ego_dixi,134', 'Wednesday':'50,64,100,Exultat_cor_meum,145', 'Thursday':'50,89,35,Cantabo_Domino,146', 'Friday':'50,142,84,Domine_audivi,147', 'Saturday':'50,91,63,Ascultate_caeli,150' }
	_prime =    { 'Sunday':'117,118:1-16,118:17-32', 'Monday':'23,18:1-7,18:8-15', 'Tuesday':'24:1-7,24:8-14,24:15-22', 'Wednesday':'25,51,52', 'Thursday':'22,71:1-7,71:8-19', 'Friday':'21:1-12,21:13-22,21:23-32', 'Saturday':'93:1-11,93:12-23,107' }
	_terce =    { 'Sunday':'118:33-48,118:49-64,118:65-80', 'Monday':'26:1-7,26:7-14,27', 'Tuesday':'39:1-9,39:10-13,39:14-18', 'Wednesday':'53,54:1-15,54:16-24', 'Thursday':'72:1-9,72:10-17,72:18-28', 'Friday':'79:1-8,79:9-20,81', 'Saturday':'101:1-12,101:13-23,101:24-29' }
	_sext =     { 'Sunday':'119:81-96,118:97-112,118:113-128', 'Monday':'30:1-9,30:10-19,30:20-25', 'Tuesday':'40,41:1-6,41:7-12', 'Wednesday':'55,56,57', 'Thursday':'73:1-9,73:10-17,73:17-23', 'Friday':'83:1-8,83:9-13,86', 'Saturday':'103:1-12,103:13-23,103:24-35' }
	_none =     { 'Sunday':'118:129-144,118:145-160,118:161-176', 'Monday':'31,32:1-12,32:13-22', 'Tuesday':'43:1-9,43:10-17,43:18-26', 'Wednesday':'58:1-11,58:11-18,59', 'Thursday':'74,75:1-7,75:8-13', 'Friday':'88:1-19,88:20-38,88:39-53', 'Saturday':'108:1-10,108:11-19,108:20-31' }
	_vespers =  { 'Sunday':'109,110,111,112,113', 'Monday':'114,115,119,120,121', 'Tuesday':'122,123,124,125,126', 'Wednesday':'127,128,129,130,131', 'Thursday':'132,135:1-9,135:10-26,136,137', 'Friday':'138:1-12,138:13-24,139,140,141', 'Saturday':'143:1-8,143:9-15,144:1-7,144:8-13,144:13-21' }
	_compline = { 'Sunday':'4,90,133', 'Monday':'6,7:1-10,7:11-18', 'Tuesday':'11,12,15', 'Wednesday':'33:1-11,33:12-23,60', 'Thursday':'69,70:1-12,70:13-24', 'Friday':'76:1-13,76:14-21,85', 'Saturday':'87,102:1-12,102:13-22' }


	def __init__(self,thistime=datetime.now()):
		#return self.get_readings(thistime)
		pass


	def get_readings(self, thistime=datetime.now()):
		curtime = datetime.time(thistime)
		curdate = datetime.date(thistime)

		if curtime >= time(18,0,0) and curtime < time(21,0,0):
			return self._vespers[curdate.strftime('%A')]
		elif curtime >= time(21,0,0) and curtime < time(0,0,0):
			return self._compline[curdate.strftime('%A')]
		elif curtime >= time(0,0,0) and curtime < time(3,0,0):
			return self._nocturn3[curdate.strftime('%A')]
		elif curtime >= time(3,0,0) and curtime < time(6,0,0):
			if curdate.strftime('%A') is 'Sunday':
				return self._lauds1[curdate.strftime('%A')]
			else:
				return self._lauds2[curdate.strftime('%A')]
		elif curtime >= time(6,0,0) and curtime < time(9,0,0):
			return self._prime[curdate.strftime('%A')]
		elif curtime >= time(9,0,0) and curtime < time(12,0,0):
			return self._terce[curdate.strftime('%A')]
		elif curtime >= time(12,0,0) and curtime < time(15,0,0):
			return self._sext[curdate.strftime('%A')]
		elif curtime >= time(15,0,0) and curtime < time(18,0,0):
			return self._none[curdate.strftime('%A')]
		else:
			return None
