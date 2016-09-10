#!/usr/bin/php -q
<?php

include_once( "/var/www/config.php" );

$date = date( "mdY" );

$logsdir = "$rootdir/logs"; 
$gamelogsdir = "$rootdir/gamelogs";
$rconlogsdir = "$rootdir/rconlogs";


# TODO make backup directory

# TODO move all logs into the date-stamped directory

# TODO get all the new logs


$query = "select serverip, serverftp, serverlog from servers";
$result = mysql_query( $query );

while( list( $ip, $url, $log ) = mysql_fetch_row( $result ) )
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
		if( ftp_login( $conn, $options[1], $options[2] ) )
		{


			if( ftp_chdir( $conn, $options[4] ) )
			{


				# rename qconlog
				if( ftp_rename( $conn, "qconsole.log", "qconsole.log-$date" ) )
				{
				} else {
					$logger->error( "couldn't rename qconsole.log to qconsole.log-$date" );
				}


				# rename gamelog
				if( ftp_rename( $conn, "$log", "$log-$date" ) )
				{
				} else {
					$logger->error( "Couldn't rename $log to $log-$date" );
				}

				# download the config

				# download the backed-up qconlog 
				if( ftp_get( $conn, "$rootdir/rconlogs/$ip-$loginName-qconsole.log", "qconsole.log", FTP_ASCII ) )
				{
				}


				# download the backed-up gamelog
				if( ftp_get( $conn, "$rootdir/gamelogs/$ip-$log", "$log", FTP_ASCII ) )
				{
					$logger->info( "download completed successfully" );
				} else {
					$logger->warn( "failed to download $log" );
				}


			} else {
				$logger->error( "CD $options[4] failed!" );
			}

		} else {
			$logger->error( "Login failed!  $options[1]/$options[2]" );
		}
		ftp_close( $conn );

	} else {
		$logger->error( "failed to connect to $options[3]" );
	}

} #end while

# TODO: dump new logs into the database

$logger->debug( "$caller_short __END__" );
?>
