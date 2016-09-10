import calendar
from math import cos, sin, acos as arccos, asin as arcsin, tan as tg, degrees, radians


def mod(a,b):
	return a % b

def isLeapYear(year):
	return (year % 4 == 0 and year % 100 != 0) or year % 400 == 0

def getDayNumber(year, month, day):
	cnt = 0
	for t in range(1900,year):
		if isLeapYear(t):
			cnt += 366
		else:
			cnt += 365
			for t in range(1,month):
				cnt += calendar.monthrange(2014, 2)[1]
	return cnt + day + 1

def getHHMMSS(h,tz):
	hh = int(h) 
	mm = (h - hh) * 60
	ss = int(0.5 + (mm - int(mm)) * 60)
	hh = hh + tz
	return "{0:2d}:{1:02d}:{2:02d}" . format(hh, int(mm), ss)


# based on: http://www.srrb.noaa.gov/highlights/sunrise/calcdetails.html 
def getSunriseAndSunset(lat, lon, dst, year, month, day):
	localtime = 12.00
	b2 = lat
	b3 = lon
	b4 = dst
	b5 = localtime / 24
	b6 = year
	d30 = getDayNumber(year, month, day)
	e30 = b5
	f30 = d30 + 2415018.5 + e30 - b4 / 24
	g30 = (f30 - 2451545) / 36525
	q30 = 23 + (26 + ((21.448 - g30 * (46.815 + g30 * (0.00059 - g30 * 0.001813)))) / 60) / 60
	r30 = q30 + 0.00256 * cos(radians(125.04 - 1934.136 * g30))
	j30 = 357.52911 + g30 * (35999.05029 - 0.0001537 * g30)
	k30 = 0.016708634 - g30 * (0.000042037 + 0.0000001267 * g30)
	l30 = sin(radians(j30)) * (1.914602 - g30 * (0.004817 + 0.000014 * g30)) + sin(radians(2 * j30)) * (0.019993 - 0.000101 * g30) + sin(radians(3 * j30)) * 0.000289
	i30 = mod(280.46646 + g30 * (36000.76983 + g30 * 0.0003032), 360)
	m30 = i30 + l30
	p30 = m30 - 0.00569 - 0.00478 * sin(radians(125.04 - 1934.136 * g30))
	t30 = degrees(arcsin(sin(radians(r30)) * sin(radians(p30))))
	u30 = tg(radians(r30 / 2)) * tg(radians(r30 / 2))
	v30 = 4 * degrees(u30 * sin(2 * radians(i30)) - 2 * k30 * sin(radians(j30)) + 4 * k30 * u30 * sin(radians(j30)) * cos(2 * radians(i30)) - 0.5 * u30 * u30 * sin(4 * radians(i30)) - 1.25 * k30 * k30 * sin(2 * radians(j30)))
	w30 = degrees(arccos(cos(radians(90.833)) / (cos(radians(b2)) * cos(radians(t30))) - tg(radians(b2)) * tg(radians(t30))))
	x30 = (720 - 4 * b3 - v30 + b4 * 60) / 1440
	x30 = (720 - 4 * b3 - v30 + b4 * 60) / 1440
	y30 = (x30 * 1440 - w30 * 4) / 1440
	z30 = (x30 * 1440 + w30 * 4) / 1440
	sunrise = y30 * 24
	sunset = z30 * 24
	return (sunrise, sunset)


def moon_phase(month, day, year):
	ages = [18, 0, 11, 22, 3, 14, 25, 6, 17, 28, 9, 20, 1, 12, 23, 4, 15, 26, 7]
	offsets = [-1, 1, 0, 1, 2, 3, 4, 5, 7, 7, 9, 9]
	description = ["new (totally dark)",
	"waxing crescent (increasing to full)",
	"in its first quarter (increasing to full)",
	"waxing gibbous (increasing to full)",
	"full (full light)",
	"waning gibbous (decreasing from full)",
	"in its last quarter (decreasing from full)",
	"waning crescent (decreasing from full)"]
	months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
	if day == 31:
		day = 1
	days_into_phase = ((ages[(year + 1) % 19] + ((day + offsets[month-1]) % 30) + (year < 1900)) % 30)
	index = int((days_into_phase + 2) * 16/59.0)
	if index > 7:
		index = 7
	status = description[index]
	# light should be 100% 15 days into phase
	light = int(2 * days_into_phase * 100/29)
	if light > 100:
		light = abs(light - 200);
	date = "%d%s%d" % (day, months[month-1], year)
	return date, status, light
	
if __name__ == '__main__': 
	month = 11
	day = 30
	year = 2015  
	lat = 43.4644521
	lon = -96.8452291
	dst = 1
	tz=-7

	(sunrise, sunset) = getSunriseAndSunset(lat, lon, dst, year, month, day)
	date, status, light = moon_phase(month, day, year)

	print "%s" % ( date )
	print "sunrise: %s" % (getHHMMSS(sunrise,tz))
	print "sunset: %s" % (getHHMMSS(sunset,tz))
	print "lunar phase: %s @ %d%% light" % (status,light)
