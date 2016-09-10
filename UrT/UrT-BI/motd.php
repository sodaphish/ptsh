<?php
/*
 * motd.php
 * by C.J. Steele <coreyjsteele@gmail.com>
 * http://sodaphish.com
 *
 * (C)opyright 2009, Corey J. Steele, all rights reserved.
 *
 * Created on September,2009
 *
 * simple website that would show the last 15 MOTD messages and color codes them.
 */
include_once( "config.php" );
?>

<html>
<head> 
	<title><?php print $siteTitle; ?> - Message Of The Day</title>
</head>
<body>

<h1>MOTD/News</h1>
<small>(Message Of The Day)</small>

<ul>

<?php

$motdQuery = "select motdAuthor, motdDate, motdBody from motd order by motdDate desc limit 15";
$motdQueryResults = mysql_query( $motdQuery ) or $logger->error( mysql_error() );

$count = 0;
$bgcolor="#eeeeee"; 
while( list( $motdAuthor, $motdDate, $motdBody ) = mysql_fetch_row( $motdQueryResults ) )
{
	if( $count == 0 )
	{
		$bgcolor="#ffff00";
	} elseif( $count % 2 ){
		$bgcolor="#ffffff";
	} else {
		$bgcolor="#eeeeee"; 
	}
	print "<li style=\"background:$bgcolor;\"><strong>$motdDate ($motdAuthor)</strong><br/>$motdBody</li>\n";
	$count++;
}

?>


</ul>

</body>
</html>
