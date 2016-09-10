#!/usr/bin/perl
# nsleuth v.0.2.0
# (C)opyirght 2003, C.J. Steele <coreyjsteele@yahoo.com>, all rights reserved.
#
# convert netscape history files to current version of BerkeleyDB by using
# the following sequence of commands:
#   `db_dump185 history.dat > history2.db && db_load history3.dat < history2.db`
# The result will be a properly formatted database in history3.dat, that can be
# mangled with the following code.
#
# TODO:
#   - none
#
use strict ;
use BerkeleyDB ;
use POSIX qw( mktime strftime );
use vars qw( %h $k $v ) ;

my %sites; 
my $incr = 0; 

my $filename = $ARGV[0];
tie( %h, "BerkeleyDB::Hash", -Filename => "$filename", -Flags => "DB_CREATE" )
    or die "Cannot open file $filename: $! $BerkeleyDB::Error\n" ;

# print the contents of the file
while (($k, $v) = each %h){

    #sanitize the output (chop off dangling characters, null-termination, etc),
    # convert time values to necessary format(s)., etc.
    chomp( $k, $v );
    $k =~ s/\0//g;
    $v = scalar( localtime( unpack( "V", $v ) ) );

	addsite( $v, $k ); 

}
untie %h;


foreach ( sort( keys( %sites ) ) ) 
#this needs to be fixed for our $sites{} that are dups.
{
	my $stringtime = strftime( "%D %R", gmtime( $_ ) ); 
	print "$stringtime|$sites{$_}\n";
}


exit( 0 );


sub addsite
{
	my( $time, $site ) = @_; 
	my $ctime = convtime( $time );
	if( not exists $sites{$ctime} )
	{
		$sites{$ctime} = $site; 
	} else {

		while( exists $sites{ "$ctime.$incr" } )
		{
			$incr++; 
		}
		$sites{"$ctime.$incr"} = $site;
		$incr = 0;

	}
}


sub convtime 
{
	# formatted "Mon Jun 30 12:05:55 2003"
	my %mon = ( 'Jan' => 0, 'Feb' => 1, 'Mar' => 2, 'Apr' => 3, 'May' => 4, 'Jun' => 5, 'Jul' => 6, 'Aug' => 7, 'Sep' => 8, 'Oct' => 9, 'Nov' => 10, 'Dec' => 11 );
	my $strtime = shift; 
	my( $weekday, $month, $monthday, $time, $year ) = split( /\ {1,2}/, 
$strtime, 5 ); 
	my( $hr, $min, $sec ) = split( /:/, $time, 3 ); 
	$hr--; $min--; $sec--;
	$year-=1900;
	return mktime( $hr, $min, $sec, $mon{$month}, $monthday, $year );
}
