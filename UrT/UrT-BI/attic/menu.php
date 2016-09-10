<?php
include_once( "config.php" );
?>
<html>
<head>
	<meta http-equiv="refresh" content=60>
</head>
<body>
<div align="center">
<table width=100% border=0>
<tr><td>
<div align=center>
<img src="WC-logo.png"><br/>
<form name="counter"><input type="text" align=right size="3" name="d2" style="border:0;"> seconds until next banBot execution</form><br/>
<script language="JavaScript">
<!--
var d = new Date();
var curr_min = d.getMinutes();
var curr_sec = d.getSeconds();
var seconds = ( curr_min % 5 ) * 60 + ( 60 - curr_sec ); 
var milisec=0; 
document.counter.d2.value=seconds;
function displayTimer(){ 
 if (milisec<=0){ 
    milisec=9 
    seconds-=1 
 } 
 if (seconds<=-1){ 
    milisec=0 
    seconds+=1 
 } 
 else 
    milisec-=1 
    document.counter.d2.value=seconds+"."+milisec 
    setTimeout("displayTimer()",100) 
} 
displayTimer();
-->
</script>
</div>
</td></tr>
<tr><td>

<div align="center">
<a target="_middle" href="main.html">Home</a> | 

<?php
$queueQuery = "select count( banid ) from bans where state='unprocessed'";
$queueQueryResult = mysql_query( $queueQuery ) or $logger->error( mysql_error() );
list( $banqueue ) = mysql_fetch_row( $queueQueryResult );
print "<a target=\"_middle\" href=\"banQueue.php\">$banqueue ban(s) queued</a> | ";
?>



<a target="_middle" href="q.php">Player Research</a> | 
<a target="_middle" href="gameLog.php">Game Log Viewer</a> | 
<a target="_middle" href="ban.php">Ban/Unban a Player</a> |
<a target="_middle" href="banquery.php">Ban Query</a> |
<a target="_middle" href="dossier.php">Dossier</a> |
<a target="_middle" href="playersOnline.html">Players Online</a> 

<?php
if( $privlevel__ > 1 )
{
?>
<br/>
<a target="_middle" href="editConfig.php">Edit Configs</a> | 
<a target="_middle" href="dRCON.php">Distributed RCON</a> 
<?php
}
?>

<?php 
if( $privlevel__ > 2 )
{
?>
| <a target="_middle" href="banman.php">BI Admin</a> |
<a target="_middle" href="rchron.php">Rchron</a> |
<a target="_middle" href="status.php">Status</a> |
<a target="_middle" href="debugLog.php">Debug Log</a> 
<?php
}
?>

</div>

</td></tr>
</table>
</div>
</body>
</html>

<?php
$logger->debug( "$caller_short __END__" );
?>
