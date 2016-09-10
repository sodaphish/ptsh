#!/usr/bin/perl
use strict;
use POSIX qw( strftime );

my @unbanned;
my @tounban;

my $curtime = strftime( "%s", localtime( time() ) );

open( IN, "/home/hostedby/www/mine/wc/phpban.txt" ) or die "$!"; 
while( <IN> )
{
	chomp( $_ );
	my( $date, $session, $level, $message ) = split( /\ \-\ /, $_, 4 );
	if( $session eq "BANBT" )
	{
		# here we identify previously unbanned IPs so we don't unban them needlessly
		my @m = split( /\s/, $message );
		push( @unbanned, $m[1] );
	} else {
		# here we're finding IP's that have temporary bans
		if( $message =~ /TEMPBAN/ )
		{
			$message =~ s/^TEMPBAN\://;
			my( $ip, $banexp ) = split( /\//, $message, 2 );
			if( $banexp <= $curtime )
			{
				push( @tounban, "$ip" );
			} 
		} #end if
	} #endif
} #end while
close( IN );

foreach my $target ( @tounban )
{
	# here we're doing the work of unbanning all the IPs that havent' been unbanned that need to be.
	unban( $target ) if( ! isin( $target, @unbanned ) );
}

exit( 0 );




sub isin
{
	my( $t, @a ) = @_;
	foreach( @a )
	{
		return 1 if( $_ eq $t );
	}
	return 0;
} #end isin()




sub unban
{
	my $ip = shift;
	open( OUT, ">>/home/hostedby/www/mine/wc/phpban.txt" ) or die( "$!" );
	print  OUT strftime( "%G-%m-%d %H:%M:%S", localtime( time() ) ), " - BANBT - INF - UNBANNING $ip because: Ban expired\n";
	close( OUT );
	my $cmd = "./ban.py -u $ip"; 
	# do the actual unban.
	system( $cmd );
} #end unban()




#EOF
