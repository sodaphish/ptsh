create table if not exists users (
	uid		int auto_increment,
	usernmae	varchar(32) not null,
	password	varchar(32) not null,
	privlevel	int(1) not null default '0',
	primary key (uid)
) TYPE=MyISAM;

create table if not exists servers (
	sid 	int(11) not null auto_increment,
	primary key (sid),
	servername	varchar(128) not null,
	serverport	int(2) not null default '27960',
	serverip 		varchar(128) not null,
	serverrcon	varchar(32) not null,
	serverftp		varchar(255) not null
) TYPE=MyISAM;

