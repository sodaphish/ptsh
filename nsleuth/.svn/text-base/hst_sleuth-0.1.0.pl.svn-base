#!/usr/bin/perl
# hst_sleuth v.0.1.0
# (C)opyirght 2003, C.J. Steele <coreyjsteele@yahoo.com>, all rights reserved.
#
# This script can be used on converted dbv1.85 history files to view results
# about the user's browsing history.
#
# convert netscape history files to current version of BerkeleyDB by using 
# the following sequence of commands:
# 	`db_dump185 history.dat > history2.db && db_load history3.dat < history2.db`
# The result will be a properly formatted database in history3.dat, that can be
# mangled with the following code.
#
# TODO: 
#	- none
#
use strict ;
use BerkeleyDB ;
use vars qw( %h $k $v ) ;

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

	#print output
	print "$v: $k\n"; 

}
untie %h;

exit( 0 );
