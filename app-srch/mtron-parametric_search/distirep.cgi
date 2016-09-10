#!/usr/bin/perl
# filename: distirep.cgi
# (C)opyright 1999-2001, M-tron Industries, Inc., all rights reserved.
#	written by Corey J. Steele <csteele@mtron.com>
# last modified: 1/25/2001
#
# Description: This file handles doing lookups against the web.dr_* tables to
#	output them to a web-site for our website.  If no location is specified
#	the script drops a form with a drop-box to the client browser, else it
#	attempts to do the lookup.
print "Content-type: text/html", "\n\n";

use CGI param;
use lib qw( lib cfg );
use ParseLib;
use SearchLib;
require "DSN_readonly.pl";

$location = param( "location" );
@locations = ();

LoadTemplate( "content/distirep.tmpl" );
Parse( "HEADER" );

if( $location eq "" ){

	#
	# until we can alphabetize this shit, we can't use it.
	Parse( "LIST_HEAD" );

	#
	# get the list of locations for the distributors
	$sql_h = $__dsn->prepare( "select location from dr_show_locations order by location" );
	$sql_h->execute();
	while( my( $loc ) = $sql_h->fetchrow() ){
		push( @locations, $loc ); 
	}
	$sql_h->finish();

	foreach my $tmp ( @locations ){
		Tokenize( 'LOCATION_EL', $tmp );
		Parse( "LOCATION" );
	}

	#
	# need to post the end of the list.
	Parse( "LIST_FOOT" );

} else {

	#
	# the user specified a location, let's get the reps for that location
	@reps_to_display = ();
	@disti_to_display = ();

	$sql_h = $__dsn->prepare( "select id from dr_representatives_coverage where location = '$location'" );
	$sql_h->execute();
	while( my( $id ) = $sql_h->fetchrow() ){
		push( @reps_to_display, $id ) if( IsIn( $id, @reps_to_display ) != 1 );
	}
	$sql_h->finish();

	$stmt_h = $__dsn->prepare( "select id from dr_distributors_coverage where location = '$location'" );
	$stmt_h->execute();
	while( my( $id ) = $stmt_h->fetchrow() ){
		push( @disti_to_display, $id ) if( IsIn( $id, @disti_to_display ) != 1 );
	}
	$stmt_h->finish();

	$count = scalar( @reps_to_display ) + scalar( @disti_to_display ); 

	if( $count > 0 ){

		# 
		# there were matches to their search...
		AppendOut( "<b><font size=+2>Listings for $location</font></b><br><hr>\n" );

		if( scalar( @reps_to_display ) > 0 ){
			Parse( "REPS_HEAD" );
			foreach( @reps_to_display ){
				$stmt_h = $__dsn->prepare( "select name, add1, add2, city, state, zip, country, phone, fax from dr_representatives where id = '$_'" );
				$stmt_h->execute();
				my( $name, $add1, $add2, $city, $state, $zip, $country, $phone, $fax ) = $stmt_h->fetchrow(); 
				$stmt_h->finish();
				Tokenize( 'NAME', $name );
				Tokenize( 'ADD1', $add1 );
				$add2 = "" if( $add2 eq "" );
				Tokenize( 'ADD2', $add2 );
				Tokenize( 'CITY', $city );
				Tokenize( 'STATE', $state );
				Tokenize( 'ZIP', $zip );
				$country = "USA" if( $country eq "" );
				Tokenize( 'COUNTRY', $country );
				Tokenize( 'PHONE', $phone );
				Tokenize( 'FAX', $fax );
				Parse( "REPS" ); 
			}
			Parse( "REPS_FOOT" );
		}

		if( scalar( @disti_to_display ) > 0 ){
			Parse( "DISTI_HEAD" ); 
			foreach( @disti_to_display ){
				$sql_h = $__dsn->prepare( "select st, name, add1, city, zip, phone, fax, add2 from dr_distributors where id='$_'" );
				  $stmt_h = $__dsn->prepare( "select name, add1, add2, city, state, zip, country, phone, fax from dr_representatives where id = '$_'" );
				$sql_h->execute();
				my( $st, $name, $address, $city, $zip, $phone, $fax, $address2 ) = $sql_h->fetchrow();
				$sql_h->finish();
				Tokenize( 'ST', $st );
				Tokenize( 'NAME', $name );
				Tokenize( 'ADDRESS', $address );
				Tokenize( 'ADDRESS2', $address2 );
				Tokenize( 'CITY', $city );
				Tokenize( 'ZIP', $zip );
				Tokenize( 'PHONE', $phone );
				Tokenize( 'FAX', $fax );
				Parse( "DISTI" );
			}
			Parse( "DISTI_FOOT" ); 
		}

	} else {

		#
		# there were no matches to their search!
		AppendOut( "<font size=+2><b>Sorry, there were no reps matching that location.</b></font><br><br>\n" );

	}

}

Parse( "FOOTER" );
Output();

$__dsn->disconnect();


#
# leave cleanly
exit( 0 );
exit( 0 );
