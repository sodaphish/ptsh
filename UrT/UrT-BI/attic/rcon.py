#!/usr/bin/python
"""
drcon - distributed rcon commando
http://sodaphish.com/wc/
By SodaPhish

Python Quake 3 Library
http://misc.slowchop.com/misc/wiki/pyquake3
Copyright (C) 2006-2007 Gerald Kaszuba
Modified by |ALPHA|SodaPhish 2008
"""

import socket, re, sys, md5, urllib, time
from optparse import OptionParser
sys.path.append( '/home/hostedby/python/usr/lib64/python2.3/site-packages/' )
sys.path.append( '/home/hostedby/python/usr/lib/python2.3/site-packages/' )
import adodb


class GameServer:
	ip = ""
	port = ""
	rcon = ""
	def __init__( self, i, p, r ): 
		self.ip = i
		self.port = p
		self.rcon = r
	def __str__( self ):
		return "%s:%s" % ( self.ip, self.port )
	def getip( self ): 
		return "%s:%s" % ( self.ip , self.port )
	def getrcon( self ): 
		return self.rcon



class Player:
	def __init__( self, name, frags, ping, address=None, bot=-1 ):
		self.name = name 
		self.frags = frags
		self.ping = ping
		self.address = address
		self.bot = bot
	def __str__( self ):
		return self.name
	def __repr__( self ):
		return str( self )



class PyQuake3:
	packet_prefix = '\xff' * 4
	player_reo = re.compile(r'^(\d+) (\d+) "(.*)"')
	def __init__(self, server, rcon_password=''):
		self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.set_server(server)
		self.set_rcon_password(rcon_password)
	def set_server(self, server):
		try:
			#self.address, self.port = server.getip.split(':')
			self.address, self.port = server.split(':')
		except:
			raise Exception('Server address must be in the format of \
					"address:port"')
		self.port = int(self.port)
		self.s.connect((self.address, self.port))
	def get_address(self):
		return '%s:%s' % (self.address, self.port)
	def set_rcon_password(self, rcon_password):
		self.rcon_password = rcon_password
	def send_packet(self, data):
		self.s.send('%s%s\n' % (self.packet_prefix, data))
	def recv(self, timeout=1):
		self.s.settimeout(timeout)
		try:
			return self.s.recv(4096)
		except socket.error, e:
			raise Exception('Error receiving the packet: %s' % \
					e[1])
	def command(self, cmd, timeout=1, retries=3):
		while retries:
			self.send_packet(cmd)
			try:
				data = self.recv(timeout)
			except:
				data = None
			if data:
				return self.parse_packet(data)
			retries -= 1
		raise Exception('Server response timed out')
	def rcon(self, cmd):
		r = self.command('rcon "%s" %s' % (self.rcon_password, cmd))
		if r[1] == 'No rconpassword set on the server.\n' or r[1] == \
				'Bad rconpassword.\n':
			raise Exception(r[1][:-1])
		return r
	def parse_packet(self, data):
		if data.find(self.packet_prefix) != 0:
			raise Exception('Malformed packet')
		first_line_length = data.find('\n')
		if first_line_length == -1:
			raise Exception('Malformed packet')
		response_type = data[len(self.packet_prefix):first_line_length]
		response_data = data[first_line_length+1:]
		return response_type, response_data
	def parse_status(self, data):
		split = data[1:].split('\\')
		values = dict(zip(split[::2], split[1::2]))
		# if there are \n's in one of the values, it's the list of players
		for var, val in values.items():
			pos = val.find('\n')
			if pos == -1:
				continue
			split = val.split('\n', 1)
			values[var] = split[0]
			self.parse_players(split[1])
		return values
	def parse_players(self, data):
		self.players = []
		for player in data.split('\n'):
			if not player:
				continue
			match = self.player_reo.match(player)
			if not match:
				print 'couldnt match', player
				continue
			frags, ping, name = match.groups()
			self.players.append(Player(name, frags, ping))
	def update(self):
		cmd, data = self.command('getstatus')
		self.vars = self.parse_status(data)
	def rcon_update(self):
		cmd, data = self.rcon('status')
		lines = data.split('\n')
		players = lines[3:]
		self.players = []
		for p in players:
			while p.find('  ') != -1:
				p = p.replace('  ', ' ')
			while p.find(' ') == 0:
				p = p[1:]
			if p == '':
				continue
			p = p.split(' ')
			try:
				self.players.append(Player(p[3][:-2], p[0], p[1], p[5], p[6]))
			except:
				# for whatever reason, some shit hit the fan here.
				self.players.append( Player( "", "", 'None', "") )


def main():
	print "rcon %s -- python RCON client" % ( VERSION )
	print "...by |ALPHA|SodaPhish <sodaphish@gmail.com>\n" 

	parser = OptionParser()
	(options, args ) = parser.parse_args()

	server = args[0]
	rcon = args[1]
	cmd = ''
	for a in args[2:]:
		cmd += a
		cmd += ' '
	
	if not DEBUG: 
		try:
			q = PyQuake3( server, rcon )
			#print '%s on %s' % ( q.rcon( cmd )[-1].rstrip('\n'), server )
			#time.sleep( .75 )
			#print '%s on %s' % ( q.rcon( cmd )[-1].rstrip('\n'), server )
			print q.rcon( cmd )
		except:
			print "E: couldn\'t execute '%s' on %s" % ( cmd, server )
	else:
		print "D: exec '%s' on %s" % ( cmd, server )

if __name__ == '__main__':
	VERSION = "0.1.0"
	DEBUG = 0
	main()
