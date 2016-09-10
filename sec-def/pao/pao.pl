#!/usr/bin/perl
# pao.pl by C.J. Steele <coreyjsteele@yahoo.com>
#   (C)opyright 2005, C.J. Steele, all rights reserved.
#
# PIX Access-list Orderer - a script to help tune the order in which acl's on a
# PIX should be listed in the config so they are listed most efficiently (i.e.
# most frequently used rules come first.)
#
# use this from the CLI as follows...
#
# 	$ dpixsh sh access-list <access-list> > pixacls.txt
# 	$ ./pao.pl pixacls.txt | sort -nr | grep <access-list> | cut -f2- \
#		-d\ > <access-list>_ordered.txt
#
# the list will need to be hand-sorted to verify that the 'deny any' and 
# similar ACL's are listed last, or in whatever order most desired.
# 
use strict;

open( IN, "$ARGV[0]" ) or die( "$!" );
while( <IN> )
{
	chomp();
	if( $_ =~ /permit|deny\ / )
	{
		my @e = split();
		my $aclName = $e[1];
		my $aclLine = $e[3];
		my $aclHitCount = $e[scalar(@e)-1];
			$aclHitCount =~ s/\(hitcnt\=//; 
			$aclHitCount =~ s/\)//;
		my $aclThingy = ""; 
		for( my $x = 4; $x < scalar( @e ) - 1;  $x++ )
		{
			$aclThingy .= " $e[$x]";
		}

		print "$aclHitCount access-list $aclName $aclThingy\n";
	} 
}
close( IN );
