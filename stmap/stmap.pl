#!/usr/bin/perl
use strict;

my @specFields = ( "status", "name", "version", "author", "summary", "url", "description" );

if( scalar( @ARGV ) > 0 )
{
	my %tokens = readFile( $ARGV[0] ); 
	foreach( keys %tokens )
	{
		print "$_ : $tokens{$_}\n"; 
	}
} else {
	# print the specfile template
	foreach( @specFields )
	{
		print "$_:\n";
	}
}

exit( 0 );




sub readFile
{
	my $specFile = shift();
	my %tokens;
	open( IN, $specFile ) or die( "$!" );
	while( <IN> )
	{
		chomp( $_ );
		if( $_ !~ /^\#/ )
		{
			# this line isn't a comment...
			my( $token, $value ) = split( /\:/, $_, 2 );
			$tokens{$token} = $value;
		}
	}
	close( IN );
	return %tokens;
} #end readFile()
