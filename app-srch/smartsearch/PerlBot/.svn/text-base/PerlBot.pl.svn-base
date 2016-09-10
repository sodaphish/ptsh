#!/usr/bin/perl
use strict;
use LWP::Simple;

my @relavent = ( "firewall", "antivirus", "vpn", "hacker", "hack", "crack", "encryption", 
		"virus", "worm", "authentication", "buffer", "buffer-overflow", "overflow", 
		"trojan", "password", "biometrics", "piracy", "lan", "checksum", 
		"access-control", "ACL", "sniffer", "cookie", "javascript", "bug", "security", "network" ); 
my @urls = getURLs(); 

foreach my $url ( @urls )
{
	chomp( $url );
	my $result = get( $url );
	if( defined( $result ) )
	{
		my @hit_words = (); 

		$result =~ s/<[^>]*>/\:\*\:/g;
		$result =~ s/\ /\:\*\:/g; 
		$result =~ s/\s//g; 
		$result =~ s/\:\*\:/ /g;
		foreach( split( /\s/, $result ) )
		{
			chomp( $_ );

			# look for keyword hits in @relavent
			if( isIn( $_, @relavent ) )
			{
				# this word is a match, insert it in the database
				if( ! isIn( $_, @hit_words ) )
				{
					push( @hit_words, $_ ); 
				} 
			} else {
				# this word is irrelevant
			}

			#look for URL's

		}
	
		# check page for other relavent URLs

		if( @hit_words ) 
		{
			recordHit( $url, @hit_words ); 
		} else {
			# google thinks this URL was worthwhile, why don't we?
			# TODO: demote this link
		}

	} else {
		# get failed
		print STDERR "Couldn't get $url\n";
		# TODO: remove $_ from database
	}
}

exit( 0 );


sub isIn
{
	my( $query, @array ) = @_;
	foreach( @array )
	{
		return 1 if( $query eq $_ );
	}
	return 0;
}


sub recordHit 
{
	my( $url, @hitWords ) = @_; 
	print "recording hits for $url: "; 
	print "$_, " foreach( @hitWords ); 
	print "\n"; 
	return;
}


sub getURLs 
{
	# TODO: query the database for the URLs gleaned from the GoogleQuery tool.
	return ( "http://sodaphish.com", "http://forwardsteptech.com" );
}
