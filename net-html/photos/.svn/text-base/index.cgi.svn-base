#!/usr/bin/perl
#
# index.cgi - this is a re-write of scripts leeched from Doug Jennewein (http://www.usd.edu/~djennewe)
# 
print "Content-type: text/html", "\n\n";
use strict;

my $page_title = "Photos"; 
my $page_headline = "My Photographs"; 
my $thumb_dir = "/shared/www/photos/thumbs"; 
my $jpeg_dir = "jpgs"; 
my $count = -1;
my $image_count = 0;

print "<html><head><title>$page_title</title></head><body><div align=center><h1>$page_headline</h1><table><tr>\n";
foreach my $image ( `ls -1 $thumb_dir/*.JPG` )
{
	chomp( $image );
	my $image_basename = `basename $image`; chomp( $image_basename );
	if( int( $count / 3 ) == 0 )
	{
		print "<td><a href=\"$jpeg_dir/$image_basename\"><img width=100 height=80 src=\"$jpeg_dir/$image_basename\" alt=\"$image\"></a><br><!--$image_basename--></td>\n";
		$count++;
	} else {
		print "</tr><tr><td><a href=\"$jpeg_dir/$image_basename\"><img width=100 height=80 src=\"$jpeg_dir/$image_basename\" alt=\"$image\"></a><!--<br>$image_basename--></td>\n";
		$count=0;
	}
	$image_count++;
}
print "</tr></table></div>"; 
print "<br><div align=right><i>$image_count images found</i></div><br>\n";
print "</body></html>\n";

exit( 0 );
