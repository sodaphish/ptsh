#!/usr/bin/php -q
<?php
include_once( "/var/www/config.php" );
include_once( "$rootdir/libs/rcon.php" );

$count = 0;

$serverQuery = "select serverip, serverport, serverrcon from servers"; 
$result = mysql_query( $serverQuery ) or $logger->error( mysql_error() );

while( list( $ip, $port, $rcon ) = mysql_fetch_row( $result ) )
{
	$q = new q3query( $ip, $port );
	$q->set_rconpassword( $rcon );
	$q->rcon('status');
	$response = $q->get_response();
	foreach( explode( "\n", $response ) as $line )
	{
		if( preg_match( "/^\ /", $line ) )
		{
			$count++;
		} #endif
	} #end foreach
} #end while

$insertQuery = "insert into playerTrend ( playerCount ) values ( $count )";
mysql_query( $insertQuery ) or $logger->error( mysql_error() );

$logger->debug( "$caller __END__" );
?>
