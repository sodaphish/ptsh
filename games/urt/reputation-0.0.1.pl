#!/usr/bin/perl
# 
# reputation.pl v0.0.1 
#		by C.J. "SodaPhish" Steele <coreyjsteele@gmail.com>
#
# this script processes a ioURT server log file and calculates 
# reputations for each player based off of their relative performance 
# (i.e. if you've played a little, that's accounted for, if you've 
# played a lot, that is too.)
# 
# reputations are calculated based off of a number of variables, such 
# as how many kills you have and with which weapons (kicking someone 
# to death is higher valued than shooting someone with an LR300, which 
# is less difficult than a pistol, and so on) and performance in bomb-
# mode, performance in CTF, etc.  These values are then logarithmically 
# normalized to produce a value between 0 and 100, which is 
# representative of the player's reputation.
# 
# a plausible scale based off of my statistical analysis might be:
#   85 or higher:	god-like
#   75-84			really good
#		60-74			good
#		30-59			average
#		10-30			bad
#		0-10			down-right awful
#
# the idea behind this script is to produce an objective means by which 
# a player's skill and/or contribution to the clan can be measured on 
# an on-going basis.  using this script, in conjunction with other 
# components, it should be possible to produce information on the 
# statistical trend of a given player (i.e. improving, maintaining, 
# worsening, etc.) and could or should be wrapped into a web-based gui 
# for easy viewing
#
use strict;
use Switch;

my %rep;
my %slots;

my $DBG = 0;

open( IN, $ARGV[0] ) or die( $! );
while( my $line = <IN> )
{
	chomp( $line );
	$line =~ s/^\ *// if( $line =~ /^\ / ); #get rid of leading spaces
	my( $time, $command, $slot, $bits ) = split( /\ /, $line, 4 );

	print "D: LINE_TIME: $time\n" if( $DBG );
	print "D: LINE_COMMAND: $command\n" if( $DBG );
	print "D: LINE_SLOT: $slot\n" if( $DBG );
	print "D: LINE_BITS: $bits\n" if( $DBG );

	switch( $command )
	{

		case /ClientUserinfo\:/
		{
			my %ht = {};
			my $in = 1;
			my $key = ""; 

			foreach my $v ( split( /\\/, $bits ) )
			{
				if( $in )
				{
					$ht{$key} = $v;
					$in = 0;
					print "D: set key: $key = $v\n" if( $DBG );
				} else {
					$key = $v; 
					$in = 1;
				}
			} #end foreach
			${$slots{$ht{name}}}{'slot'} = $slot;

			print "D: ClientUserinfo() name = ", $ht{name}, "\n" if( $DBG );
			print "D: ClientUserinfo() slot = ", ${$slots{$ht{name}}}{'slot'}, "\n" if( $DBG );
		}
		case /ClientUserinfoChanged\:/
		{
			print "D: bits: $bits\n" if( $DBG );
			print "D: slot = $slot\n" if( $DBG );

			my %ht = {};
			my $in = 0;
			my $key = "";

			foreach my $v ( split( /\\/, $bits ) )
			{
				print "D: v = $v\n" if( $DBG );
				if( $in )
				{
					$ht{$key} = $v; 
					$in = 0;
					print "D: key set: $key = $v\n" if( $DBG );
				} else {
					$key = $v; 
					$in = 1;
					print "D: this is our key: $key\n" if( $DBG );
				} #endif
			} #end foreach
			${$slots{$ht{n}}}{'slot'} = $slot;
			${$slots{$ht{n}}}{'team'} = $ht{t};

			print "D: ClientUserinfoChanged() name = ", $ht{n}, "\n" if( $DBG );
			print "D: ClientUserinfoChanged() slot = ", $slots{$ht{n}}->{'slot'}, "\n" if( $DBG );
			print "D: ClientUserinfoChanged() team = ", $slots{$ht{n}}->{'team'}, "\n" if( $DBG );
		}
		case /ClientDisconnect\:/
		{
			# clear the slot 
			# we don't actually have to do this though 'cause we're 
			# tracking slots by screenname, so... 
		}
		case /kill\:/i
		{ 
			#my( $time, $command, $slot, $bits ) = split( /\ /, $_, 4 );
			print "D: found a kill by " if( $DBG );
			my( $crap, $crap, $name, $crap ) = split( /\ /, $bits, 4 );
			print "$name\n" if( $DBG );
			$rep{$name} += procKill($bits); 
		}
		case /say\:/i
		{ 
			print "D: found a say by" if( $DBG );
			my( $name, $crap ) = split( /\ /, $bits, 2 );
			$name =~ s/\://;
			print "$name\n" if( $DBG );
			$rep{$name} += procSay($bits); 
		}
		case /Bomb/
		{	
			#my( $time, $command, $slot, $bits ) = split( /\ /, $_, 4 );
			# 11:57 Bomb has been collected by 18
			# 15:08 Bomb was planted by 20
			# 17:10 Bomb was defused by 19!
			# $bits will be  ^^^^^^^^^^^^^^^^^^^^^
		
			print "D: bomb mode bits: $bits\n" if( $DBG );

			if( $bits =~ /been\ collected\ by/i )
			{
				$bits =~ s/been\ collected\ by//;
				my $ben = whosInSlotX( $bits );
				print "D: bomb collected by:$ben!\n" if( $DBG );
				if( exists $rep{$ben} )
				{
					$rep{$ben} += 5;
				}
			} elsif( $bits =~ /planted\ by/i ){
				$bits =~ s/planted\ by//; 
				my $ben = whosInSlotX( $bits );
				print "D: bomb planted by $ben!\n" if( $DBG );
				$rep{$ben} += 10 if( exists $rep{$ben} );
			} elsif( $bits =~ /defused\ by/i ){
				$bits =~ s/defused\ by//; 
				$bits =~ s/\!$//; 
				my $ben = whosInSlotX( $bits );
				print "D: bomb defused by $ben!\n" if( $DBG );
				$rep{$ben} += 15 if( exists $rep{$ben} );
			}

		}
		case /Flag\:/
		{
			# TODO: this is a complete punt, I haven't a clue if these values are right.
			#  worst-case, we have to invert these values... we'll do that if we need to.
			# status: 
			# 	0 = returned +1
			# 	1 = grabbed +5
			# 	2 = capped +20
			#
			#  4:39 Flag: 2 2: team_CTF_redflag
			#  bits         ^^^^^^^^^^^^^^^^^^^
			my( $status, $flag ) = split( /\:\ /, $bits, 2 );
			my $ben = whosInSlotX( $slot );
			if( $status == 2 )
			{
				$rep{$ben} += 20 if( exists $rep{$ben} );
			} elsif( $status == 1 ){
				$rep{$ben} += 5 if( exists $rep{$ben} );
			} elsif( $status == 0 ){
				$rep{$ben} += 1 if( exists $rep{$ben} );
			}
		}

	} #end switch

} #end while
close( IN );


