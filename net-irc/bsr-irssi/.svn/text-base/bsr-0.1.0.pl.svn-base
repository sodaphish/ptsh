#
# BSRb0t v.0.1.0 
# (C)opyright 2003, Corey J. Steele, all rights reserved.
#
# TODO: 
#	- add a timer to prevent flood DoS attacks.
# 
use strict;
use vars qw( $VERSION %IRSSI );

use Irssi qw( signal_add_last settings_add_bool settings_add_str 
				settings_get_bool settings_get_str );

$VERSION = '0.1.0'; 
%IRSSI = ( 
	authors => 'SodaPhish',
	contact => 'coreyjsteele@yahoo.com',
	name => 'BSRb0t',
	description => 'provides up-to-date and automated butt status reports',
	license => 'BSD-style',
	url => 'http://sodaphish.com/bsr.pl.html',
	changed => 'Jun 18 2003 15:24Z-0600'
);


my $bsr = "(_._)";

sub bsr {
    my ($server, $data, $nick, $address, $target ) = @_;
	my $channel = Irssi::active_win()->get_active_name();
	if( $data =~ /^!bsr/i )
	{
		$server->command( "/msg $channel BSRb0t says, \"BSR: ". $bsr ."\"" );
	} else {
		return;
	}
}

sub setbsr 
{
	my( $data, $server, $channel ) = @_;
	if( $data =~ /^\(/ )
	{
		$channel->print( "BSR is now $data" );
		$bsr = $data; 
	}
}

sub getbsr
{
	my( $data, $server, $channel ) = @_;
	$channel->print( "BSR: $bsr" ); 
}

Irssi::signal_add_last( 'message public', 'bsr' );
Irssi::command_bind( 'setbsr', 'setbsr' );
Irssi::command_bind( 'getbsr', 'getbsr' );

print CRAP "%B>>%n ".$IRSSI{name}." v".$VERSION." loaded...";

