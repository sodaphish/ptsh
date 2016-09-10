<html>
<head>
	<title>FWAP Port Scanner</title>
</head>
<body>

<font face="Verdana, Helvetica, Arial" size=-1>


<?php

$nmap = "/usr/bin/nmap"; 
error_reporting( 0 );

if( $query )
{
	//do the work!

	print "<h2>Scan Results for $query</h2><hr>"; 
	print "<pre>\n"; 
	print shell_exec( "$nmap $query" );
	print "</pre>\n"; 

	print "
	<form method=post action=portscan.php>
	<input type=text name=query value=\"$query\">
	<input type=submit value=\" >> \">
	<form>
	";

} else {
	//show the form...

	print "
	<H2>Port Scanner Tool</h2><hr>
	<form method=post action=portscan.php>
	<input type=text name=query value=\"$query\">
	<input type=submit value=\" >> \">
	<form>
	";
}

?>


</font>

</body>
</html>
