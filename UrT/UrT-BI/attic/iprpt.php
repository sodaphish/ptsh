<html>
<head>
	<title>|WC| player IP report</title>
</head>
<body>
<div align="center">
<table width="650">
<tr><td>

<?php

include_once( "config.php" );

$q = $_GET["q"]; 

if( $q )
{
	print "<h2>$q</h2>\n"; 
	$query = "SELECT ip, name, guid from ips where name like '%". $q . "%";
	$result = mysql_query( $query ); 
	while( list( $i, $n, $g ) = mysql_fetch_row( $result ) )
	{
		print "<a href=q.php?q=$i>$i</a><br />\n";
	} //end while
} else {
	$logger->error( "Crafting URLS!" );
	print "boo!";
}

?>

</td></tr>
</table>
</div>
</body>
</html>
