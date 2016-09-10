#!/usr/bin/perl
# filename: index.cgi
# (C)opyright 1999-2000, M-tron Industries, Inc., all rights reserved.
#	written by Corey J. Steele <csteele@mtron.com>
# last modified: 12/12/2000
# 
# Description: this controls the flow of the Parametric Search.  You should
#	need to do increadibly little with this routine.  In fact, don't change
# 	this unless you know absolutely what your'e doing.  No, really, get out!
print "Content-type: text/html", "\n\n";

BEGIN {
	use CGI::Carp qw( fatalsToBrowser );
	use CGI;
	use Time::HiRes qw( gettimeofday ); 
	use lib qw( lib cfg );
	use ParseLib;
	use NewLog;
	use Search;
	require "ParametricSearch.pl";
}

$t0 = gettimeofday;

Tokenize( 'ELAPSED_TIME', "" );

LoadTemplate( "content/layout.tmpl" );


Tokenize( 'HELP_TOPIC', "Searching" ); #this is default, change if need be.
Tokenize( 'HELP_TOPIC', "Searching" ) if( $__func eq "search" );
	Tokenize( 'HELP_SUB_TOPIC', ucfirst( $__family ) );
Tokenize( 'HELP_TOPIC', "Changelog" ) if( $__func eq "changelog" );
Tokenize( 'HELP_TOPIC', "Disclaimer" ) if( $__func eq "disclaimer" );


#
# 10/31/2000 - took out the "CATEGORIES" because it didn't fit with 
# our new web-site design
Parse( "HEADER", "SECTION_HEAD" );


#
# 11/1/2000 - originally there were some thoughts of using logins and variou
# other authentication type things in the PS, but those have since vanished,
# thus, I removed them from the main routines.
if( $__func eq "search" ){

	if( $__family ne "" ){
		#the user has submitted a query...
		Search();
	} else {
		#this is the front of the search (same as main.con for now)
		LoadTemplate( "content/search.con" );
		Sectionize( 'BODY', Parse( "SEARCH" ) );
	}

} elsif( $__func eq "changelog" ){

	ChangeLog();

} elsif( $__func eq "disclaimer" ){

	Disclaimer();

} else {

	#the user is at the front door...
	LoadTemplate( "content/main.con" );

}

$t1 = gettimeofday;
Tokenize( 'ELAPSED_TIME', $t1-$t0 );

Parse( "BODY", "SECTION_FOOT", "FOOTER" );

Output();


exit( 0 );



sub ChangeLog {
  LoadTemplate( "content/changelog.con" );
  Parse( "CHANGES" );
}


sub Disclaimer {
  LoadTemplate( "content/disclaimer.con" );
  Parse( "DISCLAIMER" );
}
