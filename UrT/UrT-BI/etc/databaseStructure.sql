-- phpMyAdmin SQL Dump
-- version 2.11.8.1deb5+lenny3
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Nov 26, 2009 at 09:21 AM
-- Server version: 5.0.51
-- PHP Version: 5.2.6-1+lenny3

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";

--
-- Database: `urt`
--

-- --------------------------------------------------------

--
-- Table structure for table `bans`
--

CREATE TABLE IF NOT EXISTS `bans` (
  `banID` int(11) NOT NULL auto_increment,
  `type` enum('ban','unban','tmpban') NOT NULL,
  `sessionid` varchar(16) NOT NULL,
  `date` timestamp NOT NULL default CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP,
  `expires` timestamp NULL default NULL,
  `IP` varchar(16) default NULL,
  `playerID` varchar(32) NOT NULL,
  `bannedBy` varchar(32) default NULL,
  `reason` tinytext,
  `notes` tinytext,
  `visible` enum('true','false') default 'true',
  `state` enum('unprocessed','midway','processed') NOT NULL default 'unprocessed',
  PRIMARY KEY  (`banID`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=759 ;

-- --------------------------------------------------------

--
-- Table structure for table `categories`
--

CREATE TABLE IF NOT EXISTS `categories` (
  `catid` int(11) NOT NULL auto_increment,
  `cattitle` varchar(128) NOT NULL,
  `catdescription` tinytext NOT NULL,
  `parent` int(11) default NULL,
  PRIMARY KEY  (`catid`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=4 ;

-- --------------------------------------------------------

--
-- Table structure for table `ips`
--

CREATE TABLE IF NOT EXISTS `ips` (
  `ipID` int(11) NOT NULL auto_increment,
  `ip` varchar(15) NOT NULL,
  `name` varchar(64) NOT NULL,
  `guid` varchar(32) NOT NULL,
  PRIMARY KEY  (`ipID`),
  KEY `ip` (`ip`,`name`,`guid`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=227972 ;

-- --------------------------------------------------------

--
-- Table structure for table `location`
--

CREATE TABLE IF NOT EXISTS `location` (
  `loc_id` int(11) NOT NULL auto_increment,
  `loc_name` varchar(255) NOT NULL default '',
  `loc_desc` text,
  `loc_parent` int(11) NOT NULL default '0',
  `loc_vis` int(2) default '1',
  `loc_public` int(2) default '1',
  PRIMARY KEY  (`loc_id`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=6 ;

-- --------------------------------------------------------

--
-- Table structure for table `motd`
--

CREATE TABLE IF NOT EXISTS `motd` (
  `motdid` int(11) NOT NULL auto_increment,
  `motdAuthor` varchar(64) NOT NULL,
  `motdDate` timestamp NOT NULL default CURRENT_TIMESTAMP,
  `motdBody` text NOT NULL,
  PRIMARY KEY  (`motdid`),
  FULLTEXT KEY `motdBody` (`motdBody`),
  FULLTEXT KEY `motdBody_2` (`motdBody`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=26 ;

-- --------------------------------------------------------

--
-- Table structure for table `playerTrend`
--

CREATE TABLE IF NOT EXISTS `playerTrend` (
  `id` int(11) NOT NULL auto_increment,
  `timestamp` timestamp NOT NULL default CURRENT_TIMESTAMP,
  `playerCount` tinyint(4) NOT NULL,
  PRIMARY KEY  (`id`),
  KEY `timestamp` (`timestamp`,`playerCount`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=2944 ;

-- --------------------------------------------------------

--
-- Table structure for table `posts`
--

CREATE TABLE IF NOT EXISTS `posts` (
  `postid` int(11) NOT NULL auto_increment,
  `postparent` int(11) NOT NULL,
  `postdate` timestamp NOT NULL default CURRENT_TIMESTAMP,
  `postauthor` varchar(64) NOT NULL,
  `posttitle` varchar(128) NOT NULL,
  `postbody` text NOT NULL,
  `views` int(11) NOT NULL,
  PRIMARY KEY  (`postid`),
  FULLTEXT KEY `postauthor` (`postauthor`,`posttitle`,`postbody`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=10045 ;

-- --------------------------------------------------------

--
-- Table structure for table `rchronJobs`
--

CREATE TABLE IF NOT EXISTS `rchronJobs` (
  `jobid` int(11) NOT NULL auto_increment,
  `owner` varchar(64) NOT NULL,
  `cmd` tinytext NOT NULL,
  `interval` int(11) NOT NULL default '1',
  `multiplier` enum('min','hr','day') NOT NULL default 'min',
  `notify` tinytext NOT NULL,
  `enabled` enum('y','n') NOT NULL default 'y',
  PRIMARY KEY  (`jobid`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=7 ;

-- --------------------------------------------------------

--
-- Table structure for table `rchronServers`
--

CREATE TABLE IF NOT EXISTS `rchronServers` (
  `jobid` tinyint(4) NOT NULL,
  `serverid` tinyint(4) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `servers`
--

CREATE TABLE IF NOT EXISTS `servers` (
  `sid` int(11) NOT NULL auto_increment,
  `servername` varchar(128) NOT NULL,
  `serverip` varchar(128) NOT NULL,
  `serverport` int(11) NOT NULL default '27960',
  `serverrcon` varchar(32) NOT NULL,
  `serverftp` varchar(256) NOT NULL,
  `serverlog` varchar(32) NOT NULL default 'games.log',
  PRIMARY KEY  (`sid`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=218 ;

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE IF NOT EXISTS `users` (
  `uid` int(11) NOT NULL auto_increment,
  `username` varchar(32) NOT NULL,
  `password` varchar(32) NOT NULL,
  `privlevel` int(1) NOT NULL default '0',
  PRIMARY KEY  (`uid`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=90 ;