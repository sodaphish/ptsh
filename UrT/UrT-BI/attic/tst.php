#!/usr/bin/php
<?php

include_once( "/var/www/config.php" );
include_once( "$rootdir/rcon.php" );

/*

$q = new q3query('1.2.3.4', 27960);
$q->set_rconpassword('hello');
$q->rcon('addbot sarge 5');
print $q->get_response();
$q->rcon('status');
print $q->get_response();
$q->rcon('kick sarge');
print $q->get_response();
$q->rcon('status');
print $q->get_response();
*/

$serverQuery = "select serverip, serverport, serverrcon from servers";
$serverResult = mysql_query( $serverQuery ) or $logger->error( mysql_error() );

while( list( $ip, $port, $rcon ) = mysql_fetch_row( $serverResult ) )
{
	$q = new q3query( $ip, $port );
	$q->set_rconpassword( $rcon );
	$q->rcon( "status" );
	print $q->get_response() . "\n";
}

$logger->debug( "$caller_short __END__" );
?>
