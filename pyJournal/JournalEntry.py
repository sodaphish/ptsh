#!/usr/bin/env python

class JournalEntry:

	entryTitle = ''
	entryEntry = ''
	entryTimeStamp = 0

	def __init__( self, title, entry ):
		self.set_entryTitle( title )
		self.set_entryEntry( title )
		self.set_entryTimeStamp( asctime() )

	
	def set_entryTitle( self, title ):
	def set_entryEntry( self, entry ):
	def set_entryTimeStamp( self, timeStamp ):

