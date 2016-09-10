<html>
<head>
  <meta http-equiv="refresh" content="120">
	<title><?php print $siteTitle; ?> - Players On-Line</title>
</head>
<body>

<!-- <div align="center">
<img src=serverGraph.php>
</div>
-->

<h1>Players Currently On-line</h1>

<?php

include_once( "config.php" );
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
			print "$line<br>\n";
			$count++;
		} #endif
	} #end foreach
} #end while


print "<br><br>\nCurrently $count players online.<br/>\n";

$logger->debug( "$caller __END__" );

?>

</body>
</html>
