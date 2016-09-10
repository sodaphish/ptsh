#!/usr/bin/python

class Coord: 
	lat = float( 0 )
	lon = float( 0 )

	def __init__( self, lat = 0, lon = 0 ):
		self.lat = lat
		self.lon = lon



class Site:
	ws = float( 0 )
	dv = float( 0 )

	def __init__( self, distance = 1, speed = 0 ):
		self.dv = distance
		self.ws = speed



A = Site( 5, 7 )
B = Site( 25, 20 )
C = Site( 12, 18 )

a = ( float( A.dv ) * -1 / ( float( A.dv ) + float( B.dv ) ) ) * float( A.ws )
b = ( float( B.dv ) * -1  / ( float( A.dv ) + float( B.dv ) ) ) * float( B.ws )

a = ( ((( A.dv + B.dv ) / A.dv ) * A.ws ) + ((( A.dv + B.dv ) / B.dv ) / B.ws ) ) / ( 2 * ( A.dv + B.dv ) )

print a
print b
