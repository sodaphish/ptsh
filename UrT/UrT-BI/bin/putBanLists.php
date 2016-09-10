#!/usr/bin/php -q
<?php

include_once( "/var/www/config.php" );

$date = date( "mdY" );

# this is our banlist to upload
$banlist = $argv[1];

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

				if( ! $banlist )
				{
					$banlist = "$rootdir/banlists/$ip-$port-banlist.txt";
				} #endif

				if( ftp_put( $conn, "banlist.txt", "$banlist", FTP_ASCII ) )
				{
					$logger->info( "successfully uploaded $banlist to $options[3]" ); 
				} else {
					$logger->error( "couldn't upload $banlist to banlist.txt on $options[3]" );
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
