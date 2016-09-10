<html>
<head>
	<title>|WC| Ban Inquiry</title>
</head>
<body>


<hr>

<table border="0">
<?php

$lastsess = ""; 
$user = "";
$tmpban = 0;
$expiry = 0;

foreach( file( "phpban.txt" ) as $line )
{

	list( $timestamp, $session, $level, $message ) = preg_split( "/\ -\ /", $line, 4 );

	if( $level == "INF" )
	{


	if( $session != $lastsess )
	{
		$cursession = $session; 
	} 

	if( preg_match( "/^username/", $message ) )
	{
		$user = preg_replace( "/username\ =\ /", "", $message );
	}

	if( preg_match( "/^TEMPBAN\:/", $message ) and ( $session == $cursession ) )
	{
		list( $junk, $expiry ) = preg_split( "/\//", $message, 2 );
		$expiry = date( "r", $expiry );
		$tmpban = 1;
	}
	
	if( preg_match( "/BANNING/", $message ) )
	{

		$color = "0000ff"; 
		if( preg_match( "/^UN/", $message ) )
		{ 
			$color = "ff0000"; 
			if( $session == "BANBT" )
			{
				$user = "BanBot";
			}
		}
		print "<tr>\n";
		print "<td><font color=$color>$timestamp</font></td>";
		print "<td><font color=$color><b>$user</b></font></td>";

		$message = preg_replace( "/^BANNING\ /", "", $message );
		$message = preg_replace( "/^UNBANNING\ /", "", $message );
		$message = preg_replace( "/because:\ /", "", $message );

		list( $ip, $reason ) = preg_split( "/\s/", $message, 2 );

		print "<td><font color=$color>$ip</font></td>";
		if( file_exists( "demos/$cursession.dm_68" ) )
		{
			if( $tmpban )
			{
				print "<td><i><font color=$color><a href=demos/$session.dm_68>$reason</a> (expires: $expiry)</font></i></td>\n";
			} else {
				print "<td><font color=$color><a href=demos/$session.dm_68>$reason</a></font></td>\n";
			}
		} else {
			if( $tmpban )
			{
				print "<td><i><font color=$color>$reason (expires: $expiry)</font></i></td>\n";
			} else {
				print "<td><font color=$color>$reason</font></td>\n";
			}
		}
		print "</tr>\n";
		$tmpban = 0;
	}

	}
}

?>
</table>

</body>
</html>
