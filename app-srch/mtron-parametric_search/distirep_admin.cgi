#!/usr/bin/perl
# filename: distirep_admin.cgi
# (C)opyright 2001, M-tron Industries, Inc., all rights reserved.
#	written by Corey J. Steele <csteele@mtron.com>
# last modified: 1/25/2001
#
# Description: This program handles modifying the dr_show_locations table in the
# 	web database... that table is what populates the drop-box of the 
#	distirep.cgi program.
print "Content-type: text/html", "\n\n";

use CGI::Carp qw( fatalsToBrowser );
use CGI param;
use lib qw( lib cfg );
use ParseLib;
require "DSN_readwrite.pl";

$date = `date`; chop( $date );


#
# variables we'll use for security purposes
$host = $ENV{'REMOTE_ADDR'};
	$host = $ENV{'REMOTE_HOST'} if( $host eq "" ); 
$this_referer = $ENV{'HTTP_REFERER'}; 


# 
# HTTP header parameters...
$filled = param( "filled" );
$function = param( "function" );


if( $host ne "12.43.85.34" ){

	print "<HTML><HEAD><TITLE>404 Not Found</TITLE></HEAD><BODY><H1>Not Found</H1>The requested URL /~csteele/distirep_admin.cgi was not found on this server.<P></BODY></HTML>\n"; 
	exit();

}



LoadTemplate( "content/distirep_admin.tmpl" );
Parse( "HEADER" );


if( $filled ){

	if( uc( $function ) eq "DELETE" ){

		foreach( param( "selection" ) ){
			my $stmt_h = $__dsn->prepare( "delete from dr_show_locations where location=\"$_\"" )
				or die "Couldn't prepare database statement.";
			$stmt_h->execute()
				or die "Couldn't execute database statement."; 
			AppendOut( "deleting $_<br>\n" );
		}

		AppendOut( "Click <a href=distirep_admin.cgi>here</a> to do more administration." );

	} elsif( uc( $function ) eq "ADD" ){ 
	
		my $loc = param( "location" );

		my $stmt_h = $__dsn->prepare( "insert into dr_show_locations( location ) values( '$loc')" )
			or die "Couldn't prepare database statement.";
		$stmt_h->execute()
			or die "Couldn't execute database statement."; 
		AppendOut( "adding $loc<br>\n" ); 

		AppendOut( "Click <a href=distirep_admin.cgi>here</a> to do more administration." );

	} else {

		AppendOut( "NO, I WILL <b>NOT</b>!!!<br>" ); 

	}

} else {

	my $stmt_h = $__dsn->prepare( "select distinct location from dr_show_locations order by location" ) 
		or die "Couldn't prepare the database statement!"; 
	$stmt_h->execute()
		or die "Couldn't execute the database statement!";

	Parse( "LOCATION_SELECT_HEAD" ); 
	while( my( $loc ) = $stmt_h->fetchrow() ){
		Tokenize( 'LOC', $loc );
		Parse( "LOCATION_SELECT_ELEMENT" ); 
	}
	Parse( "LOCATION_SELECT_FOOT" );


	AppendOut( "<br><hr><br>" );


	Parse( "LOCATION_ADD" );

}


Parse( "FOOTER" ); 
Output(); 
$__dsn->disconnect();




#
# leave cleanly
exit( 0 );
