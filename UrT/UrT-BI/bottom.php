<?php
/*
 * bottom.php
 * by C.J. Steele <coreyjsteele@gmail.com>
 * http://sodaphish.com
 * 
 * (C)opyright 2009, Corey J. Steele, all rights reserved.
 * 
 * Created September, 2009
 * 
 * This draws the bottom frame of the main page.
 */
include_once( "config.php" );
?>

<html>
<head>
	<meta http-equiv="refresh" content="60">
</head>
<body bgcolor=#bbbbbb>
<div align="center">
<table width=100% border=0>
<tr>

<?php

print "<td align=left><strong>Logged in as $username__ (from: $remote_addr)</strong></td>";

/*
$queueQuery = "select count( banid ) from bans where state='unprocessed' and type='ban'";
$queueQueryResult = mysql_query( $queueQuery ) or $logger->error( mysql_error() );
list( $banqueue ) = mysql_fetch_row( $queueQueryResult );
#print "<td>$banqueue bans in the queue</td>";

$adminctq = "select count( uid ) from users";
$adminctr = mysql_query( $adminctq );
list( $adminct ) = mysql_fetch_row( $adminctr );
print "<td align=center>$adminct admins are:</td>";


$banctq = "select count( banid ) from bans";
$banctr = mysql_query( $banctq );
list( $banct ) = mysql_fetch_row( $banctr );
print "<td align=center>managing $banct bans,</td>";

$playerctq = "select count( ipid ) from ips";
$playerctr = mysql_query( $playerctq );
list( $playerct ) = mysql_fetch_row( $playerctr );
print "<td align=center>tracking $playerct players,</td>";

$svrctq = "select count( sid ) from servers";
$svrctr = mysql_query( $svrctq );
list( $svrct ) = mysql_fetch_row( $svrctr );
print "<td align=center>and managing $svrct servers.</td>";
*/

$highWaterQuery = "select max( playerCount ), timestamp from playerTrend group by playercount order by playercount desc limit 1";
$highWaterResult = mysql_query( $highWaterQuery ) or $logger->error( mysql_error() );
list( $highWaterMark, $highWaterTime ) = mysql_fetch_row( $highWaterResult );


$currentPlayersOnline = "select playercount from playerTrend where id= ( select max( id ) from playerTrend )"; 
$currentPlayersOnlineResult = mysql_query( $currentPlayersOnline ) or $logger->error( mysql_error() );
list( $currentOnline ) = mysql_fetch_row( $currentPlayersOnlineResult );
print "<td align=center><nobr></nobr></td>";

$biggestBanStickQuery = "select bannedby, count( banid ) as bans from bans where type = 'ban' group by bannedby order by bans desc limit 1";
$biggestBanStickResult = mysql_query( $biggestBanStickQuery ) or $logger->error( mysql_error() ); 
list( $bigStickAward, $bans ) = mysql_fetch_row( $biggestBanStickResult );
print "<td align=right><strong><a href=banstats.php target=_middle>Biggest Ban Stick: $bigStickAward ($bans)</a></strong></td>\n";

?>

</tr>
</table>
</div>
</body>
</html>

<?php $logger->debug( "$caller_short __END__" ); ?>

