#!/usr/bin/perl -w
use URI::URL;
$| = 1;

while ( <> ){
    ($url, $addr, $fqdn, $ident, $method) = m:(\S*) (\S*)/(\S*) (\S*) (\S*):;

	$url = url $url;
	$host = lc($url->host);

	# do not process hosts in local domain or unqualified hostnames
	if ( $host !~ /\./ ) {
	next;
	}

	# do our thing to the url's that match
	# -- here is where we'd look to see if the domain is blacklisted...

} continue {
    print "$url $addr/$fqdn $ident $method\n"
}
#close( OUT );
