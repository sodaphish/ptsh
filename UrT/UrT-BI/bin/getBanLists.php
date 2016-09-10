#!/usr/bin/php -q
<?php

include_once( "/var/www/config.php" );

$date = date( "mdY" );

$query = "select serverip, serverport, serverftp, serverlog from servers";
$result = mysql_query( $query );

while( list( $ip, $port, $url, $log ) = mysql_fetch_row( $result ) )
{
	preg_match("/ftp:\/\/(.*?):(.*?)@(.*?)(\/.*)/i", $url, $options); 

	$logger->debug( "options[1] (username): " . $options[1] );
	$logger->debug( "options[2] (password): " . $options[2] );
	$logger->debug( "options[3] (hostname): " . $options[3] );
	$logger->debug( "options[4] (directory): " . $options[4] );

	$options[4] = preg_replace( "/^\//", "", $options[4] );

	$conn = ftp_connect( $options[3] );
	if( $conn ) 
	{
		$logger->debug( "got connected to $options[3]" );
		if( ftp_login( $conn, $options[1], $options[2] ) )
		{
			$logger->debug( "logged in as $options[1]" );
			if( ftp_chdir( $conn, $options[4] ) )
			{
				if( ftp_get( $conn, "$rootdir/banlists/$ip-$port-banlist.txt", "banlist.txt", FTP_ASCII ) )
				{
					$logger->info( "successfully downloaded $log to $rootdir/banlists/$ip-$port-banlist.txt" ); 
				} else {
					$logger->error( "couldn't fetch file banlist.txt" );
				}
			} else {
				$logger->error( "couldn't cd to $option[4]" );
			}
		} else {
			$logger->error( "couldn't login as $option[1]" );
		}
	} else {
		$logger->error( "couldn't connect to $option[3]" );
	}
	ftp_close( $conn );
}

$logger->debug( "$caller_short __END__" );

?>
