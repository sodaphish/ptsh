<?php
/*
 * debugLog.php
 * by C.J. Steele <coreyjsteele@gmail.com>
 * http://sodaphish.com
 * 
 * (C)opyright 2009, Corey J. Steele, all rights reserved.
 * 
 * Created September,2009
 * 
 * This is a web-based viewer for the debug logs that are generated with Logger.
 */
include_once( "config.php" );

$log = $_GET['log']; 
if( ! $log ){ $log = $_POST['log']; }
$logger->debug( "logfile to view is $log" );

//TODO: implement a windowing mechanism that has forward, backward, last page, first page, and a search function.
?>

<html>
<head>
	<title><?php print $siteTitle; ?> - Backend Log Viewer</title>
</head>
<body>


<div align="center">
<table width=80% border="0">
<tr><td>

<div align="center">
<form method="get" action="<?php print $caller; ?>">
<select name="log">

<?php
$dh = opendir( "$rootdir/logs" );
while( false !== ( $file = readdir( $dh ) ) )
{

	if( preg_match( "/^\.*$/", $file ) )
	{
	} else {
		if( preg_match( "/$log/", $file ) )
		{
			echo "<option selected value=\"$file\">$file</option>";
		} else {
			echo "<option value=\"$file\">$file</option>";
		} //end if
	} //end if
} //end while
?>

</select>
<input type="submit" value="View"> 
</form>
</div>
<hr>

<?php
if( $log and file_exists( "$rootdir/logs/$log" ) )
{
	$f = fopen( "$rootdir/logs/$log", "r" );
	while( $line = fgets( $f ) )
	{
		if( preg_match( "/\ DBG\ /", $line ) ){
			print "<font color=#bbbbbb>$line</font><br/>\n";
		} elseif( preg_match( "/\ INF\ /", $line ) ){
			print "<font color=#0000ff>$line</font><br/>\n";
		} elseif( preg_match( "/\ WARN\ /", $line ) ){
			print "<font color=#ffff00>$line</font><br/>\n";
		} elseif( preg_match( "/\ ERR\ /", $line ) ){
			print "<font color=#ff0000>$line</font><br/>\n";
		} else {
			print "$line<br/>\n";
		} //end if
	} //end while
	fclose( $f );
} //end if
?>

</td></tr>
</table>
</div>

</body>
</html>

<?
$logger->debug( "$caller_short __END__" );

//EOF debugLog.php
?>
