<html>
<head>
	<title>|WC| game.log Query</title>
</head>
<body>


<div align="center">
<table width="600" border="0">
<tr><td>

<?php 
$completed = $_POST["completed"];
$server = $_POST["server"]; 
$q = $_POST["q"]; 

if( $completed )
{

	$logfile = "gamelogs/$server-games.log";
	$handle = fopen( $logfile, "r" );
	while( $line = fgets( $handle ) )
	{
		if( preg_match( "/$q/", $line ) )
		{	
			print "$line<br/><br/>\n";
		}
	}

} else {
?>

<form method="post" action="logquery.php">
<input type="hidden" name="completed" value="1">
Which server:<select name="server">
<?php

	$db = mysql_connect( "localhost", "hostedby_soda", "alpha01" );
	mysql_select_db( "hostedby_alpha" );
	$q = "select serverip, servername from servers";
	$r = mysql_query( $q );

	while( list( $ip, $name ) = mysql_fetch_row( $r ) )
	{
		print "<option value=\"$ip\">$name ($ip)</option>\n";
	}

?>
</select><br />
What to find:<input type="text" name="q"><br />
<input type="submit" value="Search">
</form>

<?php
} #end if
?>

</td></tr>
</table>
</div>


</body>
</html>
