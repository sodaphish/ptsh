#
# BSRb0t v.0.2.0 
# (C)opyright 2003, Corey J. Steele, all rights reserved.
#
# TODO/ROADMAP: 
#       - add a timer to prevent flood DoS attacks. (v.0.2.0)
#       - add '!bsr help' (v.0.2.0)
# 		- allow change of bsr timeout via '/settot' command (v.0.2.0)
#       - track multiple people's BSR, accounting for nick changes. (v.0.3.0)
#       - support on-the-fly add/rmv/edt of BSR list (v.0.4.0)
# 

use strict;
use vars qw( $VERSION %IRSSI );

use Irssi qw( signal_add_last settings_add_bool settings_add_str 
				settings_get_bool settings_get_str );

$VERSION = '0.2.0'; 
%IRSSI = ( 
	authors => 'SodaPhish',
	contact => 'coreyjsteele@yahoo.com',
	name => 'BSRb0t',
	description => 'provides up-to-date and automated butt status reports',
	license => 'BSD-style',
	url => 'http://sodaphish.com/bsr.pl.html',
	changed => 'Jun 20 2003 09:24Z-0600'
);


my $bsr = "(_*_)";
my $tot = 300;
my $lastbsr = 0;

my @helptext = ( "BSRb0t v.$VERSION", "Its probably better if you not ask questions, but since you have...", "The Butt Status Report presently tracks the status of sp's anus.", "If you're smart, you'll leave it at that.", "If not, read on.", "The following butt statae are known/established:", "    (_*_)    normal", "    (_._)    constipated", "    (_S_)    stinky", "    (_X_)    painful", "    (_\&_)    buttplug in", "    (_db_)   gay butt-love", "    (_^_)    random insertion error", "    (_(  )_) bored out from too much (_db_)", "    (_\$_)    rich ass", "    (_oo)ooo butt beads", "    (_\@_)    goatse.cx", "PM sp with suggestions." );

sub bsr {
	my ($server, $data, $nick, $address, $target ) = @_;
	my $channel = Irssi::active_win()->get_active_name();
	if( $data =~ /^!bsr/i )
	{

		$data =~ s/^!bsr//i;
		chomp( $data ); 
		my @args = split( / /, $data ); 

		$server->command( "/msg sp $_" ) foreach( @args ); 

		#if( scalar( @args ) != 0 )
		if( scalar( @args ) > 0 )
		{

			#$args[0] = lc( $args[0] ); 
			my $cmd = pop( @args ); 
			if( $cmd eq "help" )
			{
				# show help screen
				$server->command( "/msg $nick $_" ) foreach( @helptext );
			} else {
				# unknown command.
				$server->command( "/msg $nick BSRb0t: unknown command $args[0]." ); 
			}

		} else {
			if( $lastbsr < (time() - $tot) )
			{
				$server->command( "/msg $channel BSRb0t says, \"BSR: ". $bsr ."\"" );
				$lastbsr = time();
			} else {
				$server->command( "/msg $nick BSRb0t says, \"BSR: ". $bsr ."\"" );
				$server->command( "/msg $nick You got a pm 'cause the last BSR was requested less than $tot seconds ago." );
			}
		}
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

sub settot
{
	my( $data, $server, $channel ) = @_;
	$tot = $data; 
	$channel->print( "BSR timeout is now $data" );
}

Irssi::signal_add_last( 'message public', 'bsr' );
Irssi::command_bind( 'setbsr', 'setbsr' );
Irssi::command_bind( 'getbsr', 'getbsr' );
Irssi::command_bind( 'settot', 'settot' );

print CRAP "%B>>%n ".$IRSSI{name}." v".$VERSION." loaded...";

