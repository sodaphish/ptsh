<?php


list( $a, $b, $c, $d ) = preg_split( "/\./", getenv( REMOTE_ADDR ) );
$banned = 0;

$host = "$a.$b.$c.$d";
$classC = "$a.$b.$c.0"; 
$classB = "$a.$b.0.0"; 

$s = isBanned( $host );
if( $s )
{
	$banned = 1;
	print "$host either is, or has been banned in the past, please inquire about ban #$s<br/>";
} else {
	print "$host is not in the ban log.<br/>\n";
}

$s = isBanned( $classC );
if( $s )
{
	$banned = 1;
	print "$classC either is, or has been banned in the past, please inquire about ban #$s<br/>";
} else {
	print "$classC is not in the ban log.<br/>\n";
}

$s = isBanned( $classB );
if( $s )
{
	$banned = 1;
	print "$classB either is, or has been banned in the past, please inquire about ban #$s<br/>";
} else {
	print "$classB is not in the ban log.<br/>\n";
}


if( $banned )
{

	print "<p>Please follow-up on the ban(s) identified in the results above.  You can inquire about specific bans by contacting |WC|SodaPhish at sodaphish@gmail.com</p>\n";

}





function isBanned( $addr )
{
	$g_phpbanlog = "/home/hostedby/www/mine/wc/phpban.txt";
	$fh = fopen( $g_phpbanlog, "r" );
	while( $line = fgets( $fh ))
	{
		list( $timestamp, $session, $level, $message ) = preg_split( "/\ -\ /", $line, 4 );
		if( preg_match( "/$addr/", $message ) ){ return $session; }
	}
	fclose( $fh ); 
	return 0;
} #end isBanned()

?>
