<?php
include_once( "config.php" );
include_once( "libs/rcon.php" );

$completed = $_GET['completed'];
if( ! $completed ){ $completed = $_POST['completed']; } 
$logger->debug( "completed: $completed" );

$server = $_GET['server'];
if( ! $server ){ $server = $_POST['server']; } 
$logger->debug( "server: $server" );

$cmd = $_GET['cmd'];
if( ! $cmd ){ $cmd = $_POST['cmd']; } 
$logger->debug( "cmd: $cmd" );

?>
<html>
<head>
	<title><?php print $siteTitle; ?> - Distributed RCON utility</title>
</head>
<body>


<div align=center>
<table width=80% border=0>
<tr><td>

<?php


function drawInputBox()
{
	global $logger;
	global $caller;

	print "<form method=post action=$caller>\n";
	print "<input type=hidden name=completed value=1>\n";
	print "<b>Step 1: Pick the servers you want the command to run on</b><br/><i>(hold CTRL to select multiples)</i><br/>";
	print "<select name=server[] multiple size=7>\n";
	$query = "select sid, servername from servers";
	$result = mysql_query( $query );
	while( list( $id, $name ) = mysql_fetch_row( $result ) )
	{
		print "<option value=\"$id\">$name</option>\n";
	}
	print "</select><br/><br/>\n";
	print "<b>Step 2: Type in the command to run on the selected servers</b><br/><i>(e.g. 'status' to get the selected servers to run `rcon status`)</i><br/>";
	print "<input type=text size=30 name=cmd value=\"status\"><br/><br/>\n";
	print "<b>Step 3: Click \"Run It!\"</b><br/>\n";
	print "<input type=submit value=\"Run It!\">";
	print "</form>";
}


if( $completed )
{
	# do the work... 
	foreach( $server as $s )
	{
		$serverQuery = "select serverip, serverport, serverrcon from servers where sid=$s"; 
		$serverResult = mysql_query( $serverQuery ) or $logger->error( mysql_error() );
		if( $serverResult )
		{
			list( $sI, $sP, $sR ) = mysql_fetch_row( $serverResult );
			$q = new q3query( "$sI", "$sP" );
			$q->set_rconpassword( "$sR" );
			$q->rcon( "$cmd" );
			print "<b>$sI:$sP</b><br/>\n";
			print "<pre>\n";
			print $q->get_response();
			print "</pre>\n";
			flush();
		}
	}
	print "<hr>\n";
	drawInputBox();
} else {
	# show the form
	drawInputBox();
}
?>


</td></tr>
</table>
</div>

</body>
</html>

<?php
$logger->debug( "$caller_short __END__" );
?>
