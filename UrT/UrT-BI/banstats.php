<?php
/*
 * banstats.php
 * by C.J. Steele <coreyjsteele@gmail.com>
 * http://sodaphish.com
 * 
 * (C)opyright 2009, Corey J. Steele, all rights reserved.
 * 
 * Created September, 2009.
 * 
 * This script shows various statistics about ban interfaces.
 */
include_once( "config.php" );
?>
<html>
<head>
	<title><?php print $siteTitle; ?> - Ban Statistics</title>
	<meta http-equiv="refresh" content="60">
</head>
<body>
<div align="center">
<table width=80% border=0>
<tr><td>

<h2>Top 10 "Big Sticks"</h2>
<ol>

<?php
$biggestBanStickQuery = "select bannedby, count( banid ) as bans from bans where type = 'ban' group by bannedby order by bans desc limit 20";
$biggestBanStickResult = mysql_query( $biggestBanStickQuery ) or $logger->error( mysql_error() ); 
while( list( $bigStickAward, $bans ) = mysql_fetch_row( $biggestBanStickResult ) )
{
	print "<li>$bigStickAward has $bans bans</li>\n";
}
?>

</ol>

</td></tr>
</table>
</div>
</body>
</html>

<?php $logger->debug( "$caller_short __END__" ); ?>