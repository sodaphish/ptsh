-- MySQL dump 8.22
--
-- Host: localhost    Database: fw2
---------------------------------------------------------
-- Server version	3.23.56-log

--
-- Table structure for table 'blocked'
--

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

--
-- Table structure for table 'dddates'
--

CREATE TABLE dddates (
  id int(11) NOT NULL auto_increment,
  date varchar(32) NOT NULL default '',
  PRIMARY KEY  (id),
  KEY date (date)
) TYPE=MyISAM;

--
-- Table structure for table 'leaseinfo'
--

CREATE TABLE leaseinfo (
  id int(11) NOT NULL auto_increment,
  date datetime NOT NULL default '0000-00-00 00:00:00',
  type int(1) NOT NULL default '0',
  ip varchar(32) NOT NULL default '',
  mac varchar(32) NOT NULL default '',
  host varchar(64) default NULL,
  PRIMARY KEY  (id),
  KEY ip (ip),
  KEY mac (mac),
  KEY date (date)
) TYPE=MyISAM;

--
-- Table structure for table 'others'
--

CREATE TABLE others (
  id int(11) NOT NULL auto_increment,
  time varchar(16) NOT NULL default '',
  date varchar(32) NOT NULL default '',
  pixerror varchar(32) NOT NULL default '',
  message text NOT NULL,
  PRIMARY KEY  (id),
  KEY date (date),
  FULLTEXT KEY message (message)
) TYPE=MyISAM;

--
-- Table structure for table 'stats'
--

CREATE TABLE stats (
  id int(11) NOT NULL auto_increment,
  date varchar(32) NOT NULL default '',
  rpt varchar(8) NOT NULL default '',
  data text NOT NULL,
  PRIMARY KEY  (id),
  KEY date (date),
  KEY rpt (rpt)
) TYPE=MyISAM;

