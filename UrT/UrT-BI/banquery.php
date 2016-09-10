<?php
/*
 * banquery.php
 * by C.J. Steele <coreyjsteele@gmail.com>
 * http://sodaphish.com
 *
 * (C)opyright 2009, Corey J. Steele, all rights reserved.
 *
 * Created September, 2009
 *
 * This script handles searching and viewing the ban history
 */
include_once( "config.php" );
?>
<html>
<head>
	<title><?php print $siteTitle; ?> - Ban Query</title>
</head>
<body>

<div align="center">
<table width="800" border="0">
<tr><td>

<?php
$completed = $_GET["completed"];
if( ! $completed ){ $completed = $_POST["completed"]; }
$logger->debug( "completed = $completed" );
$q = $_GET["q"];
if( ! $q ){ $q = $_POST["q"]; }
$logger->debug( "q = $q" );


function search( $query ) 
{
	global $logger;
	$searchQuery = "";
	if( ip2long( $query ) )
	{
		# they searched for an IP
		$searchQuery = "select banid, reason, type, ip, playerID, bannedby, notes, expires, state, sessionid from bans where ip like '$query%'";
	} else {
		# they searched for a username
		$searchQuery = "select banid, reason, type, ip, playerID, bannedby, notes, expires, state, sessionid from bans where playerID like '$query%'";
	} #endif
	$logger->debug( "searchQuery: $searchQuery" );

	$result = mysql_query( $searchQuery ) or $logger->error( mysql_error() ); 
	$resCount = mysql_affected_rows(); 
	$logger->debug( "search found $resCount matches" ); 
	if( $resCount )
	{
		print "<table width=\"100%\" border=\"0\">\n";
		print "<tr><td valign=\"top\" align=\"center\"><b>Ban #</b></td><td valign=\"top\" align=\"center\"><b>Reason</b></td><td valign=\"top\" align=\"center\"><b>Type</b></td><td valign=\"top\" align=\"center\"><b>IP</b></td><td valign=\"top\" align=\"center\"><b>Player</b></td><td valign=\"top\" align=\"center\"><b>Banned By</b></td><td valign=\"top\" align=\"center\"><b>Notes</b></td><td valign=top><b valign=\"top\" align=\"center\">Ban Expires</b></td><td valign=\"top\" align=\"center\"><b>Processed?</b></td><td valign=\"top\" align=\"center\"><b>Demo</b></td></tr>\n";
		while( list( $b, $r, $t, $i, $p, $B, $n, $e, $s, $S ) = mysql_fetch_row( $result ) )
		{
			$count = 0;
			$bgcolor = "#ffffff"; 
			if( $count % 2 ) 
			{
				$bgcolor = "#eeeeee"; 
			} else {
				$bgcolor = "#ffffff"; 
			}
			if( file_exists( "demos/$S.dm_68" ) )
			{
				print "<tr><td valign=top bgcolor=$bgcolor>$b</td><td valign=top bgcolor=$bgcolor>$r</td><td valign=top bgcolor=$bgcolor>$t</td><td valign=top bgcolor=$bgcolor><a target=_middle href=q.php?completed=1&q=$i>$i</a></td><td valign=top bgcolor=$bgcolor><a target=_middle href=q.php?completed=1&q=$p>$p</a></td><td valign=top bgcolor=$bgcolor>$B</td><td valign=top bgcolor=$bgcolor>$n</td><td valign=top bgcolor=$bgcolor>$e</td><td valign=top bgcolor=$bgcolor>$s</td><td valign=top bgcolor=$bgcolor><a href=demos/$S.dm_68>Demo</a></td></tr>\n";
			} else {
				print "<tr><td valign=top bgcolor=$bgcolor>$b</td><td valign=top bgcolor=$bgcolor>$r</td><td valign=top bgcolor=$bgcolor>$t</td><td valign=top bgcolor=$bgcolor><a target=_middle href=q.php?completed=1&q=$i>$i</a></td valign=top bgcolor=$bgcolor><td valign=top bgcolor=$bgcolor><a target=_middle href=q.php?completed=1&q=$p>$p</a></td><td valign=top bgcolor=$bgcolor>$B</td><td valign=top bgcolor=$bgcolor>$n</td><td valign=top bgcolor=$bgcolor>$e</td><td valign=top bgcolor=$bgcolor>$s</td><td valign=top bgcolor=$bgcolor>&nbsp;</td></tr>\n";
			}
			$count++;
		}
		print "</table>\n";
	} else {
		print "<p>There were no matches.</p>\n";
	}
} //end search()


if( $completed )
{

	print "<h2>Ban search results for '$q'</h2>\n";
	search( $q );
} else {
?>

<div align="center">
<form method="get" action="<?php print $caller; ?>">
<input type="hidden" name="completed" value="1">
<input size="40" type="text" name="q" value="name or IP (192.168.209.0)">
<input type="submit" value=" &gt; &gt; ">
</form>
<p><i>Below are all the bans on record.</i></p>
<hr width=100%>
</div>

<?php
	search( "" );
} #endif
?>

</td></tr>
</table>
</div>

</body>
</html>

<?php $logger->debug( "$caller_short __END__" ); ?>
