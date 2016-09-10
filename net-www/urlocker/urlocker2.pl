#!/usr/bin/perl -w
use URI::URL;
$| = 1;

while ( <> ) {
	$in = $_;
    ($url, $addr, $fqdn, $ident, $method) = m:(\S*) (\S*)/(\S*) (\S*) (\S*):;

    $url = url $url;
    $host = lc($url->host);

    # do not process unqualified hostnames
    if( $host !~ /\./ )
	{
		next;
    }

} continue {
    #print "$url $addr/$fqdn $ident $method\n"
    print "$in\n";
}
