#!/usr/bin/perl
print "Content-type: text/html", "\n\n";

use ParseLib;
use CGI param;
use CGI::Carp qw(fatalsToBrowser);

Tokenize( 'FILE', DetermineFileName() ); 

$version = "5.0.0"; 
	Tokenize( 'VERSION', $version ); 
$login = param( "login" );
	Tokenize( 'LOGIN', $login ); 
$password = param( "passwd" );
	Tokenize( 'PASSWD', $password );
$function = param( "func" );
	Tokenize( 'FUNCTION', $function ); 
$entry = param( "entry" ); 
	Tokenize( 'ENTRY', $entry ); 
$query = param( "query" );
	Tokenize( 'QUERY', $query );
$file = param( "file" );
$date = `date`; chomp( $date );
	Tokenize( 'DATE', $date );


LoadTemplate( "portal.tmpl" );
Tokenize( 'TITLE', "pPortal $version - $function" ); 
Parse( "HEADER", "MASTHEAD" );

if( Login() ){
	# 
	# user logged in
	if( $function eq "list" ){
		#
		# we want to see what we can look at.

	} elsif( $function eq "view" ){
		#
		# we want to look at an entry

	} elsif( $function eq "search" ){
		#
		# we want to search for something

	} elsif( $function eq "add" ){
		#
		# we're to add an entry that has been specified
		if( $file ne "" and $entry ne "" ){
			MakeEntry( $file, $entry ); 
		} else {
			Tokenize( 'ERROR', "ERROR - not enough data provided." );
		}

	} else {
		#
		# display the add entry dialog
		Parse( "ADD_DIALOG", "WEATHER" );

	}

} else {
	#
	# user NOT logged in

} 

Parse( "FOOTER" );
Output(); 

exit( 0 );



sub DetermineFileName {
	my $month = `date +%B`; chomp( $month ); 
	$month = lc( $month );
	my $year = `date +%Y`; chomp( $year );
	return "$month-$year.jrnl"; 
}



sub Login {
	return 1;
}
