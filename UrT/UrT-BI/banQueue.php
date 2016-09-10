<?php
include_once( "config.php" );
?>

<html>
<head>
	<title><?php print $siteTitle; ?> - Ban Queue Viewer</title>
</head>
<body>


<?php
$searchQuery = "";
$searchQuery = "select banid, reason, type, ip, playerID, bannedby, notes, expires, state, sessionid from bans where state='unprocessed' or state='midway'"; 

$result = mysql_query( $searchQuery ) or $logger->error( mysql_error() ); 
$resCount = mysql_affected_rows(); 
$logger->debug( "search found $resCount matches" ); 
if( $resCount )
{
	print "<table width=\"100%\" border=\"0\">\n";
	print "<tr><td valign=\"top\" align=\"center\"><b>Ban #</b></td><td valign=\"top\" align=\"center\"><b>Reason</b></td><td valign=\"top\" align=\"center\"><b>Type</b></td><td valign=\"top\" align=\"center\"><b>IP</b></td><td valign=\"top\" align=\"center\"><b>Player</b></td><td valign=\"top\" align=\"center\"><b>Banned By</b></td><td valign=\"top\" align=\"center\"><b>Notes</b></td><td><b valign=\"top\" align=\"center\">Ban Expires</b></td><td valign=\"top\" align=\"center\"><b>Processed?</b></td><td valign=\"top\" align=\"center\"><b>Demo</b></td></tr>\n";
	while( list( $b, $r, $t, $i, $p, $B, $n, $e, $s, $S ) = mysql_fetch_row( $result ) )
	{
		$bgcolor="#ffffff";
		if( $count % 2 )
		{
			$bgcolor="#eeeeee";
		} else {
			$bgcolor="#ffffff";
		}
		if( file_exists( "demos/$S.dm_68" ) )
		{
			print "<tr><td valign=top bgcolor=$bgcolor><a href=banquery.php?q=$i&completed=1>$b</a></td><td valign=top bgcolor=$bgcolor>$r</td><td valign=top bgcolor=$bgcolor>$t</td><td valign=top bgcolor=$bgcolor><a target=_middle href=q.php?completed=1&q=$i>$i</a></td><td valign=top bgcolor=$bgcolor><a target=_middle href=q.php?completed=1&q=$p>$p</a></td><td valign=top bgcolor=$bgcolor>$B</td><td valign=top bgcolor=$bgcolor>$n</td><td valign=top bgcolor=$bgcolor>$e</td><td valign=top bgcolor=$bgcolor>$s</td><td valign=top bgcolor=$bgcolor><a href=demos/$S.dm_68>Demo</a></td></tr>\n";
		} else {
			print "<tr><td valign=top bgcolor=$bgcolor><a href=banquery.php?q=$i&completed=1>$b</a></td><td valign=top bgcolor=$bgcolor>$r</td><td valign=top bgcolor=$bgcolor>$t</td><td valign=top bgcolor=$bgcolor><a target=_middle href=q.php?completed=1&q=$i>$i</a></td><td valign=top bgcolor=$bgcolor><a target=_middle href=q.php?completed=1&q=$p>$p</a></td><td valign=top bgcolor=$bgcolor>$B</td><td valign=top bgcolor=$bgcolor>$n</td><td valign=top bgcolor=$bgcolor>$e</td><td valign=top bgcolor=$bgcolor>$s</td><td>&nbsp;</td></tr>\n";
		}
		$count++;
	}
	print "</table>\n";
} else {
	print "<p>There were no matches.</p>\n";
}
?>



</body>
</html>

<?php
$logger->debug( "$caller_short __END__" );
?>
