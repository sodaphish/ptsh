create database if not exists bobfus;
use bobfus;
create table if not exists submissions (
	id			int(11) not null auto_increment, 
	reqtime		timestamp(14) not null,
	ipadd		varchar(16) not null,
	url			varchar(256) not null,
	email		varchar(128) not null, 
	passwd		varchar(32) not null,
	status 		int(2) default '0',
	sn			char(16) unique,
	primary key( id )
)\g
