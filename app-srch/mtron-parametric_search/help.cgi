#!/usr/bin/perl
print "Content-type: text/html", "\n\n";

BEGIN {
	use CGI;
	use lib 'lib';
	use ParseLib;
	require "Config.pl";
}

$topic = lc( CGI::param( "topic" ) );
$page = lc( CGI::param( "p" ) );

use vars qw( $topic $page );

Tokenize( 'HELP_SUB_TOPIC', "" );

main {

	Tokenize( 'HELP_TOPIC', "Help" ); #this is default
	Tokenize( 'HELP_TOPIC', "Searching" ) if( $topic eq "searching" and $page ne "" );
        #Tokenize( 'HELP_TOPIC', "Changelog" ) if( $topic eq "changelog" );
	#Tokenize( 'HELP_TOPIC', "Disclaimer" ) if( $topic eq "disclaimer" );

 	LoadTemplate( "content/layout.tmpl" );

	Parse( "HEADER", "CATEGORIES", "SECTION_HEAD" );

	if( $topic eq "searching" ){

		LoadTemplate( "content/help-searching.con" );

		if( $page eq "crystals" ){

			Parse( "CRYSTAL_HELP" );

		} elsif( $page eq "oscillators" ){
	
			Parse( "OSCILLATOR_HELP" );	

		} else {

			Parse( "GENERAL_HELP" );

		}

 	} elsif( $topic eq "changelog" ){

		LoadTemplate( "content/help-changelog.con" );

		Parse( "GENERAL_HELP" );
	
	} elsif( $topic eq "disclaimer" ){

		LoadTemplate( "content/help-disclaimer.con" );

		Parse( "GENERAL_HELP" );

	} else {

		LoadTemplate( "content/help.con" );

		Parse( "GENERAL_HELP" );
	
	}

	Parse( "SECTION_FOOT", "FOOTER" );

	Output();

} #end main()

exit( 0 );
