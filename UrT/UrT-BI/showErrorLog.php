<?php
/*
 * showErrorLog.php
 * by C.J. Steele <coreyjsteele@gmail.com>
 * http://sodaphish.com
 *
 * (C)opyright 2009, Corey J. Steele, all rights reserved.
 *
 * Created long long ago in a galaxy not so far away...
 *
 * This is a global configuration file for the site; it takes care of setting
 * up initial bits like the logger and the database connection and some globals.
 */

include_once( "config.php" );
include_once( "$rootdir/libs/commonLib.php" );

$session = getParam( "session" );
?>

<html>
	<head>
		<title><?php print $siteTitle; ?> - showErrorLog</title>
	</head>
	<body>

<?php
$fh = fopen( "$rootdir/logs/bi.log", "r" );

while( !feof( $fh ) )
{
	$line = fgets($fh, 4096);
	if( preg_match( '/$session/i', $line ) )
	{
		print $line . "<br/>\n";
	} //end if
} //end while

fclose( $fh );
?>

	</body>
</html>

<?php
$logger->debug( "$caller_short __END__" );

//EOF showErrorLog.php
?>