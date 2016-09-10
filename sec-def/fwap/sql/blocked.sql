CREATE TABLE blocked (
  id int(11) NOT NULL auto_increment,
  time varchar(16) NOT NULL default '',
  date varchar(32) NOT NULL default '',
  proto varchar(16) NOT NULL default '',
  src varchar(64) NOT NULL default '',
  srcprt varchar(16) NOT NULL default '',
  dst varchar(64) NOT NULL default '',
  dstprt varchar(16) NOT NULL default '',
  PRIMARY KEY  (id),
  KEY src (src),
  KEY dst (dst),
  KEY date (date)
) TYPE=MyISAM;
