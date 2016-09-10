#!/usr/bin/perl
# produces a 32-character string of random characters
use strict;
my $key = "";
for( my $x = 0; $x < $ARGV[0]; $x++ )
{
	my $rndChar = chr( int( rand( 255 ) ) );
	while( $rndChar !~ /\w/ )
	{
		$rndChar = chr( int( rand( 255 ) ) ); 
	}
	$key .= $rndChar;
}
print $key;
