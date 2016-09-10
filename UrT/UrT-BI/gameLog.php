<?php
include_once( "config.php" );

$log = $_GET['log']; 
if( ! $log ){ $log = $_POST['log']; }
$logger->debug( "logfile to view is $log" );
$q = $_GET['q']; 
if( ! $q ){ $q = $_POST['q']; }
$logger->debug( "query $q" );
?>

<html>
<head>
	<title><?php print $siteTitle; ?> - Game Log Viewer</title>
</head>
<body>


<div align="center">
<table width=80% border="0">
<tr><td>

<div align="center">
<form method="get" action="<?php print $caller; ?>">
<select name="log">
<?php
	$serverQuery = "select servername, serverip, serverlog from servers";
	$serverQueryResult = mysql_query( $serverQuery ) or $logger->error( mysql_error() );

	while( list( $servername, $serverip, $serverlog ) = mysql_fetch_row( $serverQueryResult ) )
	{
		if( preg_match( "/$serverip-$serverlog/", $log ) )
		{
			print "<option selected value=\"$serverip-$serverlog\">$servername</option>";
		} else {
			print "<option value=\"$serverip-$serverlog\">$servername</option>";
		}
	}
?>
</select>
<input type="submit" value="View"> 
</form>

<?php
if( $log )
{
?>
<form method="get" action="<?php print $caller; ?>">
<input type=hidden name=log value=<?php print $log; ?>>
<input type=text name=q value="<?php print $q; ?>">
<input type=submit value="Search">
</form>
<?php
}
?>
</div>

<?php
if( $log and file_exists( "$rootdir/gamelogs/$log" ) )
{
	$f = fopen( "$rootdir/gamelogs/$log", "r" );
	while( $line = fgets( $f ) )
	{
		if( $q )
		{
			if( preg_match( "/$q/", $line ) )
			{
				print "$line<br/><br/>\n";
			}
		} else {
			print "$line<br/><br/>\n";
		}
	}
	fclose( $f );
}
?>

</td></tr>
</table>
</div>

</body>
</html>

<?
$logger->debug( "$caller_short __END__" );
?>
