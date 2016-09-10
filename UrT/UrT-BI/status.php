<?php
include_once( "config.php" );
require( "$rootdir/libs/rcon.php" );
?>

<html>
<head>
	<title><?php print $siteTitle; ?> - Tool Status</title>
</head>
<body>

<div align="center">
<table width=80% border=0>
<tr><td>
<p><i>This page shows the current status of everything in the |WC| empire... its slow to load, so be patient, because it is testing everything as you wait, so none of this is cached, its all live data.</i></p>
<br><br>
<h1>Ban Interface</h1>
<strong>BI Backend</strong><br/>
<?php

passthru( "w | head -n 1" );
print "<br/>\n";

if( $db )
{
	print "<font color=#00FF00>The database server is on-line</font><br/>\n";
} else {
	print "<font color=#FF0000>The database server is on-line</font><br/>\n";
}
flush();

print "<strong>Game logs</strong><br/>\n";
$d = opendir( "$rootdir/gamelogs/" );
while( false !== ( $file = readdir( $d ) ) )
{
	if( !preg_match( "/^\./", $file ) )
	{
		$ctime = filectime( "$rootdir/gamelogs/$file" );
		$age = time() - $ctime;
		if( $age < 3600*6 )
		{
			print "<font color=#00ff00>$rootdir/gamelogs/$file is current (updated $age seconds ago)</font><br>\n";
			$logger->info( "$rootdir/gamelogs$file is current ($age)" );
		} else {
			print "<font color=#ff0000>$rootdir/gamelogs/$file is older than six hours by $age seconds.</font><br>\n";
			$logger->error( "$rootdir/gamelogs$file is old ($age)" );
		}
	}
}
closedir( $d );

print "<strong>RCON log files</strong><br/>\n";
$d2 = opendir( "$rootdir/rconlogs/" );
while( false !== ( $file = readdir( $d2 ) ) )
{
	if( !preg_match( "/^\./", $file ) )
	{
		$ctime = filectime( "$rootdir/rconlogs/$file" );
		$age = $ctime - time();
		if( $age < 3600*6 )
		{
			print "<font color=#00ff00>$rootdir/rconlogs/$file is current</font><br>\n";
			$logger->info( "$rootdir/gamelogs$file is current ($age)" );
		} else {
			print "<font color=#ff0000>$rootdir/rconlogs/$file is older than six hours by $age seconds.</font><br>\n";
			$logger->error( "$rootdir/gamelogs$file is old ($age)" );
		}
	}
}
closedir( $d2 );

print "<hr>\n";

$serverQuery = "select servername, serverip, serverport, serverrcon, serverftp from servers";
$serverQueryResult = mysql_query( $serverQuery ) or $logger->error( mysql_error() );

set_time_limit( 30 );

while( list( $servername, $serverip, $serverport, $serverrcon, $serverftp ) = mysql_fetch_row( $serverQueryResult ) )
{
	print "<h1>$servername</h1>\n";
	$q = new q3query( $serverip, $serverport );
	if( $q )
	{
		print "<font color=#00FF00>$serverip:$serverport is alive</font><br/>\n";
		$logger->info( "$serverip:$serverport is alive" );
	} else {
		print "<font color=#FF0000>$serverip:$serverport is DEAD</font><br/>\n";
		$logger->info( "$serverip:$serverport is alive" );
	}
	flush();

	$q->rcon( $serverrcon, "status" );
	$resp = preg_replace( "/print/", "", trim( $q->get_response() ) ); 
	if( $resp )
	{
		print "<font color=#ff0000>rcon to $serverip:$serverport FAILED ($resp)</font><br/>\n"; 
	} else {
		print "<font color=#00ff00>rcon to $serverip:$serverport is good</font><br/>\n"; 
	}
	flush();

	preg_match("/ftp:\/\/(.*?):(.*?)@(.*?)(\/.*)/i", $serverftp, $options);
	$conn = ftp_connect( $options[3] );
	if( $conn )
	{
		$logger->debug( "got connected to $options[3]" );
		if( ftp_login( $conn, $options[1], $options[2] ) )
		{
			print "<font color=#00FF00>ftp for $serverip:$serverport is functioning</font><br/>\n";
			$logger->info( "ftp for $serverip:$serverport is alive" );
		} else {
			print "<font color=#FF0000>ftp for $serverip:$serverport FAILED</font><br/>\n";
			$logger->error( "ftp for $serverip:$serverport FAILED" );
		}
	} else {
		print "<font color=#FF0000>ftp for $serverip:$serverport FAILED</font><br/>\n";
		$logger->error( "ftp for $serverip:$serverport FAILED" );
	}
	print "<hr>\n";
	flush();
} #end while
?>

</td></tr>
</table>
</div>

<?php
$logger->debug( "$caller_short __END__" );
?>
