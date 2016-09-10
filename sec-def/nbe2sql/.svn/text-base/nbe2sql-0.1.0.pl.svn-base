#!/usr/bin/perl
# nbe2sql v.0.1.0 
# (C)opyright 2003, C.J. Steele <coreyjsteele@yahoo.com>, all rights reserved.
# 
# This script converts Nessus (2.0) NBE reports to various output formats
# check the TODO/ROADMAP section for details on what is currently supported.
#
# TODO/ROADMAP:
#	- write basic README on how to use this tool and how to generate 
#		.nbe files from the CLI w/ Nessus. (v.0.1.0)
#	- expand cmd-line options to support (v.0.2.0):
#		-f	source NBE file
#		-o 	output type {csv,sql}
#		-h	database host
#		-t	type of database {mysql}
#		-u	user for db connect
#		-p	password for db connect
#		-v	verbose output/debugging
#		-h	help
#	- abstract SQL commands to multiple DB types; adjust -t options (v.0.3.0)
#
use strict;
use DBI::mysql;

my $scanstart = "";
my $scanstop = ""; 
my %hostscans = {};
my $db_user = "root";
my $db_passwd = "";
my $db_host = "localhost";
my $db_dbname = "nessus"; 

if( -f $ARGV[0] ){
	open( IN, $ARGV[0] ) or die "$!"; 
	#connect to the desired database
	my $dbh = DBI->connect( "dbi:mysql:$db_dbname;host=$db_host", "$db_user", "$db_passwd" ) or die "$!"; 
	while( <IN> )
	{
		chomp( $_ );
		my @e = split( /\|/, $_ ); 
		if( scalar( @e ) == 7 ){

			$dbh->do( "insert into nessus_alert (date,host,type,srvc,msg) VALUES ( '$hostscans{$e[2]}', '$e[2]', '$e[3]', '$e[5]', '$e[6]' )" ) 
				or die "Couldn't insert into the database.\n"; 

		} else {

			if( $e[0] eq "timestamps" ){
				#these are the lines we're actually looking at in the NBE
				# timestamps||172.16.104.151|host_end|Mon Jun  2 15:34:12 2003|
				# timestamps|||scan_end|Mon Jun  2 15:34:12 2003|
				if( $e[3] eq "scan_start" ){
					#beginning of a specific scan
					# not even sure why we're tracking this
					$scanstart = $e[4]; 
				} elsif( $e[3] eq "scan_stop" ){
					#end of a general scan
					# not even sure why we're tracking this
					$scanstop = $e[4]; 
				} elsif( $e[2] ne "" ){
					#message regarding a specific host's scan; 
					# we're really only worried about the start time for the
					# purpose of logging. 
					$hostscans{$e[2]}="$e[4]" if( $e[3] eq "host_start" );
				}
			}

		}
	} #end while
	close( IN ); 
} else {
	print "usage: nbe2sql <file.nbe>\n\n";
}

exit( 0 );
