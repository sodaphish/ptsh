CREATE TABLE IF NOT EXISTS infosec_mail (
	id		int(11) auto_increment not null primary key,
	frm		text not null,
	dt		text not null,
	sbj		text not null,
	msg		longtext not null,
	-- flag to indicate whether or not the the msg has been processed
	processed int(2) default '0'
)\g

-- infosec_mail_queries
-- this table stores information on the queries we will make of the 
-- infosec_mail table.
CREATE TABLE IF NOT EXISTS infosec_mail_queries (
	id			int(11) auto_increment not null primary key,
	-- the phpbb user ID that we're associating with this query.
	uid			int(11) not null,
	-- keyphrase is the exact phrase we're looking for 
	keyphrase	varchar(255) not null,
	-- method will eventually be representative of different modes
	-- of delivery to be used.  for now, the known methods are:
	-- 		0 - e-mail
	-- 		1 - icq
	-- 		2 - irc
	method		int(4) default '0', 
	-- mode is an indicator of the frequency the updates are to be 
	-- provided.  currently known modes are: 
	-- 		0 - individually
	-- 		1 - batched daily
	mode		int(4) default '0', 
	-- prefs is used to indicate formatting preferences.
	-- 		0 - plaintext
	--		1 - html
	--		2 - xml
	prefs		int(4) default '0',
	-- active indicates whether or not this query is to be processed
	active		int(1) default '1'
)\g
