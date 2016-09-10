# spot v.0.0.0 
# (C)opyright 2003, Corey J. Steele, all rights reserved.
#
# General-purpose irssi IRC bot that...
#	* auto join/part greets fairwells
#	* interesting topic logs
#	*
#
use strict;
use vars qw( $VERSION %IRSSI );
use Irssi qw( signal_add_last settings_add_bool settings_add_str 
				settings_get_bool settings_get_str );

$VERSION = '0.0.0'; 
%IRSSI = ( 
	authors => 'SodaPhish',
	contact => 'coreyjsteele@yahoo.com',
	name => 'spot',
	description => 'provides various customized irc functions',
	license => 'BSD-style',
	url => 'http://sodaphish.com/spot.html',
	changed => 'Jun 24 2003'
);


my $sp_mylastact = time();
my $sp_awaythresh = 300;
my $sp_awaystate = 0; 
my $sp_mynick = "sp"; 
my $sp_spotdir = "~csteele/.irssi/spot/"; 
my %sp_lastseen;
my @sp_friends = ( "Painless", "Guru", "bidders", "morner", "BalDown", "CharlieB", "rathgild" ); 
my @sp_topics = ( "firewall", "iptables" );
my %sp_topiclogstate;
my $sp_awaymsg = "Sorry, I'm away right now..."; 




#
#evt_ownpublicmsgs() - stuff I've said throws these signals...
sub evt_ownpublicmsgs {
	my( $server, $data, $target ) = @_; 
	$sp_mylastact = time();
	if( $sp_awaystate )
	{
		back();
	}
} #end evt_ownpublicmsgs()




#
#evt_ownprivatemsgs()
sub evt_ownprivatemsgs {
	my( $server, $data, $target, $origtarget ) = @_; 
	
	#don't do anything, yet.

} #end evt_ownprivatemsgs()




#
#evt_publicmsgs() - stuff other people say throws this signal...
sub evt_publicmsgs {
    my ($server, $data, $nick, $address, $target ) = @_;
	my $channel = Irssi::active_win()->get_active_name();

	# track interesting topics in public discussion...
	#foreach( @sp_topics )
	#{
	#}

	#handle tracking stuff while I'm 'away'.
	if( $sp_awaystate and $data =~ m/^$sp_mynick(\:|\>|\s+?)/g )
	{
		$server->command( "/msg $nick ..." ); 
	}

	#handle setting auto-away
	if( ( (time() - $sp_mylastact) > $sp_awaythresh ) and not $sp_awaystate )
	{
		#I've been idle longer than the permitted time...
		# call my auto-away routines!
		away( $server, $channel );
	}

} #end evt_publicmsgs()




#
#evt_privatemsgs() - when someone privmsgs me, it throws this sig.
sub evt_privatemsgs {
	my( $server, $data, $nick, $address, $target ) = @_;
	my $channel = Irssi::active_win()->get_active_name();

	#decide what you want to do with privmsgs

} #end evt_privatemsgs()




#
#evt_join() - when somone joins the channel, it throws this sig.
sub evt_join {
	my( $server, $data, $nick, $address, $target ) = @_;
	my $channel = Irssi::active_win()->get_active_name();

	if( not $sp_awaystate )
	{
		#if we're not away, greet friends
		foreach( @sp_friends )
		{
			if( $nick =~ m/^$_(\w*)\s/ )
			{
				#this person is our friend, greet them!
				$server->command( "/msg $channel 'lo $nick" ); 
			}
		}
	} #endif

} #end evt_join();




#
#evt_leave() - when somone leaves, it throws this sig.
sub evt_leave {
	my( $server, $data, $nick, $address, $target ) = @_;
	my $channel = Irssi::active_win()->get_active_name();

	foreach( @sp_friends )
	{
		if( $nick eq $_ )
		{
			$server->command( "/action $channel stands waving as $nick rides off in to the sunset..." );
		}
	}

	#update the lastseen record for the departing user.
	$sp_lastseen{$nick} = time();

} #end evt_leave()




#
#autoaway()
sub away {
	my( $server, $channel ) = @_;
	# set the away-bit
	$sp_awaystate = 1;
	print CRAP "%B>>%n ". $IRSSI{name} ." $sp_mynick is away."; 
} #end autoaway()




#
#back() - 
sub back {
	$sp_awaystate = 0;
	# add bits to show events that occurred while away.
	print CRAP "%B>>%n ". $IRSSI{name} ." $sp_mynick is back."; 
} #end back()



#
#cmd_away()
sub cmd_away {

} #end cmd_away()




#
#cmd_auto()
sub cmd_auto
{
	my( $data, $server, $channel ) = @_;
	# the auto command handles autojoins of channels
	$server->print( $server, "auto!" );
} #end cmd_auto()




#
#main()
print CRAP "%B>>%n ". $IRSSI{name} ." v". $VERSION ." loading..."; 
if( not ( -d $sp_spotdir and -W $sp_spotdir ) )
{
	#our directory structure isn't in place, try to create it.
	# this may be the first time we've been run, so... 
	eval {
		system( "mkdir $sp_spotdir 2&>/dev/null " ) or die( "$!" ); 
	}; if( $@ ) {
		print CRAP "%B>-%n ". $IRSSI{name} .": failed to load! ($@)"; 
		exit( 1 );
	} else {
		print CRAP "%B>-%n ". $IRSSI{name} ." initialization completed!"; 
		print CRAP "%B>-%n ". $IRSSI{name} ."-specific files are in $sp_spotdir";
		print CRAP "%B>-%n ".$IRSSI{name}." v".$VERSION." loaded...";
	}

} else {

	#the startup checks succeeded, DO IT!
	print CRAP "%B>-%n ". $IRSSI{name} ." startup checks completed!"; 
	print CRAP "%B>-%n ".$IRSSI{name}." v".$VERSION." loaded...";

}

Irssi::signal_add_last( 'message public', 'evt_publicmsgs' );
Irssi::signal_add_last( 'message own_public', 'evt_ownpublicmsgs' );
Irssi::signal_add_last( 'message private', 'evt_privatemsgs' );
Irssi::signal_add_last( 'message own_private', 'evt_ownprivatemsgs' );
Irssi::signal_add_last( 'message join', 'evt_join' );
Irssi::signal_add_last( 'message part', 'evt_part' );
Irssi::command_bind( 'auto', 'cmd_auto' );
