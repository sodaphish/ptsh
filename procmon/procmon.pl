#!/usr/bin/perl
use strict;

my @pids = ( "1", "2265", "1099" );

foreach( @pids )
{
	if( isPID( $_ ) )
	{
		print "ok\n";
	} else {
		print "oops!\n";
	}
}


exit( 0 );


sub getPIDS
{
}


sub isPID
{
	my $pid_needed = shift;
	if( -e "/proc/$pid_needed" )
	{
		return 1; 
	} else {
		return 0;
	}
}
