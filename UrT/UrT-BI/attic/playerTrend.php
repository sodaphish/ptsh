#!/usr/bin/php -q 
<?php

include_once( "/var/www/config.php" );

$count = 0;

$serverQuery = "select serverip, serverport from servers"; 
$result = mysql_query( $serverQuery );

while( list( $ip, $port ) = mysql_fetch_row( $result ) )
{
	foreach( explode( "\x0a", shell_exec( "$rootdir/bin/qstat -raw ' ' -nh -pa -P -q3s $ip:$port" ) ) as $l )
	{
		if( !preg_match( "/^Q3S\ $ip/", $l ) and !preg_match( "/^\s*$/", $l ) )
		{
			$parts = array();
			$parts = explode( " ", $l );
			$name = "";
			for( $x = 0; $x < sizeof( $parts ) - 2; $x++ )
			{
				$name .= "$parts[$x]"; 
			}
			$count++;
		}
	}
}

$insertQuery = "insert into playerTrend ( playerCount ) values ( $count )";
mysql_query( $insertQuery ) or $logger->error( mysql_error() );

$logger->debug( "$caller __END__" );
?>
