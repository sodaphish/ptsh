#!/usr/bin/perl
use strict;
use IO::Socket;
use Net::hostent;

# goal: this script acts as a mini HTTP proxy to block/log URL's visited by URL 
# and/or page content. This will be accomplished by acting as a proxy server 
# through which all HTTP requests must be made at which time the URL and its
# content will be examined for violations of policy and either permitted or 
# denied.
#
# should handle multiple clients, be database driven, have an easy interface 
# through which new sites can be added to be blocked, and should make it 
# impossible for connections to be made outside of this proxy.  Also need to
# support various levels of protection/filtering so an adult can surf to
# bad sites but so that kids can't.

# stage 1: bind to a local port to accept connections on
# stage 2: listen for connections from localhost (or, LAN connections)
# stage 3: handle connections

my $port = 8080;
my $server = IO::Socket::INET->new(	Proto 		=> 'tcp', 
									LocalPort 	=> $port, 
									Listen 		=> SOMAXCONN, 
									Reuse => 1 );

die "Can't bind to $port!" unless $server;

print "\n\n --- urlocker running on $port --- \n\n"; 

while( my $client = $server->accept() )
{

	my $pid = fork(); 
	die "Couldn't fork process!" unless defined $pid;
	if( $pid )
	{
		# parent
		close $client; 
		next;
	} else {
		# child
		my $url = ""; 
		my $header_string = ""; 
		my $method;
		my $junk;

		$client->autoflush( 1 );

		while( <$client> )
		{
			$header_string .= "$_";
			if( $_ =~ /^GET / or $_ =~ /^POST / )
			{
				$url = get_url( $_ ); 
				( $method, $junk ) = split( /\s/, $_, 2 ); 
			}
		}

		my $hostname = get_hostname( $url );
		print "remote host: $hostname...\n";

		my $dst = sockaddr_in( 80, inet_aton( "$hostname" ) );
		connect( SH, $dst ) or die $!;
			print SH $header_string;
			my $results; 
		while( <SH> )
		{
			# read results of inquery
			$results .= $_;
		}
		close( SH );

		print $client $results;

	} # if-else

}

print "\n\n --- exiting urlocker --- \n\n"; 
exit( 0 );


sub get_hostname
{
	my $url = shift;
	$url =~ s/http:\/\///i; 
	my( @bits ) = split( /\//, $url, 2 ); 
	return $bits[0];
}

sub get_url
{
	my( $request ) = shift;
	my( @parts ) = split( /\s/, $request );
	foreach( @parts )
	{
		if( $_ =~ /^http:\/\//i )
		{
			return $_; 
		}
	}

	return ""; 
}

sub is_safe
{
	return 1;
}
