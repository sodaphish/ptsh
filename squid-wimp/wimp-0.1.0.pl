#!/usr/bin/perl
#
# wimp.pl v.0.1.0
# (C)opyright 2003, C.J. Steele <coreyjsteele@yahoo.com>, all rights reserved.
#
# wimp can be used to convert squid proxy log files in to comma separated values
# files, that can be imported in to Excel and other data-munging software.
#
# TODO/ROADMAP:
#	- allow exceptions such that images, stylesheets, and java/javascript 
#		requests aren't displayed.(v.0.2.0)
#
use strict;

my $file = $ARGV[0];
if( $file and ( -e $file and -r $file ) )
{

	# proceed only if the file is there and we can read it.
	open( IN, $file ) or die_violently( "open failed!" );
	while( my $line = <IN> )
	{
	
		chomp( $line );
		# clean_parse() returns ( $time, $size, $client_ip, $hit_or_miss, $unknown, $method, $url, $garbage, $ipc, $type );
		my @log_entry = clean_parse( $line );
		my @time = parse_time( $log_entry[0] );
		print "$time[2]:$time[1]:$time[0],", $time[4] + 1, "/", $time[3] + 1, "/", $time[5] + 1900, ",$log_entry[2],$log_entry[6]\n";

	}
	close( IN );

} else {

	if( $file ne "" )
	{
		die_violently( "$file not found!" );
	} else {
		show_usage();
		exit( 1 );
	}

}

exit( 0 );


sub parse_time
{
	my( $in_time ) = @_;
	return gmtime( $in_time );
}


sub clean_parse
{

	my( $entry_line ) = @_;

	my $time = substr( $entry_line, 0, 14 ); 
	my $size = substr( $entry_line, 14, 8 ); $size =~ s/\s//g; 
	my $client_ip = substr( $entry_line, 22 ); my( $client_ip, $entry_line ) = split( /\s/, $client_ip, 2 ); 
	my ( $hit_or_miss, $unknown, $method, $url, $garbage, $ipc, $type ) = split( /\s/, $entry_line ); 

	return( $time, $size, $client_ip, $hit_or_miss, $unknown, $method, $url, $garbage, $ipc, $type );

	return;

}


sub die_violently 
{

	my( $msg ) = @_;
	print STDERR "$0 > $msg\n";

}


sub show_usage
{

	print "$0 - (C) 2002 by Corey J. Steele\n";
	print "$0 <squid_log>\n\n";

}
