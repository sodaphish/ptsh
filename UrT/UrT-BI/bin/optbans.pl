#!/usr/bin/perl
# prepare the banlist by first eliminating duplicate records.  This can 
# be done on a *nix box by doing something like this... 
# 	cat banlist.txt | sort -n | uniq > banlist2.txt
# and then pass the banlist2.txt to this file via...
#		perl optbans.pl banlist2.txt > banlist3.txt
# once the script has optimized your list(s), rename banlist3.txt to 
# banlist.txt and upload it to your server.
#
use strict;

my %subnets;
my @hosts; 

open( IN, $ARGV[0] ) or die( "$!" );
while( <IN> )
{
	chomp( $_ );
	my( $ip, $sumpin ) = split( /\:/, $_, 2 );
	my( $a, $b, $c, $d ) = split( /\./, $ip, 4 );
	$subnets{"$a.$b.$c"} += 1;
	push( @hosts, $ip );
}
close( IN );

foreach my $key ( keys %subnets )
{
	if( $subnets{$key} > 1 )
	{
		# this bans any class C with more than one banned IP
		print "$key.0:-1\n";
	} else {
		#yes, this is grossly inefficient, but I'm lazy, so sod off.
		foreach my $host ( @hosts )
		{
			if( $host =~ /^$key/ )
			{
				print "$host:-1\n";
			}
		} #end foreach
	} #end if
} #end foreach

exit( 0 );




sub isin
{
	my( $target, @list ) = @_;
	foreach( @list )
	{
		return 1 if( $target eq $_ );
	}
	return 0;
} 

