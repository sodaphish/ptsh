#!/usr/bin/php -q
<?php
/*
 * bin/rchron.php
 * by C.J. Steele <coreyjsteele@gmail.com>
 * http://sodaphish.com
 * 
 * (C)opyright 2009, Corey J. Steele, all rights reserved.
 * 
 * Created on Oct 20,2009
 * 
 * This script executes rcon commands as scheduled through the rchron web interface.
 * 
 * TODO: implement http://pear.php.net/manual/en/package.system.system-daemon.examples.simple.php 
 */
include_once "/var/www/config.php"; 
include_once( "$rootdir/libs/ProcessHandler.php" );

if( ProcessHandler::isActive() )
{
	$logger->error( "$caller_short already running!" );
	die( "Already running!\n" );
} else {
	ProcessHandler::activate();
	$epoch = 0;
	$intervals = array( 1, 5, 60 );
	$multipliers = array( 1, 60, 3600 ); # min, hrs, days
	while( 1 )
	{
		foreach( $multipliers as $m )
		{
			foreach( $intervals as $i )
			{
				if( ( ( time() - $epoch ) % ( $i * 60 * $m ) ) == 0 )
				{
					# thread this out and execute the job...
					//TODO: put the bits you actually want to do here.
					print "\nfire $i!\n";
				} //end if
			} //end foreach
		} //end foreach
		print ".";
		sleep( 1 );
	} //end while
} //end if

$logger->debug( "$caller_short __END__" );


//EOF bin/rchron.php
?>
