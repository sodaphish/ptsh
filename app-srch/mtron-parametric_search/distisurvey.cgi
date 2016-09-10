#!/usr/bin/perl
# filename: distisurvey.cgi
# (C)opyright 2000, M-tron Industries, Inc., all rights reserved.
#	written by Corey J. Steele <csteele@mtron.com>
# last modified: 12/13/2000
#
# Description: this script handles the distributor survey.  It simply dumps
#	the contents of the survey form to a database.
print "Content-type: text/html", "\n\n";

use CGI::Carp qw( fatalsToBrowser );
use CGI param;
use lib qw( cfg );
require "DSN_readwrite.pl";

#
# initialize the SQL insert... (we do this here so we only have to loop once.
$sqlstmt = "INSERT INTO misc_distisurvey (date, choice";  

#
# setup the parameters sent by the HTML form...
@choices = (); 
	$choices[0] = param( "choice" );
	for( $x = 1; $x < 19; $x++ ){
		my $mod_choice = $x+1; 
		$choices[$x] = param( "choice$mod_choice" );
		$sqlstmt .= ", choice$mod_choice"; 
	}
$fcd_line = Clean( param( "fcd_line" ) ); #nuke the apostrophies!
$comments = Clean( param( "comments" ) ); #nuke the apostrophies!

#
# setup the other parameters we'll need
$date = time(); 

#
# finish off the SQL statement.
$sqlstmt .= ", fcd_line, comments) VALUES ( '$date'"; 
$count = 0; 
foreach( @choices ){
	$sqlstmt .= ", '$choices[$count]'"; 
	$count ++; 
}

#
# close SQL statement parenthesis.
$sqlstmt .= ", '$fcd_line', '$comments' )"; 


$stmt_h = $__dsn->prepare( $sqlstmt );
$stmt_h->execute;


open( IN, "distisurvey_thankyou.html" ) or die "$!";
print <IN>; 
close( IN );

exit( 0 );


sub Clean {

        my $return = "";
        foreach( @_ ){
                $_ =~ s/\'/\`/gi;
                $return .= "$_ ";
        }
	chop( $return );
        return $return;

}
