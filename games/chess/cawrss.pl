#!/usr/bin/perl
use strict;
use LWP::Simple;
use XML::Atom::SimpleFeed;

my $username = "SodaPhish";
my $url = "http://www.chessatwork.com/core/viewpublicgames.php?p1name=$username&p2name=&showgamescode=I&Search=Search";

my $content = get( $url );
die "Couldn't get HTML." unless defined $content;

my $updated = scalar( gmtime( time() ) );


print "content-type: text/xml; charset=us-ascii\n\n";

my $feed = XML::Atom::SimpleFeed->new(
	title    => "Chess\@Work Game Feed",
	subtitle => "$username\'s games in progress",
	logo     => "http://www.chessatwork.com/favicon.ico",
	link     => "http://www.chessatwork.com/core/viewpublicgames.php?p1name=$username&p2name=&showgamescode=I&Search=Search",
	link     => {
		rel  => 'self',
		href => "http://intertrusion.com/chessatwork.php?$username",
		},
	id       => "http://intertrusion.com/chessatwork.php?$username",
	author   => "Corey J. Steele",
	updated  => $updated,
);


my( @elements ) = split( /\</, $content );

my $loopctr = 0;
my $player1 = "";
my $player1id = "";
my $player2 = "";
my $player2id = "";

foreach( @elements )
{
	if( $_ =~ /viewhistory/ or $_ =~ /playerprofile/ ){
		#a  href="/profile/playerprofile.php?uid=98906">sodaphish
		#a  href="/profile/playerprofile.php?uid=292384">polymorph
		#a href="/core/viewhistory.php?gameid=4457002">In progress

		$_ =~ s/a\s*href\=\"//gi;
		my ( $link, $target ) = split( /\"\>/, $_, 2 );

		#print "D($loopctr):   $link\t$target\n";

		if( $loopctr == 0 )
		{
			( $link, $player1id ) = split( /uid\=/, $link, 2 );
			$player1 = $target;			
			$loopctr += 1;
		} elsif( $loopctr == 1 ){
			( $link, $player2id ) = split( /uid\=/, $link, 2 );
			$player2 = $target;
			$loopctr += 1;
		} elsif( $loopctr == 2 ){
			my( $junk, $gameid ) = split( /gameid\=/, $link, 2 );
			$feed->add_entry( 
				title	=> "<a href=\"http://www.chessatwork.com/profile/playerprofile.php?uid=$player1id\">$player1</a> v. <a href=\"http://www.chessatwork.com/profile/playerprofile.php?uid=$player2id\">$player2</a> <a href=\"http://www.chessatwork.com/core/viewhistory.php?gameid=$gameid\">$gameid</a>",
				link	=> "http://www.chessatwork.com/core/viewhistory.php?gameid=$gameid",
				id		=> "http://www.chessatwork.com/core/viewhistory.php?gameid=$gameid",
				summary => "coming soon... the PGN of this game.",
				updated => "$updated"
			);
			#print "$player1 ($player1id) vs. $player2 ($player2id) $gameid ($target)\n";
			$loopctr = 0;
		} #end if
	} #end if
} #end foreach

$feed->print;


exit( 0 );
