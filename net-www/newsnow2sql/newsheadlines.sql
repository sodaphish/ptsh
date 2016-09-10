CREATE TABLE IF NOT EXISTS newsheadlines (
	url varchar( 255 ) not null unique,
	date timestamp not null,
	title varchar( 255 ) not null,
	source varchar( 128 ) not null,
	procd enum('true','false') default 'false'
)\g
