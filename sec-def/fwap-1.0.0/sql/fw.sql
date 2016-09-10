CREATE TABLE IF NOT EXISTS blocked (
	id		int(11) auto_increment not null,
	time	varchar(16) not null,
	date	varchar(32) not null,
	proto	varchar(16) not null,
	src		varchar(64) not null,
	srcprt	varchar(16) not null,
	dst		varchar(64) not null,
	dstprt	varchar(16) not null,
	key( src ),
	key( dst ),
	key( date ),
	primary key( id )
)\g

CREATE TABLE IF NOT EXISTS others (
	id			int(11) auto_increment not null,
	time		varchar(16) not null,
	date		varchar(32) not null,
	pixerror	varchar(32) not null,
	message		text not null,
	key( date ),
	fulltext index( message ),
	primary key( id )
)\g

CREATE TABLE IF NOT EXISTS stats (
	id 			int(11) auto_increment not null,
	date		varchar(32) not null,
	rpt			varchar(8) not null,
	data		text not null,
	key( date ),
	key( rpt ),
	primary key( id )
)\g
