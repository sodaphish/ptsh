<?php
/*
 * newMenu.php
 * by C.J. Steele <coreyjsteele@gmail.com>
 * http://sodaphish.com
 *
 * (C)opyright 2009, Corey J. Steele, all rights reserved.
 *
 * Created October, 2009
 *
 * This paints the top menu according to access-control.
 */
include_once( "config.php" );
?>
<html>
<head>
	<title><?php print $siteTitle; ?> - Menu</title>
</head>
<body>


<table border=0 width=100%>
<tr>
	<td valign=top>
		<!-- links-->
<a target="_middle" border=0 href="motd.php"><img src="WC-logo.png" border=0></a>

	</td>
	<td valign=top width=100%>
<!-- links -->
<nobr><a target="_middle" href="q.php">Player Research</a></nobr> |
<nobr><a target="_middle" href="gameLog.php">Game Log Viewer</a></nobr> |
<nobr><a target="_middle" href="ban.php">Ban/Unban a Player</a></nobr> |
<nobr><a target="_middle" href="banquery.php">Ban Query</a></nobr> |
<nobr><a target="_middle" href="dossier.php">Dossier</a></nobr> |
<nobr><a target="_middle" href="playersOnline.html">Players Online</a></nobr> |
<nobr><a target="_middle" href="status.php">Status</a></nobr><br>


<?php
if( $privlevel__ > 1 )
{
?>
<nobr><a target="_middle" href="editConfig.php">Edit Configs</a></nobr> |
<nobr><a target="_middle" href="dRCON.php">Distributed RCON</a></nobr> 
<?php
	} #endif
?>

<?php 
	if( $privlevel__ > 2 )
	{
?>
| <nobr><a target="_middle" href="banman.php">BI Admin</a></nobr> |
<nobr><a target="_middle" href="rchron.php">Rchron</a></nobr> |
<nobr><a target="_middle" href="debugLog.php">Debug Log</a></nobr>
<?php
	} #endif
?>
	<hr width=100%>

<?php
$queueQuery = "select count( banid ) from bans where state='unprocessed' or state='midway'";
$queueQueryResult = mysql_query( $queueQuery ) or $logger->error( mysql_error() );
list( $banqueue ) = mysql_fetch_row( $queueQueryResult );
#print "<nobr><a target=\"_middle\" href=\"banQueue.php\">$banqueue ban(s) queued</a> | ";
print "<nobr>";

$adminctq = "select count( uid ) from users";
$adminctr = mysql_query( $adminctq );
list( $adminct ) = mysql_fetch_row( $adminctr );
print "$adminct admins are: ";


$banctq = "select count( banid ) from bans";
$banctr = mysql_query( $banctq );
list( $banct ) = mysql_fetch_row( $banctr );
print "managing $banct bans (<a target=\"_middle\" href=\"banQueue.php\">$banqueue queued</a>), ";

$playerctq = "select count( ipid ) from ips";
$playerctr = mysql_query( $playerctq );
list( $playerct ) = mysql_fetch_row( $playerctr );
print "tracking $playerct players, ";

$svrctq = "select count( sid ) from servers";
$svrctr = mysql_query( $svrctq );
list( $svrct ) = mysql_fetch_row( $svrctr );
print "and managing $svrct servers.</nobr>";

?>

<form name="counter"><input type="text" align=right size="3" name="d2" style="border:0;"> seconds until next banBot execution</form>


<script language="JavaScript">
<!--
var d = new Date();
var curr_min = d.getMinutes();
var curr_sec = d.getSeconds();
var seconds = ( curr_min % 5 ) * 60 + ( 60 - curr_sec ); 
var milisec=0; 
document.counter.d2.value=seconds;
function displayTimer(){ 
	if (seconds==0 && milisec==0){
		document.location.href="newMenu.php"
	}
	if (milisec<=0){ 
		milisec=9 
		seconds-=1 
	} 
	if (seconds<=-1){ 
		milisec=0 
		seconds+=1 
	} else 
	milisec-=1
	document.counter.d2.value=seconds+"."+milisec 
	setTimeout("displayTimer()",100) 
} 
displayTimer();
-->
</script>


	</td>
</tr>
</table>



</body>
</html>

<?php
$logger->debug( "$caller_short __END__" );
?>
