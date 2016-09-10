create table invoices (
	id			int(11) auto_increment not null,
	client		int(11) not null,
	date		varchar(64) not null,
	paid		tinyint default '0',
	taxrate		float(2,3) default '6.000',
	notes		mediumtext,
	primary key ( id )
)\g

create table lineitems (
	id			int(11) auto_increment not null,
	invoice		int(11) not null,
	descr		varchar(255) not null,
	quantity	float(4,2) default '1.00',
	price		float(8,2) not null,
	primary key ( id )
)\g

create table clients (
	id			int(11) auto_increment not null,
	name		varchar(128) not null,
	address1	varchar(128) not null,
	address2	varchar(128),
	city		varchar(64) not null,
	state		varchar(32) not null,
	zip			varchar(16) not null,
	phone		varchar(32) not null,
	fax			varchar(32) not null,
	contact		varchar(128) not null,
	email		varchar(128) not null,
	visible		int(2) default '1',
	primary key ( id )
)\g
