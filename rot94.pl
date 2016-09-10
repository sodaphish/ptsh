#!/usr/bin/perl
use strict;

my $input = $ARGV[0];
#my $input = "ing!\@test~";
my @original = split( //, $input );
my $output = ""; 
my $output2 = ""; 

# 'encrypt' bits...
foreach( @original )
{
	my $ordv1 = ord( $_ );
	my $ordv2 = $ordv1 - 46; 
	if( $ordv2 < 33 )
	{
		$ordv2 += 94;
	}
	print chr( $ordv1 ), " -> ", chr( $ordv2 ), " ($ordv1 -> $ordv2)\n";
	$output .= chr( $ordv2 );
}

print "$output\n";
my @encrypted = split( //, $output );
foreach( @encrypted )
{
	my $ordv1 = ord( $_ );
	my $ordv2 = $ordv1 + 46;
	if( $ordv2 > 126 )
	{
		$ordv2 -= 94;
	}
	print chr( $ordv1 ), " -> ", chr( $ordv2 ), " ($ordv1 -> $ordv2)\n";
	$output2 .= chr( $ordv2 );
}
print "$output2\n";
