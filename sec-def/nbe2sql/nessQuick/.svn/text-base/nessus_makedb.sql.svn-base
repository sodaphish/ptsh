# These sql commands will create the Nessus database, table, and schema
# to be used for .nbe file imports
#
create database nessus;
use nessus;
#
# Table structure for table 'nessus'
#
CREATE TABLE results (
	id		int(11)		DEFAULT '0' NOT NULL auto_increment,
	domain		varchar(40)	DEFAULT '' NOT NULL,
	host		varchar(40)	DEFAULT '' NOT NULL,
	service		varchar(40)	DEFAULT '' NOT NULL,
	scriptid	varchar(40)	DEFAULT '' NOT NULL,
	risk		varchar(40)	DEFAULT '' NOT NULL,
	msg		text,
	PRIMARY		KEY		(id),
	KEY		host		(host),
	KEY		host_2		(host,service)
	);
#
#
# +----------+-------------+-----+---------------------+----------------+
# | Field    | Type        | Key | Default             | Extra          |
# +----------+-------------+-----+---------------------+----------------+
# | id       | int(11)     | PRI | 0                   | auto_increment |
# | rectype  | varchar(10) |     |                     |                |
# | domain   | varchar(40) |     |                     |                |
# | host     | varchar(40) | MUL |                     |                |
# | service  | varchar(40) |     |                     |                |
# | scriptid | varchar(40) |     |                     |                |
# | risk     | varchar(40) |     |                     |                |
# | msg      | text        |     | NULL                |                |
# +----------+-------------+-----+---------------------+----------------+
#
#
#
#
CREATE TABLE timestamps (
	id		int(11)		DEFAULT '0' NOT NULL auto_increment,
	unused		varchar(40)	DEFAULT '' NOT NULL,
	host		varchar(40)	DEFAULT '' NOT NULL,
	progress	varchar(40)	DEFAULT '' NOT NULL,
	timestamp	varchar(40)		DEFAULT '0000-00-00 00:00:00' NOT NULL,
	PRIMARY		KEY		(id),
	KEY		host		(host)	);
#
#
# +----------+-------------+-----+---------------------+----------------+
# | Field    | Type        | Key | Default             | Extra          |
# +----------+-------------+-----+---------------------+----------------+
# | id       | int(11)     | PRI | 0                   | auto_increment |
# | rectype  | varchar(10) |     |                     |                |
# | unused   | varchar(40) |     |                     |                |
# | host     | varchar(40) | MUL |                     |                |
# | progress | varchar(40) |     |                     |                |
# | timestamp| varchar(40) |     |                     |                |
# +----------+-------------+-----+---------------------+----------------+
