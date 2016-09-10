#!/usr/bin/perl
#
# bkmrk_sleuth.pl v.0.1.0
# (C)opyright 2003, C.J. Steele <coreyjsteele@yahoo.com>, all rights reserved.
#
# This script disects a netscape/mozilla bookmarks file and tells us useful information about 
# the user's browsing history.
use strict;

open( IN, "bookmarks.html" ) or die "$!";
while( <IN> )
{
	chomp( $_ );
	if( $_ =~ m/href/i ) # the line contained a hyper-reference
	{
		# chop out the preceeding crap
		$_ =~ s/\s*\<\/dd\>\<dt\>\<*a\s//i;
		# split the remainder in to bits...
		my @comp = split( /\s/, $_, 4 );
		$comp[0] =~ s/href\=\"//; $comp[0] =~ s/\"//; 
		$comp[1] =~ s/add_date\=\"//; $comp[1] =~ s/\"//;
		$comp[2] =~ s/last_visit\=\"//; $comp[2] =~ s/\"//;
		( $comp[3], $comp[4] ) = split( /\>/, $comp[3], 2 );
		$comp[3] =~ s/last_modified\=\"//; $comp[3] =~ s/\"//;
		$comp[4] =~ s/\<\/a\>//; 
		# @comp
		# 0 - url
		# 1 - add_date
		# 2 - last_visit
		# 3 - last_modified
		# 4 - title
		my $lvv = time() - $comp[2]; 
		if( $lvv > 604800 )
		{
			my @tc = gmtime( $lvv );
			$tc[4]++;
			$lvv = "$tc[4]\/$tc[3]";
		} else {
			if( $lvv >= 518400 ){ $lvv = "7 days ago"; }
			elsif( $lvv >= 432000 ){ $lvv = "6 days ago"; }
			elsif( $lvv >= 345600 ){ $lvv = "5 days ago"; }
			elsif( $lvv >= 259200 ){ $lvv = "4 days ago"; }
			elsif( $lvv >= 172800 ){ $lvv = "3 days ago"; }
			elsif( $lvv >= 86400 ){ $lvv = "2 days ago"; }
			else { $lvv = "Today"; }
		}

		my @ftc = gmtime( $comp[1] );
		my $fcc = "$ftc[4]\/$ftc[3]"; 

		if( $comp[4] eq "" ){ $comp[4] = "Untitled"; }

		print "\n==============================\n$comp[4] - $comp[0]\n";
		print "\tfirst visit: $fcc\n\tlast visit: $lvv\n";
	}
}
close( IN );
