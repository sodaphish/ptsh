create table if not exists project (
	id 	int(11) auto_increment,
	title	varchar(128) not null,
	due_date	varchar(10),
	start_date	varchar(10),
	description	text not null,
	active		int(2) default '1',
	primary key ( id )
)\g

create table if not exists timecard (
	id int(11) auto_increment,
	project_id int(11) not null,
	date varchar(10),
	description text not null,
	hours int(8) not null,
	employee varchar(64),
	active int(2) default '1',
	primary key(id)
	)\g

create table if not exists client (
	id int(11) auto_increment,
	company_name varchar(128) not null,
	contact varchar(128) not null,
	address1 varchar(128) not null,
	address2 varchar(128),
	city varchar(128) not null,
	state varchar(32) not null,
	zip varchar(24) not null,
	telephone varchar(16) not null,
	email varchar(255),
	fax varchar(16),
	www varchar(255),
	active int(2) default '1',
	primary key(id)
	)\g

create table if not exists line_items (
	id int(11) auto_increment,
	invoice_id int(11) not null,
	description varchar(255) not null,
	qty int(4) not null,
	date varchar(16) not null,
	price float(6,2) not null,
	active int(2) default '1',
	primary key(id)
)\g

create table if not exists invoice(
	id int(11) auto_increment,
	date varchar(16) not null,
    due_date varchar(16) not null,
	client int(11) not null,
	project_id int(11),
	note text,
	status int(4) default '0',
	active int(2) default '1',
	primary key(id)
)\g