foreach my $key ( sort keys( %rep ) )
{
	my $rep;
	eval {
		$rep = logB( log( $rep{$key} / 1 ), 10 ) * 100;
	}; if( $@ ){
		$rep = 0;
	}
	printf( "%s\t%i\t%i\n", $key, $rep{$key}, $rep );
}


exit( 0 );




sub logB
{
	my( $val, $base ) = @_; 
	my $retval;

	eval {
		$retval = log( $val) / log( $base );
	}; if( $@ ){
		return 0;
	}
	return $retval;
} #end logB()




sub procSay
{

	my( $line ) = shift;
	# TODO: expand this...  because that'd be fun.
	my @bad = ( 'fuck', 'shit', 'damn', 'hell', 'jesus', 'god', 'cock', 'pussie' );
	my @good = ( 'thanks', 'thx', 'gjt', 'good job team' );

	my $incval = 0;

	foreach( @bad )
	{
		if( $line =~ /$_/gi ){ $incval -= 1; }
	}
	foreach( @good )
	{
		if( $line =~ /$_/gi ){ $incval += 1; }
	}

	return $incval;
} #end procSay()




sub procKill
{

	my( $line ) = shift;
	my( @bits ) = split( /\ /, $line );
	my $actor = $bits[0];
	my $target = $bits[2];
	my $mods = pop( @bits ); 

	my $incval = 0;

	switch( $mods ) 
	{
		case /suicide/i	{ $incval = -10; } # you should be beaten.
		case /fallint/i	{ $incval = -5; } # you're an idiot, but not as bad as killing yourself.
		case /bled/i 	{ $incval = 5; } # these shouldn't count, but...
		case /sr8/i 	{ $incval = 12; } # more skilled than the assault rifles
		case /psg1/i 	{ $incval = 12; }  
		case /g36/i 	{ $incval = 10; } # pretty standard
		case /negev/i 	{ $incval = 10; }
		case /lr300/i 	{ $incval = 10; }
		case /m4/i 		{ $incval = 10; }
		case /ump/i 	{ $incval = 12; } # slower rate of fire makes it harder to use
		case /mp5/i 	{ $incval = 12; } # does much less damage, so its harder to kill with
		case /deagle/i 	{ $incval = 15; } # requires hella-good-aim
		case /beretta/i { $incval = 15; }
		case /hegrenade/i { $incval = 10; } # is based mostly on luck
		case /hk69/i 	{ $incval = 10; }
		case /knife/i 	{ $incval = 20; } # is substantially more difficult
		case /kicked/i 	{ $incval = 20; } # is substantially more difficult
	}

	my $shooter_team = $slots{$actor}->{'team'}; 
	my $targets_team = $slots{$target}->{'team'}; 

	#identify tk's.
	if( $shooter_team == $targets_team )
	{
		$incval = $incval * -1 if( $incval > 0 );
		print "D: BOOOOO!!!!!  $actor (team $slots{$actor}->{'team'}) is on the same team as $target (team $slots{$target}->{'team'})\n" if( $DBG );
	}

	return $incval; 
} #end procKill()




sub whosInSlotX
{
	# this is where we figure out who occupied a particular slot last... 
	# TODO this is a kludgey mess... is there a better way? i.e. one that isn't O^n or worse?
	my $targetSlot = shift;
	my $occupant = "";
	foreach( keys %slots )
	{
		$occupant = $_ if( ${$slots{$_}}{'slot'} == $targetSlot );
	}
	return $occupant; 
} #end whosInSlotX
