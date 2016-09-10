#!/usr/bin/perl
use strict;

my @results = ();

open( IN, $ARGV[0] );
while( my $line =  <IN> )
{
	chomp( $line );
	$line =~ s/^\ *// if( $line =~ /^\ / ); 
	my( $time, $command, $slot, $bits ) = split( /\ /, $line, 4 );

	if( $command =~ /ClientUserinfo\:/ )
	{

		my %ht = {}; 
		my $key = "";
		my $in = 1;
		foreach my $v ( split( /\\/, $bits ) )
		{
			if( $in )
			{
				$ht{$key} = $v;
				$in = 0;
			} else {
				$key = $v;
				$in = 1;
			} #end if
		} #end foreach
		my $res = $ht{name} . "\\" . $ht{ip} . "\\" . $ht{cl_guid} . "\n";
		push( @results, $res ) if( ! isin( $res, @results ) );
	} #end if
} #end while
close( IN ); 

foreach( @results )
{
	print "$_";
}


#
# this is an ugly linear search of the list for item
sub isin
{
	my( $item, @list ) = @_;
	foreach( @list )
	{
		return 1 if( $_ eq $item );	
	}
	return 0;
} #end isin()
