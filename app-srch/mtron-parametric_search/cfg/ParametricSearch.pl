


#!/usr/bin/perl
# filename: ParametricSearch.pl
# (C)opyright 1999, M-tron Industries, Inc., all rights reserved.
# 	written by Corey J. Steele <csteele@mtron.com>
# last modified: 12/15/2000
#
# Description: the variables outlined herein are specific to the Parametric
#	Search code.  They should not be needed by any other applications.
#
use Env;
use CGI;
use lib qw( ../lib );
use ParseLib;

Tokenize( 'HELP_SUB_TOPIC', "" );

Tokenize( '__VERSION', "1.1.0-0" );

$main::__remoteHost = $ENV{'REMOTE_ADDR'};
$main::__remoteHost = $ENV{'REMOTE_HOST'} if( $main::__remoteHost eq "" );
$main::__remoteHost = 'localhost' if( $main::__remoteHost eq "" ); 

#
# this variable controls flow of the program... 
$main::__func = CGI::param( "f" );
	Tokenize( 'FUNCTION', $main::__func );

#
# debug level ranges from one to five, five is most verbose
$main::__DEBUG_LEVEL = 2;

#
# __maxNumView tells the searches how many results to display per screen
$main::__maxNumView = 25;

#
# $log_file is the location of the parametric search's logs
$log_file = "/home/httpd/html/parametric.log"; 

#
# these are the people to be e-mailed by the feedback.cgi script
@main::feedback_recipients = ( "csteele\@mtron.com, billjnwn\@mtron.com, sluchtel\@mtron.com" ); 

#
# these are the people to be e-mailed by the contact.cgi script
@main::contact_recipients = ( "csteele\@mtron.com, billjnwn\@mtron.com, sluchtel\@mtron.com" );
